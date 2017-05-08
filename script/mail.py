# coding: utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getopt
import sys
import random
from email.header import Header
import os.path
reload(sys)
sys.setdefaultencoding("utf-8")


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
        msg = MIMEText(cfg.get("CONTENT"), _charset='utf-8')
        msg["Accept-Language"] = "zh-CN"
        msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    else:
        # add file
        msg = MIMEMultipart()
        for onefile in cfg.get("FILEPATH"):
            filename = os.path.basename(onefile)
            att = MIMEText(open(onefile, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="{0}"'.format(filename)
            msg.attach(att)
        # add content
        textmsg = MIMEText(cfg.get("CONTENT"), _charset='utf-8')
        textmsg["Accept-Language"] = "zh-CN"
        textmsg["Accept-Charset"] = "ISO-8859-1,utf-8"
        msg.attach(textmsg)
    subject = cfg.get("SUBJECT")
    if not isinstance(subject, unicode):
        subject = unicode(subject)
    msg["Subject"] = subject
    msg["From"] = cfg.get("_USER_NAME")
    msg["To"] = ",".join(cfg.get("_TO"))
    return msg.as_string()


def main(cfg):
    try:
        if cfg.get("SMTP_SSL"):
            s = smtplib.SMTP()
            s.connect(cfg.get("SMTP_URL"),
                      cfg.get("SMTP_PORT"))
            s.starttls()
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
    filepath = []
    SMTP_SSL = False
    for o, v in opts:
        if o == '-t':
            type = "file"
        elif o == '-f':
            filepath.append(v)
        elif o == '-s':
            SMTP_SSL = True
    return dict(TYPE=type, FILEPATH=filepath, SMTP_SSL=SMTP_SSL)


class DefaultConfig(object):
    SMTP_URL = "smtp.qq.com"
    SMTP_PORT = 25
    _USER = "test**@qq.com"
    _USER_NAME = "{0}<1test**@qq.com>".format(Header('运维','utf-8'))
    _PWD = "test**"
    _TO = ["test**@163.com", "test**@qq.com", "test**@gamil.com"]
    CONTENT = "content中文{0}".format(random.randint(0, 20))
    SUBJECT = "Subject 中文{0}".format(random.randint(0, 20))


if __name__ == "__main__":
    # 使用qq邮箱 ssl smtp发送邮件
    """
    20170225 Tips:
        1 _USER must as similar as _USER_NAME,
        because many email servers will return content rejected if zhese not sumilar
        2 Deal some probles about Chinese
    20170508 Tips:
        1 get filenam by filepath
        2 can send more files
    """
    cfg = load_config()
    main(cfg)
