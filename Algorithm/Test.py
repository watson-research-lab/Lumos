from matplotlib import pyplot as plt, cm
from scipy.interpolate import griddata

from Algorithm.Theoretical_Approx import Theoretical_Approx
import pandas as pd
import numpy as np

#from Data.pull_data import process_df

#Import LEDs and PDs
led_df = pd.read_csv("../Data/LEDs_watch.csv")
pd_df = pd.read_csv("../Data/PDs.csv")

ta = Theoretical_Approx(led_df, pd_df)
areas = ta.theory_approx()

fig = plt.figure(figsize=(7,6))
ax = plt.axes(projection='3d')
X = np.array(led_df.Wavelength.tolist()*len(pd_df.Wavelength.tolist()))
Y = np.array(np.repeat(pd_df.Wavelength.tolist(), len(led_df.Wavelength.tolist())))
Z = np.array([item for sublist in areas for item in sublist])
x_min = X.min()
x_max = X.max()
y_min = Y.min()
y_max = Y.max()

#citation
#https://stackoverflow.com/questions/33287620/creating-a-smooth-surface-plot-from-topographic-data-using-matplotlib

#change third argument in linspace() to change interpolated dataset amount
x_new = np.linspace(x_min, x_max, 600)
y_new = np.linspace(y_min, y_max, 600)

#change method: nearest, linear, cubic, etc.
z_new = griddata((X, Y), Z, (x_new[None,:], y_new[:,None]), method='cubic')

x_new_grid, y_new_grid = np.meshgrid(x_new, y_new)

surf = ax.plot_surface(x_new_grid, y_new_grid, z_new, cmap=cm.jet)

ax.set_xticks(led_df.Wavelength.tolist())
ax.set_yticks(pd_df.Wavelength.tolist())
ax.set_zticks([0,1])

fig.show()
print()