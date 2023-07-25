#coding: utf-8

import jieba
import pickle
from urllib.parse import quote
from urllib.parse import unquote
import ast
import numpy as np
from flask import Flask,request,render_template,redirect,url_for
from urllib.request import urlopen
import json
import appointment
import pandas as pd
from difflib import SequenceMatcher
from sklearn.linear_model import LinearRegression
model_linear_regression = LinearRegression()

hospitals_info = pd.read_csv('/Users/angeliaye/Desktop/学术_专业相关_大三/数据采集与数据集成/Final/代码与运行文件/1.csv',encoding='utf-8')
aid_center = pd.read_excel('/Users/angeliaye/Desktop/学术_专业相关_大三/数据采集与数据集成/Final/代码与运行文件/3.xls')

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

app = Flask(__name__)

@app.route('/')
def show():
   return render_template('about.html')

@app.route('/appointment')
def apm():
    if request.method == 'POST':
        illname = request.form['ill_name']
        return redirect(url_for('/appointment/'+illname))
    #team上放医院信息
    else:
        dict = []
        for i in range(12):
            info = hospitals_info.iloc[i]
            reset ={}
            reset['name'] = (info['名字'])
            reset['class'] = (info['类别'])
            reset['level'] = (info['级别'])
            reset['add'] = (info['地址'])
            reset['pic'] = info['示意图']
            dict.append(reset)
        return render_template('team.html',info = dict)

@app.route('/appointment/query',methods=["POST"])
def query_illname():
    if request.method=='POST':
        illname = request.form['ill_name']
        info = appointment.query_appointment(illname)
        if len(info)>0:
            return render_template('team-details.html', illname = illname,info = info)
        else:
            flag = 0
            for item in jieba.cut(illname):
                if item in ['上海','医院','上海市']:
                    continue
                print(item)
                info = appointment.query_appointment(item)
                if len(info) > 0:
                    flag=1
                    break
            if flag == 1:
                return render_template('team-details.html', illname=illname, info=info)
            else:
                return render_template('error.html', hosname = illname)

@app.route('/appointment/query/ill/<illname>',methods=["GET"])
def query_illname_app(illname):
    if request.method=='GET':
        illname = unquote(illname)
        #print(illname)
        info = appointment.query_appointment(illname)
        if len(info)>0:
            return render_template('team-details.html', illname = illname,info = info)
        else:
            flag = 0
            for item in jieba.cut(illname):
                if item == ['上海','医院','上海市']:
                    continue
                info = appointment.query_appointment(item)
                if len(info) > 0:
                    flag = 1
                    break
            if flag == 1:
                return render_template('team-details.html', illname=illname, info=info)
            else:
                return render_template('error.html', hosname=illname)

@app.route('/appointment/query/<hosid>',methods=["GET"])
def query_illname_hos(hosid):
    if request.method=='GET':
        illname = hospitals_info.iloc[int(hosid)]['名字']
        oname = hospitals_info.iloc[int(hosid)]['别名'].split(',')
        names = [illname]
        for item in oname:
            names.append(item)
        for item in names:
            info = appointment.query_appointment(item)
            break

        if len(info)>0:
            return render_template('team-details.html', illname = illname,info = info)
        else:
            flag = 0
            for item in jieba.cut(illname):
                if item == ['上海','医院','上海市']:
                    continue
                info = appointment.query_appointment(item)
                if len(info) > 0:
                    flag = 1
                    break
            if flag == 1:
                return render_template('team-details.html', illname=illname, info=info)
            else:
                return render_template('error.html', hosname=illname)


@app.route('/hospitals/<page>')
def hsp(page):
    i = int(page)-1
    dict = []
    total = len(hospitals_info)
    info = hospitals_info.iloc[i*20:min((i+1)*20,total)]
    if page != 8:
        index = 20
    else:
        index = 10
    for j in range(len(info)):
        reset = {}
        reset['name'] = info.iloc[j]['名字']
        reset['class'] = info.iloc[j]['类别']
        reset['level'] = info.iloc[j]['级别']
        reset['add'] = (info.iloc[j]['地址'].split('、')[0].split('，')[0].split('；')[0])
        reset['id'] = i*20+j
        dict.append(reset)

    return render_template('hos.html',info =dict,page=int(page))

