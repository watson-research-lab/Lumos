from matplotlib import pyplot as plt, cm
from scipy.interpolate import griddata

from Algorithm.Theoretical_Approx import Theoretical_Approx
import pandas as pd
import numpy as np

from Data.pull_data import process_df

#Import LEDs and PDs
led_df = pd.read_csv("../../../../Data/LEDs_watch.csv")
pd_df = pd.read_csv("../../../../Data/PDs.csv")

#Import Air Medium
air_df = pd.read_csv("../../../../Data/IMWUT_Data/Medium/air.csv", usecols = ['1','2','5'])
air_df = process_df(air_df)
air_df = air_df.sort_values('timestamp')
air_df = air_df.iloc[85:]
led_order = [530,940,660,470,568,450,633,415,599]
air_df.plot(x='timestamp', y=['415_counts','445_counts','480_counts','515_counts','555_counts','590_counts','630_counts','680_counts'])

xx=air_df.iloc[0]['timestamp']
i=0

for led in led_order:
    #if i != 1:
    print(i)
    air_df.loc[air_df.timestamp.between(xx+ 3000,xx+ 26000), 'LED'] = led
    plt.axvline(x=xx+ 3000, color='b')
    plt.axvline(x=xx + 26000, color='b')
    # air_df.loc[air_df['timestamp'] > xx+ 1000 and air_df['timestamp'] < xx+ 26000] = 1
    xx=xx+30000
    i=i+1
plt.show()
air_df = air_df[air_df['LED'].notna()]
air_df['LED'] = air_df['LED'].astype(int)
air_df = air_df.drop(['timestamp'], axis=1)

final_df = pd.DataFrame()

for led in led_df.Wavelength:
    working_df = pd.DataFrame(air_df.loc[air_df['LED'] == (led)].mean().to_dict(),index=[air_df.index.values[-1]])
    final_df = pd.concat([final_df, working_df], axis=0)

print(final_df.head())
final_df = final_df.drop(['LED'], axis=1)
exp_arr = final_df.to_numpy()

theory = Theoretical_Approx(led_df, pd_df)
theory_areas = theory.theory_approx()

#Intensity
st_arr=[]
for ta,ea in zip(theory_areas, exp_arr):
    #print(max(ea) * np.array(ta))
    new_t = max(ta) * np.array(ea)
    #print(new_t)
    st_arr = np.append(st_arr, np.array(new_t), axis=0)
    #print
print('Exp: ',exp_arr)
print('Theory: ',st_arr)
med_arr = np.subtract(exp_arr, st_arr)

#print(med_arr)
fig = plt.figure(figsize=(7,6))
ax = plt.axes(projection='3d')
X = led_df.Wavelength.tolist()*len(pd_df.Wavelength.tolist())
Y = np.repeat(pd_df.Wavelength.tolist(), len(led_df.Wavelength.tolist()))
Z = [item for sublist in med_arr for item in sublist]

surf = ax.plot_trisurf(X, Y, Z, cmap=cm.jet, linewidth=0.1)

ax.set_xticks(led_df.Wavelength.tolist())
ax.set_yticks(pd_df.Wavelength.tolist())

fig.show()
print()