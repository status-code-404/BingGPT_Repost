class Error:
    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = detail

    def get_code(self):
        return self.code

    def __str__(self):
        return "Error Code : %s,  Details :  %s" % (self.code, self.detail)

    def dict(self):
        return {"response_code": self.code, "response_text": self.detail}


REQUEST_EXCEPTION = "0"
PARAM_JSON_ERROR = "1"
PARAM_ERROR = "2"
MAIL_ACCOUNT_ERROR = "3"
MAIL_USE_ERROR = "4"
COOKIE_REFRESH = "5"
WSS_CONNECT_ERROR = "6"
GET_EVENT_ID = "7"
WSS_HANDSHAKE_ERROR = "7"
WSS_RESPONSE_FORMAT_ERROR = "8"
FILE_OPEN_ERROR = "9"
KEY_FORMAT_WRONG = "10"
NO_QUESTION = "11"
NO_PROBLEM = "12"
EXCEPTION_OCCUR = "13"
