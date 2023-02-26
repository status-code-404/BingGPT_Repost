from create_conversation import get_conversation_param, build_header, build_cookie
from error import *
from random import random
from base64 import b64encode
from mail_remind import send_mail
import re
import websocket
import emoji
from datetime import datetime
import json
import  time
from template import *



def get_time_stamp():
    time_str = str(datetime.now())
    return  time_str[:10] + "T" + time_str[11:19] + "+08:00"

def build_wss_secret_key():
    key = b64encode(str(random()).encode("utf8")).decode()
    return key

def build_wss_request_data(traceId, innovationId, conversationId, clientId, conversationSignature, question):
    try:
        request_data = json.loads(ARGUMENT_TEMPLATE)
    except:
        return Error(PARAM_JSON_ERROR, "Argunment_template cant translate into json")
    request_data["arguments"][0]["traceId"] = traceId
    request_data["arguments"][0]["isStartOfSession"] = innovationId == 0
    request_data["arguments"][0]["conversationSignature"] = conversationSignature
    request_data["arguments"][0]["conversationId"] = conversationId
    request_data["arguments"][0]["participant"] = {"id":clientId}
    request_data["arguments"][0]["message"]["text"] = question
    request_data["arguments"][0]["message"]["timestamp"] = get_time_stamp()
    request_data["invocationId"] = str(innovationId)

    return json.dumps(request_data) + END_SET


class Conversation:
    def __init__(self, cookie_file_name):
        self.invocation_id = 0
        self.request_param = None
        self.last_use_time = None
        self.wss_header = None
        self.wss_connect = None
        self.cookie_name = cookie_file_name
        self.last_question_time = time.time()

    def can_use(self):
        if self.request_param is None or self.request_param.get("conversationId") is None:
            return False
        return True

    def init(self, cookie_file_name):
        self.invocation_id = 0
        self.request_param = get_conversation_param(cookie_file_name)
        if type(self.request_param) == Error:
            return self.request_param
        if self.request_param is None:
            return Error(COOKIE_REFRESH, "cookie/headers need to be refresh, already send the mail")
        self.wss_header = build_header(CHAT_HEADER)
        if type(self.wss_header) == Error:
            return self.wss_header

    def init_handshake(self):
        self.wss_connect.send('''{"protocol":"json","version":1}''' + END_SET)
        hand_shake = self.wss_connect.recv()
        if not(hand_shake == "{}" + END_SET):
            return Error(WSS_HANDSHAKE_ERROR, "handshake message wrong")

    def create_connection(self):
        self.wss_connect = websocket.WebSocket()
        self.wss_connect.connect(CHAT_URL, header=self.wss_header)
        try:
            self.wss_connect.connect(CHAT_URL, header=self.wss_header)
        except:
            return Error(WSS_CONNECT_ERROR, "something wrong when connect to %s" % CHAT_URL)
        return self.init_handshake()

    def get_answer(self, question):
        error = self.create_connection()
        if error is not None:
            return None, error
        self.wss_connect.send(WAKE_CONNECTION)
        request_data= build_wss_request_data(traceId=self.request_param["traceId"], conversationId=self.request_param["conversationId"],
                                             clientId=self.request_param["clientId"], conversationSignature= self.request_param["conversationSignature"],
                                             question= question, innovationId= self.invocation_id)
        if type(request_data) == Error:
            return None, request_data
        self.wss_connect.send(request_data)
        self.invocation_id += 1
        last_max_answer = ""
        max_answer_len = 0
        # 这一段的逻辑算有些混乱的
        connect_maintain = 0
        while 1:
            if connect_maintain >= 13:
                connect_maintain = 0
                self.wss_connect.send(WAKE_CONNECTION)
            answer = self.wss_connect.recv()
            if answer == WAKE_CONNECTION:
                continue
            answer = answer[:-1]
            if '''{"type":2,''' in answer:
                break
            try:
                answer_json = json.loads(answer)
            except:
                self.wss_connect.close()
                return last_max_answer, Error(PARAM_JSON_ERROR, "the receive from wss sydeny cant trans to json")

            if answer_json.get("type") == 2:
                break
            elif answer_json.get("type") != 1 :
                continue

            try:
                if len(answer_json["arguments"][0]["messages"][0]["text"]) >= max_answer_len:
                    last_max_answer = answer_json["arguments"][0]["messages"][0]["text"]
                    max_answer_len = len(last_max_answer)
            except:
                continue

        self.wss_connect.close()
        return last_max_answer, None

    def ask(self, question):
        now_time = time.time()
        if self.invocation_id >= ROUND_LIMIT or now_question_time - self.last_question_time >= ROUND_LIMIT_TIME:
            error = self.init(self.cookie_name)
            if error is not None:
                return None, error
        self.last_question_time = now_time
        return self.get_answer(question)

CONVERSATIONS = {}


def get_conversation(cookie_file_name:str):
    global CONVERSATIONS
    error = None
    if CONVERSATIONS.get(cookie_file_name) is None:
        CONVERSATIONS[cookie_file_name] = Conversation(cookie_file_name)
    if not CONVERSATIONS[cookie_file_name].can_use():
        error = CONVERSATIONS[cookie_file_name].init(cookie_file_name)
    if error is not None:
        return error
    return CONVERSATIONS[cookie_file_name]

def conversations_clear():
    global CONVERSATIONS
    CONVERSATIONS.clear()

def question_interface(cookie_file:str, question: str):
    conversation = get_conversation(cookie_file)
    if type(conversation) == Error:
        return conversation
    answer_raw, error = conversation.ask(question)
    if answer_raw is None or len(answer_raw) == 0:
        conversations_clear()
        return send_mail("回复为空", "尝试更新cookie 或查看今日提问次数是否到达上限")
    # answer_raw = answer_raw.replace("\n","")
    if answer_raw is not None and len(answer_raw) != 0:
        return re.sub("\[\^([0-9]*)\^\]", "", emoji.replace_emoji(answer_raw, replace=""))
    else:
        return error

#test



