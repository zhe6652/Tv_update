# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import time
import re
import locale
from collections import deque
locale.setlocale(locale.LC_CTYPE, 'chinese')#低下的time调用的是C里的函数，底层编码是latin-1，不改就会报错

class Tv_Update():
    def __init__(self, name, url):
        self.title = ''
        self.downloadurl = ''
        self.name =name
        self.url = url

    def save_data(self):
        file = open(self.name+'.txt', 'a')
        file.write(self.title+'\n')#加入'\n'是为了下次写入时写在下一行
        file.write(self.downloadurl+'\n')
        file.write(time.strftime('%Y年%m月%d日%H时%M分%S秒',time.localtime(time.time()))+'\n')
        file.write('\n')#\n是换行符，不是新增一行
        file.close()

    def look_data(self):
        file = open(self.name+'.txt')
        list1 = list(deque(file, 8))
        for item in list1:
            print(item, end = ' ')

    def main(self):
        print(self.name)
        print("\n")
        self.get_data()
        self.save_data()
        self.look_data()
        print("\n")

class Shield_Update(Tv_Update):
    def get_data(self):
        request = urllib.request.Request(self.url, headers= {'User-Agent':'Mozilla/5.0'})
        html = urlopen(request)
        soup = BeautifulSoup(html, 'html.parser', from_encoding='gb18030')
        for node in soup.findAll('a', text =re.compile('第[0-9]+集' )):
            self.title = node.string
            self.downloadurl =node.get('href')

class BlackList_Update1(Tv_Update):
    def get_data(self):
        request = urllib.request.Request(self.url, headers= {'User-Agent':'Mozilla/5.0'})
        html = urlopen(request)
        soup = BeautifulSoup(html, 'html.parser', from_encoding='gb18030')
        for node in soup.findAll('a', text =re.compile("罪恶黑名单.The.Blacklist.S03E[0-9]+.中英字幕.HDTVrip.1024X576.mp4")):
            self.title = node.string
            self.downloadurl =node.get('href')

class BlackList_Update2(Tv_Update):
    def get_data(self):
        request = urllib.request.Request(self.url, headers= {'User-Agent':'Mozilla/5.0'})
        html = urlopen(request)
        soup = BeautifulSoup(html, 'html.parser', from_encoding='gb18030')
        for node in soup.findAll('a', text =re.compile("\[第[0-9]+集\]")):
            self.title = node.string
            self.downloadurl =node.get('href')

if __name__ == '__main__':
    #shield= Shield_Update('神盾局特工第三季', 'http://cn163.net/archives/17616/')
    #shield.main()

    bl = BlackList_Update1("The.Blacklist.S03(美剧天堂)", 'http://www.meijutt.com/content/meiju21555.html')
    bl.main()

    bl1 = BlackList_Update2("The.Blacklist.S03(看美剧)", 'http://kanmeiju.net/detail/1919.html')
    bl1.main()

    end = input("输入ENTER结束")
