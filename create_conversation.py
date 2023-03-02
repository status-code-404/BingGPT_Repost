from error import *
from mail_remind import send_mail
import requests
import re
import json
from template import *


def replace_invaild_first_character(str_: str):
    while str_[0] in ": ":
        str_ = str_[1:]
    return str_


# 这里所有的[1:]（包括后面的cookie返回） 都是因为直接复制的值开头它是空格，是违规标志
def build_header(header_str: str):
    header_lines = header_str.split("\n")
    header = {}
    for line in header_lines:
        if line == "" or ":" not in line:
            continue
        line = replace_invaild_first_character(line)
        location = re.search(":", line).span()[0]
        header[line[:location]] = replace_invaild_first_character(line[location + 1:])
    return header


# 没有cookie
def build_cookie(cookie_file_name: str, mode=None):
    try:
        with open(cookie_file_name, "r", encoding="utf8") as reader:
            cookie_all = reader.read()
    except:
        return Error(FILE_OPEN_ERROR, "cant open file %s, check if it is exists" % cookie_file_name)

    if cookie_all[:7] != "cookie:":
        return send_mail("cookie格式错误", "请检查cookie文件%s 格式是否为cookie: value" % cookie_file_name)
    return replace_invaild_first_character(cookie_all[7:])


def get_conversation_param(cookie_file_name: str, mode: str):
    headers = build_header(CONVERSATION_HEADER)
    if type(headers) == Error:
        return headers
    cookie_value = build_cookie(cookie_file_name)
    if type(cookie_value) == Error:
        return cookie_value
    if BALANCE not in cookie_value and PRECISE not in cookie_value and CREATIVE not in cookie_value:
        return send_mail("更新cookie", "此cookie仍处于上一版本，未包含变量cdxtone，需要更新")
    cookie_value = cookie_value.replace(BALANCE, mode).replace(PRECISE, mode).replace(CREATIVE, mode).replace("\n", "")
    headers["cookie"] = cookie_value
    try:
        resp = requests.get(CREATE_CHAT_URL, headers=headers)
    except:
        return Error(REQUEST_EXCEPTION, "the requests with somthing wrong to access %s, maybe the header param or cookie param wrong" % CREATE_CHAT_URL)
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

