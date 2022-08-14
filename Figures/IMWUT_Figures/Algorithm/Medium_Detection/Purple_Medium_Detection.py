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
air_df = pd.read_csv("../../../../Data/IMWUT_Data/Medium/purple.csv", usecols = ['1','2','5'])
air_df = process_df(air_df)
air_df = air_df.sort_values('timestamp')
air_df = air_df.iloc[640:-350]
led_order = [530,940,660,470,568,450,633,415,599]
air_df.plot(x='timestamp', y=['415_counts','445_counts','480_counts','515_counts','555_counts','590_counts','630_counts','680_counts'])

xx=air_df.iloc[0]['timestamp']
xx = xx + 4000
i=1

for led in led_order:
    #if i != 1:
    print(led)
    print(i)
    air_df.loc[air_df.timestamp.between(xx+ 3000,xx+ 25000), 'LED'] = led

    plt.axvline(x=xx + 3000, color='b')
    plt.axvline(x=xx + 25000, color='b')
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

#ta = Theoretical_Approx(led_df, pd_df)
#theory_areas = ta.theory_approx()
theory_areas = np.loadtxt('theory_arr.csv', delimiter = ",")


med_arr = np.subtract(exp_arr, theory_areas)
#med_arr = med_arr * -1

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

surf = ax.plot_surface(x_new_grid, y_new_grid, z_new, cmap=cm.CMRmap)
ax.set_xlabel('LED',size=15)
ax.set_ylabel('PD',size=15)
ax.set_zlabel('Spectral Response',size=15)
ax.set_title('Purple', size=20)
fig.show()

print()

fig.savefig("purple.pdf", bbox_inches='tight')
print('Done!')