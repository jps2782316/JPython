#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 16:55:45 2021

@author: jps
"""




#============================ 2. 数据可视化 ============================ 
import pandas as pd 
from pyecharts import options as opts
from pyecharts.charts import Bar

data_df = pd.read_csv('data.csv')
df = data_df.dropna()
df1 = df[['股票名称', '成交量']].iloc[:20] #切取前20条数据
print(df1['股票名称'].values)
print(df1['成交量'].values)



c = (
     Bar()
         .add_xaxis(list(df1['股票名称'].values))
         .add_yaxis('股票成交量情况', list(df1['成交量'].values))
         .set_global_opts(
            datazoom_opts=opts.DataZoomOpts(),
            title_opts=opts.TitleOpts(title=('成交量图表 - Volume chart')),
         )
         .render('data.html')
)