@app.route('/hospitals/query',methods = ['POST'])
def show_detail():
    if request.method=='POST':
        hosname = request.form['hos_name']
        dict = []
        result = []
        for n in range(156):
            info = hospitals_info.iloc[n]
            reset = {}
            names = [info['名字']]
            try:
                if info['别名'] != '':
                    for i in info['别名'].split('、'):
                        for j in i.split('/'):
                            for k in j.split(','):
                                for o in j.split('；'):
                                    names.append(o)
            except:
                names = names

            for name in names:
                if similarity(hosname,name) > 0.7 or hosname in name or name in hosname:
                    print(name)
                    reset['name'] = info['名字']
                    reset['class'] = info['类别']
                    reset['level'] = info['级别']
                    reset['add'] = info['地址'].split('、')[0].split('，')[0].split('；')[0]
                    reset['lat'] = info['纬度']
                    reset['lng'] = info['经度']
                    reset['hdcw'] = info['床位']
                    reset['pic'] = info['示意图']
                    reset['id'] = n
                    if info['别名'] !=np.NAN :
                        reset['oname'] = info['别名'].replace(',','，')
                    else:
                        reset['oname'] = ''
                    if info['网站'] != np.NAN:
                        reset['site'] = info['网站']
                    else:
                        reset['site'] = ''

                    result.append(reset)
                    break
        if len(result)>0:
            return render_template('hos-details.html',info =result,hosname=hosname)
        else:
            return render_template('error.html', info=result, hosname=hosname)

@app.route('/hospitals/detail/<hosid>')
def show_detail_single(hosid):
    if request.method=='GET':
        info = hospitals_info.iloc[int(hosid)]
        reset = {}
        result = []
        reset['name'] = info['名字']
        reset['class'] = info['类别']
        reset['level'] = info['级别']
        reset['add'] = info['地址'].split('、')[0].split('，')[0].split('；')[0]
        reset['lat'] = info['纬度']
        reset['lng'] = info['经度']
        reset['hdcw'] = info['床位']
        reset['pic'] = info['示意图']
        reset['id'] = int(hosid)
        if info['别名'] !=np.NAN :
            reset['oname'] = info['别名']
        else:
            reset['oname'] = ''
        if info['网站'] != np.NAN:
            reset['site'] = info['网站']
        else:
            reset['site'] = ''

        result.append(reset)

        return render_template('hos-details.html',info =result,hosname=reset['name'])

@app.route('/hospitals/query/loc/<hosid>',methods = ['GET'])
def showmap(hosid):
    if request.method=='GET':
        i = int(hosid)
        loc = {}
        loc['id'] = i
        loc['lat'] = hospitals_info.iloc[i]['纬度']
        loc['lng'] = hospitals_info.iloc[i]['经度']
        loc['name'] = hospitals_info.iloc[i]['名字']
        loc['add'] = hospitals_info.iloc[i]['地址'].split('、')[0].split('，')[0].split('；')[0]

        return render_template('map.html',loc = loc)

@app.route('/hospitals/query/loc/detail/<hosid>',methods = ['POST'])
def showmaproute(hosid):
    if request.method=='POST':
        addname = request.form['add_name']
        i = int(hosid)
        loc = {}
        loc['lat'] = hospitals_info.iloc[i]['纬度']
        loc['lng'] = hospitals_info.iloc[i]['经度']
        loc['name'] = hospitals_info.iloc[i]['名字']
        loc['add'] = hospitals_info.iloc[i]['地址'].split('、')[0].split('，')[0].split('；')[0]
        try:
            loc['add'] = hospitals_info.iloc[i]['地址'].split('、')[0].split('，')[0].split('；')[0]
            url = 'http://api.map.baidu.com/place/v2/search?query=' + quote(addname) + '&region=' + quote(
                '上海市') + '&output=json&ak=FzhYhckmA1ARv3TiclXn9EykM7dgL8RZ&scope=1&page_size=5&page_num=0'
            html = urlopen(url)
            info = json.loads(s=html.read())
            loc['curname'] = addname
            for result in info['results']:
                loc['curlat'] = result['location']['lat']
                loc['curlng'] = result['location']['lng']
                break
            #print(addname,loc['lat'],loc['lng'],loc['curlat'],loc['curlng'])
            return render_template('map_route.html',loc = loc)
        except:
            return render_template('error.html', hosname='该定位路线规划')


@app.route('/aid/query/loc/<aidid>',methods = ['GET'])
def showmap_aid(aidid):
    if request.method=='GET':
        i = int(aidid)
        loc = {}
        loc['name'] = aid_center.iloc[i]['机构名称']
        loc['add'] = aid_center.iloc[i]['地  址'].split('、')[0].split('，')[0].split('；')[0]
        loc['id'] = i
        url = 'http://api.map.baidu.com/place/v2/search?query=' + quote(loc['add']) + '&region=' + quote(
            '上海市') + '&output=json&ak=FzhYhckmA1ARv3TiclXn9EykM7dgL8RZ&scope=1&page_size=5&page_num=0'
        html = urlopen(url)
        info = json.loads(s=html.read())
        for result in info['results']:
            loc['lat'] = result['location']['lat']
            loc['lng'] = result['location']['lng']
            break

        return render_template('map2.html',loc = loc)

