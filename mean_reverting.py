import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import math


def cal_drawdown(nDate):
    # 添加一列为累计收益率曲线
    nDate['Cumulative_Rate'] = nDate['strategy_cum']  # 先复制前一列，第14列
    print(nDate, '\n')
    for i in range(2, len(nDate)):
        nDate.iloc[i, 14] = nDate.iloc[i, 14] + nDate.iloc[i - 1, 14]
    print(nDate, '\n')

    # 添加一列为每天的回撤率，然后找到最大的回撤率 drawdown = ((R1-Ri) / R1)
    nDate['drawdown'] = 0  # 暂时存放每次计算的回撤率 第15列
    nDate['Max_drawdown'] = 0  # 基于每天的最大回撤率 第16列
    # print(nDate['drawdown'].index)
    # print(nDate, '\n')
    # print(list(nDate))
    # for i in range(1, len(nDate)):
    #     for k in range(len(nDate)):  # 每次循环把drawdown列清零
    #         nDate.iloc[i, 15] = 0
    #     for j in range(i, len(nDate)):  # 计算第i天开始，每天相对于i的回撤率
    #         nDate.iloc[j, 15] = (nDate.iloc[i, 14] - nDate.iloc[j, 14]) / nDate.iloc[i, 14]
    #     # print(nDate['drawdown'])
    #     max_drawdown = max(nDate['drawdown']) // 0.01 / 100  # 寻找max并保留两位数
    #     # print(max_drawdown)
    #     nDate.iloc[i, 16] = max_drawdown
    Maximum_drawdown = nDate['Max_drawdown'].max()  # 计算每天最大回撤率中的最大值
    # print(nDate, '\n')

    # # 以下计算最长回撤期 max drawdown duration: 持有价值从回撤开始到再创新高所经历的时间
    # # 还是以某一天为基准，如果下一天下跌，则进入考虑范围
    # # 如何考虑: 如果基准为第i天,j in range i+1 to len,
    # # 如果cumulative_rate 在j天和j+1天中间，那么最长回撤期就是j+1-i
    # lst = []  # 存放所有回撤期
    # for i in range(len(nDate) - 1):
    #     if nDate.iloc[i, 14] > nDate.iloc[i + 1, 14]:  # 即符合下跌的条件
    #         for j in range(i + 1, len(nDate) - 1):
    #             if (nDate.iloc[i, 14] > nDate.iloc[j, 14]) and (nDate.iloc[i, 14] < nDate.iloc[j + 1, 14]):
    #                 lst.append(j + 1 - i)
    #                 break
    # lst.sort()
    # # draw_duration = lst.pop()
    draw_duration = 0
    return Maximum_drawdown, draw_duration


def cal_sharpeRatio(nDate):
    # 一般情况下的夏普比率，需要减去无风险利率。在这里假设无风险利率为每年4%。
    # 用strategy return减去无风险利率，来计算每日超额收益率。并放置于新的一列
    i = 1
    while i < len(nDate):
        nDate.iloc[i, 10] = nDate.iloc[i, 10]
        i = i + 1

    # 计算每天收益率的平均值
    mean = nDate.mean(axis=0)
    Ymean = mean[10]

    # 计算收益率和
    sum = nDate.sum(axis=0)
    Ysum = sum[10]

    # 计算收益率的标准差
    ndate = nDate.values.T  # 转化成numpy数组形式,并转置
    YieldArr = ndate[10]  # 得到收益率的数组
    yield_std = np.std(YieldArr[1:])

    print('yield std: ', yield_std)

    # sharpe ratio = mean / standard deviation
    sharpe_ratio = Ymean / yield_std
    return sharpe_ratio


