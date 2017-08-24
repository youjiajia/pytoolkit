# coding: utf-8
import sys
import os
import getopt
import re
import qiniu.config
from qiniu import Auth, put_file, etag, urlsafe_base64_encode


class DefaultConfig(object):
    ACCESS_KEY = 'your key'
    SCRET_KEY = 'your scret key'
    BUCKET_NAME = 'your bucket name'
    DIRNAME = 'page'
    FILE_PATTERN = '\.py|.gitignore|README.md'
    DIR_PATTERN = 'node_modules|.git'

class ProgressBar:
    def __init__(self, count=0, total=0, width=50):
        self.count = count
        self.total = total
        self.width = width

    def move(self):
        self.count += 1
        sys.stdout.flush()
        progress = self.width * self.count / self.total
        sys.stdout.write("{0:3}/{1}   ".format(self.count, self.total))
        sys.stdout.write('#' * progress + '-' * (self.width - progress) + '\r')
        if progress == self.width:
            sys.stdout.write('\n')
        sys.stdout.flush()


def sysopt():
    args = sys.argv[1:]
    opts, _ = getopt.getopt(args, "a:s:b:d:", ["filep=","dirp="])
    data = dict()
    for o, v in opts:
        if o == '-a':
            data["ACCESS_KEY"] = v
        if o == '-s':
            data["SCRET_KEY"] = v
        if o == '-b':
            data["BUCKET_NAME"] = v
        if o == '-d':
            data["DIRNAME"] = v
        if o == '--filep':
            data["FILE_PATTERN"] = v
        if o == '--dirp':
            data["DIR_PATTERN"] = v
    return data


def load_from_obj(obj):
    d = dict()
    for key in dir(obj):
        if key.isupper():
            d[key] = getattr(obj, key)
    return d


def loadConfig():
    cfg = load_from_obj(DefaultConfig)
    cfg.update(sysopt())
    return cfg


def listdir(path, list_name, base, dirpattern, filepattern):  #传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            if len(re.findall(dirpattern, file))<=0:
                listdir(file_path, list_name, base, dirpattern, filepattern)
        else:
            if len(re.findall(filepattern, file))<=0:
                list_name.append({
                    "oppPath":os.path.relpath(file_path, base),
                    "Path": file_path
                    })


def pushData(q, bucket_name, cfg, data):
    #上传到七牛后保存的文件名
    key = os.path.join(cfg["DIRNAME"], data["oppPath"]).replace('\\', '/')

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    #要上传文件的本地路径
    localfile = data["Path"]
    put_file(token, key, localfile)

if __name__ == "__main__":
    # 上传七牛云工具
    cfg = loadConfig()
    base = os.path.dirname(os.path.realpath(__file__))
    allfiles = []
    dirpattern = re.compile(cfg["DIR_PATTERN"], re.S)
    filepattern = re.compile(cfg["FILE_PATTERN"], re.S)
    print "scanning files"
    listdir(base, allfiles, base, dirpattern, filepattern)
    print "scanning files success"
    # 构建鉴权对象
    q = Auth(cfg["ACCESS_KEY"], cfg["SCRET_KEY"])
    #要上传的空间
    bucket_name = cfg["BUCKET_NAME"]
    bar = ProgressBar(total=len(allfiles))
    for data in allfiles:
        bar.move()
        pushData(q, bucket_name, cfg, data)
