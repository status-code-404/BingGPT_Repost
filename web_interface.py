from error import *
from converse import question_interface, conversations_clear
from flask import Flask, abort, request
from gevent import pywsgi
from template import DEFAULT_MODE, REQUEST_DICT
from error import *
import random
from mail_remind import send_mail

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def generate_random_str(randomlength: int):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


# 不想搞login那么复杂了，带个key过来访问吧
def key_trans_file(key: str):
    if key[0] not in '56789':
        return Error(KEY_FORMAT_WRONG, "%s is not a key" % key)
    key_offset = eval(key[0])
    key_len = len(key) - 1
    if key_len % key_offset != 0:
        return Error(KEY_FORMAT_WRONG, "%s is not a key" % key)
    file_name = ""
    for i in range(key_len // key_offset):
        file_name += key[(1 + i * key_offset): (1 + (i + 1) * key_offset)][key_offset // 2]
    return file_name


def file_name_trans_key(file_name: str):
    key = ""
    key_offset = random.randint(5, 9)
    key += str(key_offset)
    for i in file_name:
        random_str = generate_random_str(key_offset)
        key = key + random_str[:key_offset // 2] + i + random_str[key_offset // 2 + 1:]
    return key


@app.route("/")
def hello():
    return "Hello"


@app.route("/key/<string:key>", methods=["GET"])
def web_question(key):
    file_name = key_trans_file(key)
    if type(file_name) == Error:
        abort(401)

    question = request.args.get("question")
    if question is None or len(question) == 0:
        return {"response_text": "", "response_code": NO_QUESTION}
    answer_type = request.args.get("type")
    if answer_type is None or answer_type not in REQUEST_DICT:
        answer_type = DEFAULT_MODE
    else:
        answer_type = REQUEST_DICT[answer_type]
    try:
        response = question_interface(file_name, question, mode=answer_type)
        if response is None:
            return Error(RESPONSE_NONE, "cookie need to be refresh or today question come to limit").dict()
        if type(response) == Error:
            if response.get_code() == FILE_OPEN_ERROR:
                abort(401)
            return response.dict()
        return {"response_text": response, "response_code": NO_PROBLEM}
    except:
        #    就算这里出现error也没能力处理
        send_mail("Exception occur", "运行中出现了问题，请及时查看")
        conversations_clear()
        return {"response_text": "", "response_code": EXCEPTION_OCCUR}


if __name__ == '__main__':
    # app.run(port=7000, debug=False)
    server = pywsgi.WSGIServer(('0.0.0.0', 9990), app)
    server.serve_forever()