def cal_volatility(nDate):
    # 基本思路：求一列log_return = ln(当日收盘价/前一天收盘价), daily volatility = standard devaition of log return
    # annulized volatility = daily volatility * sqrt(252)
    daily_volatility = 0
    annulized_volatility = 0
    nDate['log_return'] = 0  # index = 17
    nDate['daily_Vlt'] = 0  # index = 18
    nDate['annual_Vlt'] = 0  # index = 19
    for i in range(1, len(nDate) - 1):
        nDate.iloc[i, 17] = math.log(nDate.iloc[i, 1] / nDate.iloc[i + 1, 1])
    lst_std = []
    for i in range(1, len(nDate) - 1):
        lst_std.append(nDate.iloc[i, 17])
    daily_volatility = np.std(lst_std)
    annulized_volatility = daily_volatility * math.sqrt(252)
    return daily_volatility, annulized_volatility


def cal_annual_yield(nDate):
    return nDate.iloc[len(nDate) - 1, 12] / len(nDate) * 252


def cal_B_volatility(nDate):
    value = 0
    return value


def cal_B_ann_yield(nDate):
    value = 0
    return value


# pandas库的载入csv文件
nDate = pd.read_csv('C:/Users/dcdn/Desktop/HS300_Data.csv')
# nDate = pd.read_csv('C:/Users/dcdn/Desktop/al1801.csv')
# print(nDate.head(), '\n')  # 显示头五行内容

# 计算SMA，简单移动平均线，也就是价格平均线，先设置过去五天的平均值为均线
nDate['SMA'] = 0  # 添加一列存放五日的SMA
j = 4
while j < len(nDate):  # 做一个循环存放结果
    nDate.iloc[j, 5] = (nDate.iloc[j, 4] + nDate.iloc[j - 1, 4] + nDate.iloc[j - 2, 4] + \
                        nDate.iloc[j - 3, 4] + nDate.iloc[j - 4, 4]) / 5
    j = j + 1
# print(nDate.head(), '\n')  # 打印结果看一下，因为计算五日均线，因此前四项的结果为0
# # 下面为十日的SMA
# j = 9
# while j < len(nDate):  # 做一个循环存放结果】
#     nDate.iloc[j, 5] = (nDate.iloc[j, 4] + nDate.iloc[j - 1, 4] + nDate.iloc[j - 2, 4] + \
#                         nDate.iloc[j - 3, 4] + nDate.iloc[j - 4, 4] + nDate.iloc[j - 5, 4] + \
#                         nDate.iloc[j - 6, 4] + nDate.iloc[j - 7, 4] + nDate.iloc[j - 8, 4] + \
#                         nDate.iloc[j - 9, 4]) / 10
#     j = j + 1

# 计算标准差
nDate['std'] = 0  # 增加一行存放standard deviation
k = 4
while k < len(nDate):  # 做一个循环计算存放结果
    temp_arr = []  # 为了计算std，用一个临时的数组存放前五天收盘价，然后用numpy的函数np.std存放前五天收盘价
    for i in range(5):  # 存放前五天收盘价
        temp_arr.append(nDate.iloc[k - i, 4])
    nDate.iloc[k, 6] = np.std(temp_arr)  # 存放前五天收盘价
    k = k + 1
# print(nDate.head(), '\n')  # 打印看结果

# 或者考虑价格百分比，比如这个threshold为上下10%×SMA

# 求出当前价格close_price与移动平均值的差价
nDate['diff'] = 0
p = 4
while p < len(nDate):
    nDate.iloc[p, 7] = nDate.iloc[p, 5] - nDate.iloc[p, 4]
    p = p + 1
# print(nDate.head(), '\n')  # 打印看结果

# 这里，如果我们暂时不用std或价格百分比来作为一个阈值的情况，简单的设定一个固定阈值
# 用matplotlib画图后，将阈值调整到一个合适的值，差价向上或向下突破了threshold，那么就产生多空信号
threshold = 85
nDate['diff'].dropna().plot(legend=True)
plt.axhline(threshold, color='r')
plt.axhline(0, color='r')
plt.axhline(-threshold, color='r')
plt.show()

