import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 市场中性策略的夏普比率，不需要减去无风险收益

# 读入数据，在数据csv文件中先加入表头后再读入
date = pd.read_csv('C:/Users/dcdn/Desktop/a1801.csv')
nColumn = date.columns.insert(5, 'yieldRate')
nDate = date.reindex(columns=nColumn, fill_value=0)
print(nDate.head(), '\n')  # 增加收益率一列，显示头五行查看

# 收益率用当天价格减去前一天价格后除以前一天价格，来计算，都是收盘价
i = 0
while i < len(nDate):
    nDate.iloc[i, 5] = (nDate.iloc[i, 4] - nDate.iloc[i - 1, 4]) / nDate.iloc[i - 1, 4]
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
print(nDate)
line = go.Scatter(x=nDate['index'], y=nDate['yieldRate'], name='yield rate')
fig = go.Figure([line])
fig.update_layout(title="Line chart for Yield Rate",
                  xaxis_title="Date",
                  yaxis_title="Rate")
fig.show()
