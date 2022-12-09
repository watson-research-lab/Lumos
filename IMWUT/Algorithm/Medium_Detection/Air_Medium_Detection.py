from matplotlib import pyplot as plt, cm
from scipy.interpolate import griddata

import pandas as pd
import numpy as np

from Spectral_Response_of_Medium.Data.pull_data import process_df

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

#Import LEDs and PDs
led_df = pd.read_csv("../../../Spectral_Response_of_Medium/Data/LEDs_watch.csv")
pd_df = pd.read_csv("../../../Spectral_Response_of_Medium/Data/PDs.csv")

#Import Air Medium
air_df = pd.read_csv("../../IMWUT_Data/Medium/air.csv", usecols = ['1', '2', '5'])
air_df = process_df(air_df)
air_df = air_df.sort_values('timestamp')
air_df = air_df.iloc[85:]
led_order = [530,940,633,470,568,450,660,415,599]
air_df.plot(x='timestamp', y=['415_counts','445_counts','480_counts','515_counts','555_counts','590_counts','630_counts','680_counts'])

xx=air_df.iloc[0]['timestamp']
i=0

for led in led_order:
    #if i != 1:
    #print(i)
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
print('Final: ',final_df.head())

final_df = final_df.drop(['LED'], axis=1)
exp_arr = final_df.to_numpy()

#theory = Theoretical_Approx(led_df, pd_df)
#theory_areas = theory.theory_approx()

#Intensity
st_arr=[]
"""for ta,ea in zip(theory_areas, exp_arr):
    #print(max(ea))
    new_t = max(ea) * np.array(ta)
    #print(new_t)
    st_arr = np.append(st_arr, np.array(new_t), axis=0)
    print('Loop st:', st_arr)
print('Exp: ',exp_arr)
print('Theory: ',st_arr)

st_arr = np.reshape(st_arr,(8,8))"""
med_arr = np.subtract(exp_arr, 0.97 * exp_arr)
med_arr = med_arr * -1
print('Medium: ',med_arr)

np.savetxt("theory_arr.csv", exp_arr, delimiter=",")

#print(med_arr
fig = plt.figure(figsize=(7,6))
ax = plt.axes(projection='3d')
X = np.array(led_df.Wavelength.tolist()*len(pd_df.Wavelength.tolist()))
Y = np.array(np.repeat(pd_df.Wavelength.tolist(), len(led_df.Wavelength.tolist())))
Z = np.array([item for sublist in med_arr for item in sublist])

x_min = X.min()
x_max = X.max()
y_min = Y.min()
y_max = Y.max()

#citation
#https://stackoverflow.com/questions/33287620/creating-a-smooth-surface-plot-from-topographic-data-using-matplotlib
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html

#change third argument in linspace() to change interpolated dataset amount
x_new = np.linspace(x_min, x_max, 600)
y_new = np.linspace(y_min, y_max, 600)

#change method: nearest, linear, cubic, etc.
z_new = griddata((X, Y), Z, (x_new[None,:], y_new[:,None]), method='cubic')

x_new_grid, y_new_grid = np.meshgrid(x_new, y_new)

surf = ax.plot_surface(x_new_grid, y_new_grid, z_new, cmap=cm.jet,vmin = 0, vmax = 5000)
ax.set_xticks(led_df.Wavelength.tolist())
ax.set_yticks(pd_df.Wavelength.tolist())
ax.set_zlim(-5000, 5000)

ax.set_xlabel('LED',size=15)
ax.set_ylabel('PD',size=15)
ax.set_zlabel('Spectral Response',size=15)
ax.set_title('No Medium', size=20)

fig.show()
print()
fig.savefig("air.pdf", bbox_inches='tight')
print('Done!')