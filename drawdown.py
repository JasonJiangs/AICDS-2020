import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 一般情况下的夏普比率，需要减去无风险利率。在这里假设无风险利率为每年4%。
# 在此基础上,基于sharpe_ratio2计算的结果，计算max drawdown, 和max drawdown duration

# 读入数据，在数据csv文件中先加入表头后再读入
nDate = pd.read_csv('C:/Users/dcdn/Desktop/Quant/finished/量化投资预习任务-江世宇/夏普比率和回撤率计算/ag1806.csv')
# nDate.insert(loc=5, column='yieldRate', value=0)
nDate['yieldRate'] = 0  # easier way, since assign value zero
# print(nDate.head(), '\n')  # 增加收益率一列，显示头五行查看

# 该数据包括了多少个交易日
ndays = len(nDate)

# 用当天收盘价减去前一天收盘价后除以前一天收盘价，并且减去无风险利率，来计算每日超额收益率。并放置于新的一列
i = 0
while i < len(nDate):
    nDate.iloc[i, 5] = ((nDate.iloc[i, 4] - nDate.iloc[i - 1, 4]) / nDate.iloc[i - 1, 4]) - 0.04 / ndays
    i = i + 1

# 添加一列为累计收益率曲线
nDate['Cumulative_Rate'] = nDate['yieldRate']  # 先复制前一列
# print(nDate.head(), '\n')
for i in range(1, len(nDate)):
    nDate.iloc[i, 6] = nDate.iloc[i, 6] + nDate.iloc[i - 1, 6]

# 添加一列为每天的回撤率，然后找到最大的回撤率 drawdown = ((R1-Ri) / R1)
nDate['drawdown'] = 0  # 暂时存放每次计算的回撤率
nDate['Max_drawdown'] = 0  # 基于每天的最大回撤率
# print(nDate.head(), '\n')
for i in range(1, len(nDate)):
    for k in range(len(nDate)):  # 每次循环把drawdown列清零
        nDate.iloc[i, 7] = 0
    for j in range(i, len(nDate)):  # 计算第i天开始，每天相对于i的回撤率
        nDate.iloc[j, 7] = (nDate.iloc[i, 6] - nDate.iloc[j, 6]) / nDate.iloc[i, 6]
    max_drawdown = nDate['drawdown'].max() // 0.01 / 100  # 寻找max并保留两位数
    nDate.iloc[i, 8] = max_drawdown
Maximum_drawdown = nDate['Max_drawdown'].max()  # 计算每天最大回撤率中的最大值
print("The max drawdown is {}%.".format(Maximum_drawdown))

# 以下计算最长回撤期 max drawdown duration: 持有价值从回撤开始到再创新高所经历的时间
# 还是以某一天为基准，如果下一天下跌，则进入考虑范围
# 如何考虑: 如果基准为第i天,j in range i+1 to len,
# 如果cumulative_rate 在j天和j+1天中间，那么最长回撤期就是j+1-i
lst = []  # 存放所有回撤期
for i in range(len(nDate) - 1):
    if nDate.iloc[i, 6] > nDate.iloc[i + 1, 6]:  # 即符合下跌的条件
        for j in range(i + 1, len(nDate) - 1):
            if nDate.iloc[i, 6] > nDate.iloc[j, 6] and nDate.iloc[i, 6] < nDate.iloc[j + 1, 6]:
                lst.append(j + 1 - i)
                break
lst.sort()
print("The max drawdown duration is {} days.".format(lst.pop()))

# 数据可视化
nDate['index'] = np.arange(len(nDate))
line = go.Scatter(x=nDate['index'], y=nDate['Cumulative_Rate'], name='Cumulative yield rate')
fig = go.Figure([line])
fig.update_layout(title="Line chart for Cumulative Yield Rate",
                  xaxis_title="Date",
                  yaxis_title="Cumulative_Rate")
fig.show()
