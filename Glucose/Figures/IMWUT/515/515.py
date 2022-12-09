import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from scipy.stats import pearsonr, spearmanr
from scipy import signal
from Data.pull_data import process_df

wv = '515'
pds = '680'
pd_col = pds + '_counts'
wv_col = wv + '_counts'

"""Load Spec values and timestamps"""
df = pd.read_csv("spec_2.csv", usecols=['1', '2', '5'])
spec_df = process_df(df)

"""Load Glucose values and timestamps"""
glucose_df = pd.read_csv("bs_times.csv")
glucose_df['time'] = pd.to_datetime(glucose_df['time'])
glucose_df['time'] = glucose_df.time.apply(lambda x: (x.value / 1e6))

glucose_df = glucose_df[3:]
spec_df.timestamp = (spec_df.timestamp - glucose_df.time.iloc[0])
glucose_df.time = (glucose_df.time - glucose_df.time.iloc[0])

mask = (spec_df['timestamp'] > glucose_df.time.iloc[0]) & (spec_df['timestamp'] <= glucose_df.time.iloc[-1])
spec_df = spec_df.loc[mask]
spec_df = spec_df.reset_index(drop=True)


glucose_df.time = glucose_df.time - glucose_df.time.iloc[0]
glucose_df.time = glucose_df.time + 300000
spec_df['timestamp'] = spec_df['timestamp'] - spec_df['timestamp'].min()
print(glucose_df.time.iloc[0])
mask = (spec_df['timestamp'] > glucose_df.time.iloc[0])
spec_df = spec_df.loc[mask]

print(spec_df['timestamp'].iloc[0])

"""Figure"""
fig = plt.figure(figsize=(9, 5))
ax = fig.gca()
ax2 = ax.twinx()

"""Plot Raw Values"""
l1 = ax.plot(spec_df.timestamp, spec_df[pd_col], label='Spectral Sensor')
l2 = ax2.plot(glucose_df.time[:-1], glucose_df.bs[:-1], 'ro', label='Glucose Reading')

"""Interpolated Data"""
N = 150
#sos = signal.cheby2(N=4, Wn = [0.5, 10], btype = 'bandpass', fs=2)
#print(sos)
mov_avg = np.convolve(spec_df[pd_col], np.ones(N) / N, mode='valid')
x = np.linspace(min(glucose_df.time[:-1]), max(glucose_df.time[:-1]), num=len(mov_avg), endpoint=True)

f2 = interp1d(glucose_df.time[:-1], glucose_df.bs[:-1], kind='linear')

signal.detrend(f2(x))
l3 = ax.plot(spec_df.timestamp[:-(N-1)], mov_avg, label='Spectral Sensor')
l4 = ax2.plot(x, f2(x), label='Glucose Reading')

print('Pearson: ', pearsonr(mov_avg, f2(x)))
print('Speaman: ', spearmanr(mov_avg, f2(x)))


def numfmt(x, pos):  # your custom formatter function: divide by 100.0
    s = f'{x / 60000:,.0f}'  # <----
    return s


import matplotlib.ticker as tkr  # has classes for tick-locating and -formatting
yfmt = tkr.FuncFormatter(numfmt)  # create your custom formatter function
ax.xaxis.set_major_formatter(yfmt)
ax2.set_ylim([150, 90])
lns = l1 + l2
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0, fontsize=16)

ax.set(xlabel='Time(minutes)', ylabel='Counts')
ax2.set(ylabel='Glucose(mg/dL)')
ax.set_title('515nm LED', fontsize=20)
plt.show()