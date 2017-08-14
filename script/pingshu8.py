# coding: utf-8
import sys
import requests
import re
from urllib import unquote
reload(sys)
sys.setdefaultencoding("utf-8")


def getAllMp3Home(showHomePage):
    # 获取所有页数
    data = requests.get(showHomePage, timeout=2)
    pagepattern = re.compile(r'页次:\d\/(\d+)页', re.S)
    pagenums = re.findall(pagepattern, data.text)
    print data.text
    print pagenums
    print "get pages successs"
    allmp3Home = []
    for x in xrange(int(pagenums[0])):
        rereobj = re.compile(r'\d\.htm', re.S)
        Url, n = re.subn(rereobj, str(x)+".htm", showHomePage)
        data = requests.get(showHomePage, timeout=2)
        downPattern = re.compile(r'<input type=\"checkbox\" name=\"id\" value=\"(\d+)\">', re.S)
        downUrls = re.findall(downPattern, data.text)
        for x in downUrls:
            allmp3Home.append("http://www.pingshu8.com/down_{0}.html".format(x))
    print "get allmp3Home pages successs"
    return allmp3Home


def getAllDownloadUrls(Mp3Homes):
    allUrls = []
    for x in Mp3Homes:
        data = requests.get(x, timeout=2)
        urlPattern = re.compile(r'var\sdownurl\s=\"(.*?)\";', re.S)
        downUrls = re.findall(urlPattern, data.text)
        print unquote(str(downUrls[0][10:]))
        break


def main(showHomePage):
    # 获取所有音频页面
    Mp3Homes = getAllMp3Home(showHomePage)
    downloadUrls = getAllDownloadUrls(Mp3Homes)

if __name__ == "__main__":
    # 根据评书吧节目主页（例如http://www.pingshu8.com/Musiclist/mmc_215_4318_3.htm）来下载该节目所有mp3文件
    showHomePage = sys.argv[1] if len(sys.argv) > 1 else None
    if showHomePage:
        # try:
            main(showHomePage)
        # except:
        #     print "failure！！！"
    else:
        print "please input pingshu8 show HomePage"
