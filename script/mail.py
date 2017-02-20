# coding: utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getopt
import sys


def load_from_obj(obj):
    d = dict()
    for key in dir(obj):
        if key.isupper():
            d[key] = getattr(obj, key)
    return d


def load_config():
    cfg = load_from_obj(DefaultConfig)
    cfg.update(sysopt())
    return cfg


def msg_init(cfg):
    if cfg.get("TYPE", "text") == "text":
        msg = MIMEText(cfg.get("CONTENT").encode("utf-8"))
    else:
        msg = MIMEMultipart(cfg.get("CONTENT").encode("utf-8"))
        att = MIMEText(open(cfg.get("FILEPATH"), 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="{0}"'.format(
            cfg.get("FILENAME"))
        msg.attach(att)
    msg["Subject"] = cfg.get("SUBJECT").encode("utf-8")
    msg["From"] = cfg.get("_USER_NAME").encode("utf-8")
    msg["To"] = cfg.get("_TO")
    return msg.as_string()


def main(cfg):
    try:
        if cfg.get("SMTP_SSL"):
            s = smtplib.SMTP_SSL(cfg.get("SMTP_URL"),
                                 cfg.get("SMTP_PORT"))
        else:
            s = smtplib.SMTP()
            s.connect(cfg.get("SMTP_URL"),
                                 cfg.get("SMTP_PORT"))
        s.login(cfg.get("_USER"),
                cfg.get("_PWD"))
        msgstr = msg_init(cfg)
        s.sendmail(cfg.get("_USER"),
                   cfg.get("_TO"), msgstr)
        s.quit()
        print "Success!"
    except smtplib.SMTPException, e:
        print "Falied,%s"%e


def sysopt():
    args = sys.argv[1:]
    opts, _ = getopt.getopt(args, "n:f:ts")
    type = "text"
    filepath = None
    filename = None
    SMTP_SSL = False
    for o, v in opts:
        if o == '-t':
            type = "file"
        elif o == '-n':
            filename = v
        elif o == '-f':
            filepath = v
        elif o == '-s':
            SMTP_SSL = True
    return dict(TYPE=type, FILEPATH=filepath,
                FILENAME=filename, SMTP_SSL=SMTP_SSL)


class DefaultConfig(object):
    SMTP_URL = "smtp.qq.com"
    SMTP_PORT = 465
    _USER = "*******@qq.com"
    _USER_NAME = u"中文test"
    _PWD = "*********"
    _TO = "*******@qq.com"
    CONTENT = u"content中文"
    SUBJECT = u"Subject 中文"


if __name__ == "__main__":
    # 使用qq邮箱 ssl smtp发送邮件
    cfg = load_config()
    main(cfg)
