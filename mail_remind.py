import smtplib
from email.mime.text import MIMEText
from error import *

# 自己填写
MAIL_CONF = {
    "self_mail": "",
    "self_smtp_key": "",
    "self_pop_key": "",    # 在本项目暂时不用pop3
    "mail_type": {
        "qq": "smtp.qq.com",
        "126": "smtp.126.com",
    },
    "receiver": ""
}


def send_mail(subject: str, text: str):
    try:
        handle = smtplib.SMTP(MAIL_CONF["mail_type"]["qq"])
        handle.login(MAIL_CONF["self_mail"], MAIL_CONF["self_smtp_key"])
    except:
        return Error(MAIL_ACCOUNT_ERROR, "%s mail cant login, checkout account and key" % MAIL_CONF["self_mail"])
    email = MIMEText(text)
    email["Subject"] = subject
    email["from"] = MAIL_CONF["self_mail"]
    email["to"] = MAIL_CONF["receiver"]
    try:
        handle.sendmail(MAIL_CONF["self_mail"], MAIL_CONF["receiver"], email.as_string())
        handle.close()
        return
    except:
        return Error(MAIL_USE_ERROR, "cant send mail, should checkout mail receiver is right or other thing happen")

