from error import *
from mail_remind import send_mail
import requests
import re
import json
from template import *


# 这里所有的[1:]（包括后面的cookie返回） 都是因为直接复制的值开头它是空格，是违规标志
def build_header(header_str: str):
    header_lines = header_str.split("\n")
    header = {}
    for line in header_lines:
        if line == "":
            continue
        if line[0] == ":":
            line = line[1:]
        try:
            [key, value] = line.split(":")
        except:
            if ":" not in line:
                continue
            location = re.search(":", line).span()[0]
            key = line[:location]
            value = line[location + 1:]

        if value[0] == " ":
            value = value[1:]
        header[key] = value
    return header


# 没有cookie
def build_cookie(cookie_file_name: str):
    try:
        with open(cookie_file_name, "r", encoding="utf8") as reader:
            cookie_all = reader.read()
    except:
        return Error(FILE_OPEN_ERROR, "cant open file %s, check if it is exists" % cookie_file_name)

    try:
        return cookie_all.split(":")
    except:
        return Error(PARAM_ERROR, "build cookie some param wrong")


def get_conversation_param(cookie_file_name: str):
    headers = build_header(CONVERSATION_HEADER)
    if type(headers) == Error:
        return headers
    cookies = build_cookie(cookie_file_name)
    if type(cookies) == Error:
        return cookies

    headers[cookies[0]] = cookies[1][1:]
    resp = requests.get(CREATE_CHAT_URL, headers=headers)
    if resp.status_code != 200:
        return Error(REQUEST_EXCEPTION, "Something wrong where try to access %s" % CREATE_CHAT_URL)
    try:
        param = resp.json()
    except:
        return Error(PARAM_JSON_ERROR, "Response from %s is not excepted or be translated to json" % CREATE_CHAT_URL)

    if param["result"]["value"] == UNAUTHORIZED:
        return send_mail("更新cookie/headers", "请及时更新你的bing cookie 和 headers")

    try:
        resp2 = requests.get(GET_TRACE_ID, headers=headers)
        trace_id = re.findall('''EventID:"(\w*)"''', resp2.text)
    except:
        return Error(GET_EVENT_ID, "something wrong with get eventId/ traceId")
    if len(trace_id) != 1:
        return Error(GET_EVENT_ID, "something wrong with get eventId/ traceId")
    param["traceId"] = trace_id[0]
    return param
