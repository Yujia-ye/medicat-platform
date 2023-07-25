
import requests
import json

import ast


def query_appointment(illname):
    url_ = 'https://www.91985.com/users/api/search/complexSearch.do'
    headers_ = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '55',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=F97F9484E42FBD7E020C720E0D4FD141; UM_distinctid=176f68d127c846-03d457d097e172-16386152-13c680-176f68d127d54; Hm_lvt_02e4feedc6daae9ac4597bf35d13b5b5=1610606343,1610606450,1610626694,1610629753; CNZZDATA1255855036=1165496235-1610454233-https%253A%252F%252Fwww.91985.com%252F%7C1610633250; Hm_lpvt_02e4feedc6daae9ac4597bf35d13b5b5=1610634033',
        'Host': 'www.91985.com',
        'Origin': 'https://www.91985.com',
        'Referer': 'https://www.91985.com/users/portal/searchByDisease.do',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data_ = {
        'keyword': illname,
        'hosName': '',
        'diseaseName': '',
        'page': '1',
        'pageSize': '10'}
    req = requests.post(url=url_, data=data_, headers=headers_)
    info = json.loads(s=req.text)
    docs_info = []
    for item in info['attach']:
        doc = {}
        doc['deptName'] = item['deptName']
        doc['level'] = item['level']
        doc['expert'] = item['expert']
        doc['name'] = item['name']
        doc['hospitalName'] = item['hospitalName']
        try:
            doc['picture'] = item['picture']
        except:
            doc['picture'] = ''
        doc['schedule'] = []
        try:
            for day in ast.literal_eval(item['scheInfoJson']):
                sin = {}
                sin['Date'] = day['schDate']
                sin['weekday'] = day['weekDay']
                sin['fee'] = day['firstFee']
                try:
                    sin['startTime'] = day['startTime']
                    sin['endTime'] = day['endTime']
                except:
                    sin['startTime'] = ''
                    sin['endTime'] = ''
                sin['diagType'] = day['diagType']
                sin['site'] = 'https://www.91985.com/users/portal/appoint.do?scheInfoId='+day['id']
                doc['schedule'].append(sin)
        except:
            continue
        docs_info.append(doc)
    return docs_info

if __name__ == '__main__':
    print(query_appointment('感冒'))
