# coding: utf-8
import sys
import os
import requests
import re
import time
if 'threading' in sys.modules:
    del sys.modules['threading']
import gevent
from gevent import monkey; monkey.patch_all()
from urllib import unquote, quote
reload(sys)
sys.setdefaultencoding("utf-8")


class ProgressBar:
    def __init__(self, count=0, total=0, width=50):
        self.count = count
        self.total = total
        self.width = width

    def move(self):
        self.count += 1
        sys.stdout.write(" " * (self.width + 9))
        sys.stdout.flush()
        progress = self.width * self.count / self.total
        sys.stdout.write("{0:3}/{1}   ".format(self.count, self.total))
        sys.stdout.write('#' * progress + '-' * (self.width - progress) + '\r')
        if progress == self.width:
            sys.stdout.write('\n')
        sys.stdout.flush()


def getAllMp3Home(showHomePage):
    # 获取所有页数
    data = requests.get(showHomePage)
    pagepattern = re.compile(r'页次:\d\/(\d+)页', re.S)
    pagenums = re.findall(pagepattern, data.content.decode('gb2312', 'replace').encode('utf-8', 'replace'))
    # print data.content
    print "get pages successs"
    allmp3Home = {}
    for x in xrange(1, int(pagenums[0])+1):
        rereobj = re.compile(r'\d\.htm', re.S)
        Url, n = re.subn(rereobj, str(x)+".htm", showHomePage)
        data = requests.get(Url)
        downPattern = re.compile(r'<input type=\"checkbox\" name=\"id\" value=\"(\d+)\">', re.S)
        downUrls = re.findall(downPattern, data.text)
        allmp3Home[Url] = []
        for x in downUrls:
            allmp3Home[Url].append("http://www.pingshu8.com/down_{0}.html".format(x))
    print "get allmp3Home pages successs"
    return allmp3Home


def getAllDownloadUrls(Mp3Homes):
    allUrls = []
    def f(i, x):
        data = requests.get(x)
        urlPattern = re.compile(r'var\sdownurl\s=\"(.*?)\";', re.S)
        downUrls = re.findall(urlPattern, data.text)
        uripattern = unquote(unquote(downUrls[0][10:]))
        uri = uripattern[2:len(uripattern) - 5]
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
                   "Cache-Control": "max-age=0",
                   "Connection": "keep-alive",
                   "Host": "www.pingshu8.com",
                   "Referer": i,
                   "Upgrade-Insecure-Requests": "1",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
        data = requests.get("http://www.pingshu8.com"+uri, headers=headers, allow_redirects=False)
        allUrls.append(data.headers['Location'])
    workers = []
    for i in Mp3Homes.keys():
        for x in Mp3Homes[i]:
            workers.append(gevent.spawn(f, i, x))
    gevent.joinall(workers)
    print "get allmp3 Urls successs"
    return allUrls


def downloadMp3(downloadUrls):
    base = os.path.dirname(os.path.realpath(__file__))
    vod_dir = os.path.join(base, "download")
    if not os.path.exists(vod_dir):
        os.makedirs(vod_dir)
    bar = ProgressBar(total=len(downloadUrls))
    failedlist = []
    def f(x):
        try:
            data = requests.get(quote(x).replace("%3A", ":"), stream=True)
            filename = os.path.join(vod_dir, x.split("/")[-1])
            f = open(filename, 'wb')
            for chunk in data.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
            f.close()
            bar.move()
        except:
            print "{0} download failed".format(x)
            failedlist.append(x)
    workers = []
    for x in downloadUrls:
        f(x)
        # workers.append(gevent.spawn(f, x))
    # gevent.joinall(workers)
    print "all failedlist is {0}".fomrat(failedlist)


def main(showHomePage):
    # 获取所有音频页面
    Mp3Homes = getAllMp3Home(showHomePage)
    downloadUrls = getAllDownloadUrls(Mp3Homes)
    downloadMp3(downloadUrls)

if __name__ == "__main__":
    # 根据评书吧节目主页（例如http://www.pingshu8.com/Musiclist/mmc_215_4318_3.htm）来下载该节目所有mp3文件
    showHomePage = sys.argv[1] if len(sys.argv) > 1 else None
    if showHomePage:
        firsttime = time.time()
        try:
            main(showHomePage)
        except:
            print "failure！！！"
        alltime = int(time.time() - firsttime)
        m, s = divmod(alltime, 60)
        h, m = divmod(m, 60)
        print "total use %d hours %02d minutes %02d seconds" % (h, m, s)
    else:
        print "please input pingshu8 show HomePage"
