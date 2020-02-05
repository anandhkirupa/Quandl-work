import quandl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = quandl.get("HKEX/02882",authtoken = open("quandl_api.txt","r").read(),paginate=True)

print(data.tail())

data['Nominal Price'].plot(grid=True)
plt.title("HK2882 (closing prices)")
plt.show()

s_window = 40
l_window = 100

sig = pd.DataFrame(index = data.index)
sig['sig1'] = 0.0

sig['s_mavg'] = data['Nominal Price'].rolling(window = s_window, min_periods = 1, center = False).mean()

sig['l_mavg'] = data['Nominal Price'].rolling(window = l_window, min_periods = 1, center = False).mean()

sig['sig1'][s_window:] = np.where(sig['s_mavg'][s_window:] > sig['l_mavg'][s_window:], 1.0, 0.0)

sig['pos'] = sig['sig1'].diff()

print(sig)

fig = plt.figure(figsize = (20,15))

ax1 = fig.add_subplot(111, ylabel = 'Price in $')

data['Nominal Price'].plot(ax = ax1, color = 'black', lw = 2.)

sig[['s_mavg', 'l_mavg']].plot(ax = ax1, lw = 2.)

ax1.plot(sig.loc[sig.pos == 1.0].index, sig.s_mavg[sig.pos == 1.0], '^', markersize = 20, color = 'g')

ax1.plot(sig.loc[sig.pos == -1.0].index, sig.s_mavg[sig.pos == -1.0], 'v', markersize = 20, color = 'r')

plt.show()

initial_capital = float(100000)

pos = pd.DataFrame(index = sig.index).fillna(0.0)

pos['pos in HKD'] = 1000*sig['sig1']

port = pos.multiply(data['Nominal Price'], axis = 0)

pos_diff = pos.diff()

port['holdings'] = (pos.multiply(data['Nominal Price'], axis = 0)).sum(axis = 1)

port['cash'] = initial_capital - (pos_diff.multiply(data['Nominal Price'], axis = 0)).sum(axis = 1).cumsum()

port['total'] = port['cash'] + port['holdings']

port['returns'] = port['total'].pct_change()

del port['pos in HKD']

print(port.tail())

fig = plt.figure(figsize=(20,15))

ax1 = fig.add_subplot(111, ylabel = 'port value in $')

port['total'].plot(ax = ax1, lw = 2.)

ax1.plot(port.loc[sig.pos == 1.0].index, port.total[sig.pos == 1.0], '^', markersize = 20, color = 'g')

ax1.plot(port.loc[sig.pos == -1.0].index, port.total[sig.pos == -1.0], 'v', markersize = 20, color = 'r')

plt.show()

print("port total value as of Febrauary 4th 2020")
print(port['total'].tail(1))

print("Absolute value as of Febrauary 4th 2020")
print((((port['total'].tail(1)/float(100000))-float(1))*100))