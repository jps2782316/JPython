#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 11:41:06 2021

@author: jps
"""

"""
主题: 股票数据采集实现数据可视化效果

介绍:
    截至2019年年底我国股票投资者数量为15975.24万户，如此多股民热衷于炒股，首先抛开炒股技术不说，
    那么多股票数据是不是非常难找，找到之后看着秘密麻麻的数据是不是头大？
    今天就来实现爬取雪球平台的股票数据，并且实现数据可是化。

课程亮点:
    1. 系统分析网页性质
    2. 结构化的数据解析
    3. csv数据保存
    4. 实现股票数据可视化的效果

环境介绍:
    python 3.9
    pycharm
    requests
    csv
    
爬虫: 模拟客户端(浏览器/app)获取服务器数据。批量的获取数据，速度比较快。


爬虫案例的步骤:
    1. 确定url地址
    2. 通过代码发送网络请求
    3. 数据解析、数据筛选
    4. 数据保存
      数据库(关系型数据库mysql、非关系型数据库mongodb、缓冲型数据库redis)
      本地文件(csv)
    

"""


"""
打开网页，空白处右键 > 显示网页源代码。就能看到一些静态数据。我们要抓取的是静态网页里没有的动态数据。

右键空白处 > 检查。会弹出调试工具。选中Network这一栏，Network相当于浏览器自带的抓包工具，其他抓包
工具还有Wireshark，charles等。也就是说其他抓包工具是可以代理这里的Network的。

点击完Network，刷新当前页面，所有的请求数据都会在下面以数据包的形式呈现。
方式一: 逐一点击数据包，选择右侧的Preview,查看是否有需要的数据，从而确定url。
方式二: 顶上的过滤器，选择过滤条件，默认为all，我们选择XHR(表示过滤一些接口数据)，再在剩余的数据包里查找，看是否有我们需要的数据。
如果没有，只能且回all，按方式一的fang


"""



#============================ 1. 数据爬取、处理 ============================ 




import requests
import pprint #格式化输出模块
import csv



#获取数据，并保存到csv
def fetch_write_data(index):
    print('=================正在抓取{}页数据================='.format(index)) #{}表示占位符，通过format传入
    
    #1. 确定url地址<分析网页性质>，然后点击Headers，复制Request URL
    url = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page={}&size=30&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz&_=1611126942745'.format(str(index))
    
    #2. 发送网络请求
    #resp = requests.get(url)
    #由于服务器一般会有一些反爬机制，所以报403错误，<Response [403]>, 因为没有加一些请求头(从浏览器请求的时候，浏览器默认会带上这些字段，处不处理，服务端自己决定)。
    #所以要加一些请求头，还是在Headers里,找到Request Headers,例如把User-Agent复制过来，加到请求头里。从而把爬虫代码伪装称浏览器用户，这样服务器就不能轻易识别我们的爬虫程序，才会给我们返回数据。
    #Chrome/87.0.4280.88 Safari/537.36
    #从User-Agent可以简单的知道，我用的是谷歌浏览器，浏览器版本为87.0.4280.88。
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    #1)得到一个响应对象
    resp = requests.get(url, headers=headers) #<Response [200]>
    print(resp)
    #2)获得json数据
    json_data = resp.json()
    print(json_data)
    #格式化输出
    pprint.pprint(json_data)
    
    
    #3. 数据解析、数据筛选
    data_list = json_data['data']['list']
    for data in data_list:
        #股票代码
        symbol = data['symbol'] 
        #公司名
        name = data['name']
        #当前价格
        price = data['current']
        #涨跌额
        chg = data['chg']
        #涨跌幅
        percent = data['percent']
        #年初至今
        current_year_percent = data['current_year_percent']
        #成交量
        volume = data['volume']
        #成交额
        amount = data['amount']
        #换手率
        turnover_rate = data['turnover_rate']
        #市盈率
        pe_ttm = data['pe_ttm']
        #股息率,可能为None
        dividend_yield = data['dividend_yield']
        #市值
        market_capital = data['market_capital']
    
        
        #4.数据保存
        data_dic = {'股票代码': symbol, '股票名称': name, '当前价格': price, '涨跌额': chg, '涨跌幅': percent, 
                    '年初至今': current_year_percent, '成交量': volume, '成交额': amount, '换手率': turnover_rate, 
                    '市盈率(TTM)': pe_ttm, '股息率': dividend_yield, '市值': market_capital}
        csv_wireter.writerow(data_dic)





#以追加方式打开一个文件
file = open('data1.csv', mode='a', encoding='utf-8', newline='')
fields = ['股票代码', '股票名称', '当前价格', '涨跌额', '涨跌幅', '年初至今', '成交量', '成交额', '换手率', '市盈率(TTM)', '股息率', '市值']
csv_wireter = csv.DictWriter(file, fieldnames=fields)
#写入一次表头数据
csv_wireter.writeheader()

#抓取前100页数据并保存, (要抓取全部的话，网页上看一下有多少翻页，就抓取到第几页就行了。)
for page in range(1, 101):
    fetch_write_data(page)
















