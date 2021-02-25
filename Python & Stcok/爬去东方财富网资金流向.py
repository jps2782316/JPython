#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:47:12 2021

@author: jps
"""

import json
import requests



#生成请求: https://curl.trillworks.com/


cookies = {
    'st_si': '85530502308782',
    'waptgshowtime': '2021118',
    'qgqp_b_id': 'd8564ccdf4a0314ea365d2f2e7f7e789',
    'cowCookie': 'true',
    'intellpositionT': '991px',
    'st_pvi': '21997121383650',
    'st_sp': '2020-10-14%2015%3A59%3A16',
    'st_inirUrl': 'https%3A%2F%2Fwww.google.com%2F',
    'st_sn': '9',
    'st_psi': '20210118163333452-111000300841-4598232959',
    'intellpositionL': '87px',
    'cowminicookie': 'true',
    'st_asi': '20210118162624887-113300300813-7981102258-dfcfwsy_dfcfwxsy_dcxn_djgb-1',
}

headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
    'Referer': 'http://data.eastmoney.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

params = (
    #('cb', 'jQuery11230975747479351698_1610958384763'),
    ('fid', 'f267'),
    ('po', '1'),
    ('pz', '50'),
    ('pn', '1'),
    ('np', '1'),
    ('fltt', '2'),
    ('invt', '2'),
    ('ut', 'b2884a393a59ad64002292a3e90d46a5'),
    ('fs', 'm:0+t:6+f:/u00212,m:0+t:13+f:/u00212,m:0+t:80+f:/u00212,m:1+t:2+f:/u00212,m:1+t:23+f:/u00212,m:0+t:7+f:/u00212,m:1+t:3+f:/u00212'),
    ('fields', 'f12,f14,f2,f127,f267,f268,f184,f269,f165,f175,f270,f271,f272,f273,f274,f275,f276,f257,f258,f124'),
)

#报错: InvalidSchema: No connection adapters were found for。原因:https://curl.trillworks.com/ 生成Python requests时，http前面多了个$符号，去掉就行了。
#response = requests.get('$http://push2.eastmoney.com/api/qt/clist/get', headers=headers, params=params, cookies=cookies, verify=False)
response = requests.get('http://push2.eastmoney.com/api/qt/clist/get', headers=headers, params=params, cookies=cookies, verify=False)


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
#response = requests.get('$http://push2.eastmoney.com/api/qt/clist/get?cb=jQuery11230975747479351698_1610958384763&fid=f267&po=0&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A0%2Bt%3A6%2Bf%3A\u00212%2Cm%3A0%2Bt%3A13%2Bf%3A\u00212%2Cm%3A0%2Bt%3A80%2Bf%3A\u00212%2Cm%3A1%2Bt%3A2%2Bf%3A\u00212%2Cm%3A1%2Bt%3A23%2Bf%3A\u00212%2Cm%3A0%2Bt%3A7%2Bf%3A\u00212%2Cm%3A1%2Bt%3A3%2Bf%3A\u00212&fields=f12%2Cf14%2Cf2%2Cf127%2Cf267%2Cf268%2Cf269%2Cf270%2Cf271%2Cf272%2Cf273%2Cf274%2Cf275%2Cf276%2Cf257%2Cf258%2Cf124', headers=headers, cookies=cookies, verify=False)

print(response)



#2. 数据清洗
#打印发现前面携带了jQuery11230975747479351698_1610958384763(这么一个东西，而非一个单纯的字典
#只要把请求的params里的cb字段去掉，就可以得到一个单纯的字典
print(response.text)
print(type(response.text)) #<class 'str'>

dic_resp = json.loads(response.text)
print(type(dic_resp)) #<class 'dict'>


#拿到数据之后，经过自己的逻辑运算，一些投资思路，满足要求的就放进来，作为重点观察跟踪的股票。

companies = []
prices = []

datas =  dic_resp.get('data').get('diff')
print(datas)
for data in datas:
    #print(data)
    
    #公司名
    company = data.get('f14')
    #当天股价
    price = data.get('f2')
    
    #今日/3日/5日/10日，主力净流入
    #默认只会返回以哥字段，需要自己在param的fields里补上其他字段
    share_1 = data.get('f184')
    share_3 = data.get('f268')
    share_5 = data.get('f165')
    share_10 = data.get('f175')
    
    print(company, price,   share_1, share_5, share_10)
    #这里要注意params里的po字段，为1才是净额大的排在前，如果为0，净额都是负的，自然筛选不到结果
    #筛选的作用，当天机构买入份额大于10%，且5天机构买入份额大于10%，且10天内机构买入份额大于5%
    if share_1 >= 10 and share_5 >= 10 and share_10 >= 5:
        #只有满足上述条件的公司，才放入我们的公司股票池
        companies.append(company)
        prices.append(price)

#满足条件的公司
print(companies)



#3. 数据可视化
from pyecharts.charts import Bar
import pyecharts.options as opts

bar = Bar()
bar.add_xaxis(companies)
bar.add_yaxis('股价图',prices)
#字体倾斜
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(
        axislabel_opts=opts.LabelOpts(rotate=-40)
        ),
    yaxis_opts=opts.AxisOpts(name='价格:(元/股)')
    )

bar.render('股价图.html')