@app.route('/aid/query/loc/detail/<aidid>',methods = ['POST'])
def showmaproute_aid(aidid):
    if request.method=='POST':
        i = int(aidid)
        loc = {}
        loc['name'] = aid_center.iloc[i]['机构名称']
        addname = request.form['add_name']
        url = 'http://api.map.baidu.com/place/v2/search?query=' + quote(loc['name']) + '&region=' + quote(
            '上海市') + '&output=json&ak=FzhYhckmA1ARv3TiclXn9EykM7dgL8RZ&scope=1&page_size=5&page_num=0'
        html = urlopen(url)
        info = json.loads(s=html.read())
        for result in info['results']:
            loc['lat'] = result['location']['lat']
            loc['lng'] = result['location']['lng']
            break
        loc['curname'] = addname
        loc['add'] = aid_center.iloc[i]['地  址'].split('、')[0].split('，')[0].split('；')[0]
        url = 'http://api.map.baidu.com/place/v2/search?query=' + quote(addname) + '&region=' + quote(
            '上海市') + '&output=json&ak=FzhYhckmA1ARv3TiclXn9EykM7dgL8RZ&scope=1&page_size=5&page_num=0'
        html = urlopen(url)
        info = json.loads(s=html.read())
        print(addname,loc['lat'],loc['lat'])
        for result in info['results']:
            loc['curlat'] = result['location']['lat']
            loc['curlng'] = result['location']['lng']
            break
        #print(addname,loc['lat'],loc['lng'],loc['curlat'],loc['curlng'])
        return render_template('map_route.html',loc = loc)


@app.route('/hospitals/aid')
def aid():
    info = aid_center
    dict = []
    for j in range(14):
        reset = {}
        reset['name'] = info.iloc[j]['机构名称']
        reset['class'] = info.iloc[j]['电话']
        reset['level'] = info.iloc[j]['邮编']
        reset['add'] = info.iloc[j]['地  址'].split('、')[0].split('，')[0].split('；')[0]
        reset['id'] = j
        dict.append(reset)
    return render_template('aid.html',info =dict)

@app.route('/illname')
def illquery():
    return render_template('ill.html')

@app.route('/illtp')
def illtp():
    return redirect('http://localhost:7474/browser/')

@app.route('/illname/query',methods=['POST'])
def illdetail():
    if request.method=='POST':
        result = []
        illname = request.form['ill_name']
        flag = 0
        f = open('w2v.model', 'rb')  # 注意此处model是rb
        s = f.read()
        model = pickle.loads(s)
        for i in range(len(illness)):
            score = 0
            reset = {}
            name = illness.iloc[i]['名称']
            if name in illname or illname in name:
                reset['score'] = 1000
                reset['name'] = name
                reset['bw'] = illness.iloc[i]['发病部位']
                reset['ks'] = illness.iloc[i]['就诊科室'].replace(',','，')
                reset['intro'] = illness.iloc[i]['概述']
                reset['yy'] = illness.iloc[i]['疾病用药']
                reset['firstdept'] = illness.iloc[i]['就诊科室'].split(',')[0]
                result.append(reset)
            elif similarity(illname,name) > 0.5:
                reset['score'] = 100
                reset['name'] = name
                reset['bw'] = illness.iloc[i]['发病部位']
                reset['ks'] = illness.iloc[i]['就诊科室'].replace(',','，')
                reset['intro'] = illness.iloc[i]['概述']
                reset['yy'] = illness.iloc[i]['疾病用药']
                reset['firstdept'] = illness.iloc[i]['就诊科室'].split(',')[0]
                result.append(reset)
            else:
                num = 0
                for item in jieba.cut(illname):
                   for item2 in jieba.cut(name):
                       num += 1
                       try:
                           score+= model.similarity(item,item2)
                       except:
                           score += similarity(item,item2)
                if score> 0.5*num:
                    reset['name'] = name
                    reset['bw'] = illness.iloc[i]['发病部位']
                    reset['ks'] = illness.iloc[i]['就诊科室'].replace(',','，')
                    reset['intro'] = illness.iloc[i]['概述']
                    reset['yy'] = illness.iloc[i]['疾病用药']
                    reset['firstdept'] = illness.iloc[i]['就诊科室'].split(',')[0]
                    result.append(reset)
                    reset['score'] = score
        result_ = []
        for i in range(len(result)):
            max = result[i]['score']
            loc = i
            for j in range(i,len(result)):
                if result[j]['score'] > max:
                    loc = j
            if result[loc] not in result_:
                result_.append(result[loc])
        if len(result) > 0:
            return render_template('ill-details.html',info = result_,illname=illname)
        else:
            return render_template('error.html',hosname=illname)


if __name__ == '__main__':
    for i in list(hospitals_info.columns):
        if i in ['别名','地址','床位','网站','示意图']:
            hospitals_info[i].fillna('',inplace = True)
    illness = pd.read_csv('/Users/angeliaye/Desktop/学术_专业相关_大三/数据采集与数据集成/Final/代码与运行文件/illness.csv').fillna('暂无数据')
    app.run(port=5000)
