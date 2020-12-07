import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 一般情况下的夏普比率，需要减去无风险利率。在这里假设无风险利率为每年4%。

# 读入数据，在数据csv文件中先加入表头后再读入
nDate = pd.read_csv('C:/Users/dcdn/Desktop/Quant/finished/量化投资预习任务-江世宇/夏普比率和回撤率计算/ag1806.csv')
# Date', 'Oprice', 'MaxPrice', 'MinPrice', 'Cprice
# nColumn = date.columns.insert(5, 'yieldRate')
# nDate = date.reindex(columns=nColumn, fill_value=0)
nDate['yieldRate'] = 0  # simpler
print(nDate.head(), '\n')  # 增加收益率一列，显示头五行查看

# 该数据包括了多少个交易日
ndays = len(nDate)

# 用当天收盘价减去前一天收盘价后除以前一天收盘价，并且减去无风险利率，来计算每日超额收益率。并放置于新的一列
i = 0
while i < len(nDate):
    nDate.iloc[i, 5] = ((nDate.iloc[i, 4] - nDate.iloc[i - 1, 4]) / nDate.iloc[i - 1, 4]) - 0.04 / ndays
    i = i + 1
print(nDate.head(), '\n')

# 计算每天收益率的平均值
mean = nDate.mean(axis=0)
Ymean = mean[5]

# 计算收益率和
sum = nDate.sum(axis=0)
Ysum = sum[5]

# 计算收益率的标准差
ndate = nDate.values.T  # 转化成numpy数组形式,并转置
YieldArr = ndate[5]  # 得到收益率的数组
yield_std = np.std(YieldArr)

# sharpe ratio = mean / standard deviation
sharpe_ratio = Ymean / yield_std
print('Yield rate of this set of data is {}, and its sharpe ratio is {}'.format(Ysum, sharpe_ratio))

# 数据可视化
nDate['index'] = np.arange(len(nDate))
line = go.Scatter(x=nDate['index'], y=nDate['yieldRate'], name='yield rate')
fig = go.Figure([line])
fig.update_layout(title="Line chart for Yield Rate",
                  xaxis_title="Date",
                  yaxis_title="Rate")
fig.show()
