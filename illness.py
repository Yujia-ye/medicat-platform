# -*- coding: utf-8 -*-
from urllib.request import urlopen
from urllib import request
from urllib.parse import urljoin,quote
from bs4 import BeautifulSoup
import pandas as pd
import ssl
import sys
import importlib
import string

letter = []
ills = []
ill_book = []


# 爬取首字母链接
def get_letter_link(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, features="lxml")
    a = bsObj.find("div",{"class":"letter-title hd"}).findAll("a")
    for i in a:
        ill = i['href']
        new = urljoin(url, ill)
        letter.append(new)


# 爬取所有病症链接
def get_ill_link(url, page):
    try:
        print("第%d页"% page)
        html = urlopen(url)
        bsObj = BeautifulSoup(html, features="lxml")
        names = bsObj.find("div", {"class": "list-cont"}).findAll("dd")
        for name in names:
            ill = name.find("a")["href"]
            new = urljoin(url, ill)
            ills.append(new)
            print(new)
        a = bsObj.find("div",{"class":"list-page"}).find("span", {"class":"l_pa nextv"}).find("a")["href"]
        link = urljoin(url,a)
        print(link)
        get_ill_link(link,page+1)
    except:
        print("该字母共%d页" % page)


def get_ill_information(url):
    try:
        dic = {}
        html = urlopen(url)
        bsObj = BeautifulSoup(html, features="lxml")
        a = bsObj.find("div", {"class": "del-wrap1"}).find("b")
        b = a.text.replace(u'\r\n', u'')
        b = b.replace(' ', '')
        b = b.replace('\n', '')
        dic['名称'] = b
        a = bsObj.find("div", {"class": "del-wrap1"}).findAll("p")
        for i in a:
            name = i.findAll("a")
            l = []
            for n in name:
                l.append(n.text)
            dic[i.find("span").text[:-1]] = l
        a = bsObj.find("div", {"class": "del-cont"}).find("p")
        b = a.text.replace(u'\u3000', u'')
        dic['概述'] = b
        print(dic)
        ill_book.append(dic)
    except:
        print("该网页已被移除")


url = 'https://jbk.99.com.cn/'
get_letter_link(url)
print(letter)
for i in range(len(letter)):
    get_ill_link(letter[i], 1)
for i in range(len(ills)):
    get_ill_information(ills[i])

end = pd.DataFrame(ill_book)
end.to_csv('ill_book.csv',index=False)