# 设置多空信号,做空和做多都用1来表示开仓
nDate['position'] = 0
u = 4
while u < len(nDate) - 1:
    dif = nDate.iloc[u, 7]
    if (dif > threshold) & (dif > 0):  # 卖出
        nDate.iloc[u + 1, 8] = -1
    elif (dif < -threshold) & (dif < 0):  # 买入
        nDate.iloc[u + 1, 8] = 1
    u = u + 1

# 计算benchmark的每日收益率
nDate['yield_Rate'] = 0
nDate['yield_Rate'] = nDate['CPrice'].pct_change()
# print(nDate.head(), '\n')

# 计算策略的收益率，***
# position要和下一天和收益率相乘是因为：策略是当日平仓的，
# 然后上一天的position是相对于收盘价，所以需要在第二天进行操作。
# 如果说第二天是正的收益率，
nDate['strategy_return'] = 0
nDate['strategy_return'] = nDate['position'].shift(1) * nDate['yield_Rate']
# print(nDate.head(), '\n')

# 计算benchmark和策略的累乘收益率
nDate['return_cum'] = 0
nDate['strategy_cum'] = 0
nDate['return_cum'] = (nDate['yield_Rate'] + 1).cumprod()  # comprod()是累乘
nDate['strategy_cum'] = (nDate['strategy_return'] + 1).cumprod()

# 累计收益率和benchmark相比较
nDate[['return_cum', 'strategy_cum']].dropna().plot()
plt.show()

nnDate = nDate

# 数据可视化,价格趋势：从价格趋势上我们可以看出它是不是一个震荡和行情
nDate['index'] = np.arange(len(nDate))
line = go.Scatter(x=nDate['index'], y=nDate['CPrice'], name='Close price')
fig = go.Figure([line])
fig.update_layout(title="Line chart for close price",
                  xaxis_title="Date",
                  yaxis_title="Close price")
# fig.show()

# 数据可视化,累计收益率
nDate['index'] = np.arange(len(nDate))
line = go.Scatter(x=nDate['index'], y=nDate['strategy_cum'], name='Cumulative strategy yield rate')
fig = go.Figure([line])
fig.update_layout(title="Line chart for Cumulative Strategy Yield Rate",
                  xaxis_title="Date",
                  yaxis_title="strategy_cum")
# fig.show()

# 数据可视化,每日收益率
nDate['index'] = np.arange(len(nDate))
line = go.Scatter(x=nDate['index'], y=nDate['strategy_return'], name='Strategy yield rate')
fig = go.Figure([line])
fig.update_layout(title="Line chart for Strategy Yield Rate",
                  xaxis_title="Date",
                  yaxis_title="strategy_return")
# fig.show()

# strategy maximum drawdown and maximum drawdown duration
max_drawdown, draw_duration = cal_drawdown(nnDate)
print('Maximum drawdown: ', max_drawdown, '%.')
print('Maximum drawdown duration: ', draw_duration, 'days.')

#  strategy volatility, backward looking
daily_volatility, annulized_volatility = cal_volatility(nnDate)
print('Annualized volatility: ', annulized_volatility)
print('Daily volatility: ', daily_volatility)

# strategy sharpe ratio
sharpe_ratio = cal_sharpeRatio(nnDate)
print('Sharpe ratio: ', sharpe_ratio)

# strategy annual yield
annual_yield = cal_annual_yield(nnDate)
print('Annual yield: ', annual_yield)

# benchmark volatility
benchmark_volatility = cal_B_volatility(nnDate)
print('Benchmark volatility: ', benchmark_volatility)

# benchmark annual yield
benchmark_ann_yield = cal_B_ann_yield(nnDate)
print('Benchmark annual yield: ', benchmark_ann_yield)

# 导出excel
nnDate.to_csv('C:/Users/dcdn/Desktop/com_Result.csv')
