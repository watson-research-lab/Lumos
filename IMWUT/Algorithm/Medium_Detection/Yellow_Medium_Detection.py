import matplotlib
from matplotlib import pyplot as plt, cm
from scipy.interpolate import griddata

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

import pandas as pd
import numpy as np

from Spectral_Response_of_Medium.Data.pull_data import process_df

#Import LEDs and PDs
led_df = pd.read_csv("../../../Spectral_Response_of_Medium/Data/LEDs_watch.csv")
pd_df = pd.read_csv("../../../Spectral_Response_of_Medium/Data/PDs.csv")

#Import Air Medium
air_df = pd.read_csv("../../IMWUT_Data/Medium/yellow.csv", usecols = ['1', '2', '5'])
air_df = process_df(air_df)
air_df = air_df.sort_values('timestamp')
air_df = air_df.iloc[85:]
led_order = [530,940,660,470,568,450,633,415,599]
air_df.plot(x='timestamp', y=['415_counts','445_counts','480_counts','515_counts','555_counts','590_counts','630_counts','680_counts'])

xx=air_df.iloc[0]['timestamp']
#plt.axvline(x=xx, color='b')
#plt.axvline(x=xx+15000, color='b')
xx = xx +22000
i=1

for led in led_order:
    #if i != 1:
    print(led)
    print(i)
    air_df.loc[air_df.timestamp.between(xx+ 1000,xx+ 26000), 'LED'] = led
    if(i==9):
        air_df.loc[air_df.timestamp.between(xx + 3000, xx + 26000), 'LED'] = led
        plt.axvline(x=xx + 3000, color='b')
        plt.axvline(x=xx + 18000, color='b')
    else:
        air_df.loc[air_df.timestamp.between(xx + 1000, xx + 26000), 'LED'] = led
        plt.axvline(x=xx + 1000, color='b')
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

print(final_df)
final_df = final_df.drop(['LED'], axis=1)
exp_arr = final_df.to_numpy()

#ta = Theoretical_Approx(led_df, pd_df)
#theory_areas = ta.theory_approx()
theory_areas = np.loadtxt('theory_arr.csv', delimiter = ",")

med_arr = np.subtract(exp_arr, theory_areas)
med_arr = med_arr *-1

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

surf = ax.plot_surface(x_new_grid, y_new_grid, z_new, cmap=cm.CMRmap,vmin = -3000, vmax = 35000)

ax.set_xticks(led_df.Wavelength.tolist())
ax.set_yticks(pd_df.Wavelength.tolist())

ax.set_xlabel('LED',size=15)
ax.set_ylabel('PD',size=15)
ax.set_zlabel('Spectral Response',size=15)
ax.set_title('Yellow', size=20)
fig.show()
print()
from scipy.signal import find_peaks
z_new2 = np.ravel(z_new)
z_new2=np.array(z_new2)
y_new2 = np.ravel(y_new_grid)
y_new2=np.array(y_new2)
x_new2 = np.ravel(x_new_grid)
x_new2=np.array(x_new2)
peaks, _ = find_peaks(z_new2, prominence=(15000, 65535))

new_peaks=peaks
print(peaks)
for i in range(0, len(peaks)):
    print(z_new2[peaks[i]])
    if(z_new2[peaks[i]]) < 0:
        print(peaks[i])
        z_new2 = np.delete(z_new2, int(z_new2[peaks[i]]))
        new_peaks = np.delete(peaks, i)
print(new_peaks)

array_temp = []
array_temp_peak = []
array_temp_peak_MAX = []
array_temp_MAX = []
temp_peaks = new_peaks
value = 0

if len(temp_peaks)!=0:
    for j in range(1, len(temp_peaks)):
        print(j)
        if z_new2[temp_peaks[j]] - z_new2[temp_peaks[j - 1]] > 0: #increasing
            array_temp.append(z_new2[temp_peaks[j - 1]])
            array_temp_peak.append(temp_peaks[j - 1])
        elif z_new2[temp_peaks[j]] - z_new2[temp_peaks[j - 1]] < 0: #decreasing
            if len(array_temp)==0:
                nothing = 0
                # skip if only decreasing from beginning. 'miss' first peak
            else:
                array_temp_MAX.append(max(array_temp))
                array_temp_peak_MAX.append(max(array_temp_peak))
                array_temp=[]
                array_temp_peak=[]

            print(len(temp_peaks))
            print("reset")
            if j == len(temp_peaks):
                temp_peaks=[]
            else:
                j=0
                temp_peaks = temp_peaks[j:len(temp_peaks)]

        if j == len(temp_peaks):
            temp_peaks=[]

        #print(temp_peaks)
        #print(array_temp_MAX)

# print("peak")
# print(array_temp_peak2)
# print(z_new2.max())
# print(y_new2)
print("z values MAX")
print(array_temp_MAX)
print("y values MAX")
for m in range(0, len(array_temp_peak_MAX)):
    print(y_new2[array_temp_peak_MAX[m]])
print("x values MAX")
for n in range(0, len(array_temp_peak_MAX)):
    print(x_new2[array_temp_peak_MAX[n]])

fig.savefig("yellow.pdf", bbox_inches='tight')
print('Done!')