from matplotlib import pyplot as plt, cm
from scipy.interpolate import griddata

from Algorithm.Theoretical_Approx import Theoretical_Approx
import pandas as pd
import numpy as np

from Data.pull_data import process_df

#Import LEDs and PDs
led_df = pd.read_csv("../Data/LEDs_watch.csv")
pd_df = pd.read_csv("../Data/PDs.csv")

ta = Theoretical_Approx(led_df, pd_df)
areas = ta.theory_approx()

fig = plt.figure(figsize=(7,6))
ax = plt.axes(projection='3d')
X = led_df.Wavelength.tolist()*len(pd_df.Wavelength.tolist())
Y = np.repeat(pd_df.Wavelength.tolist(), len(led_df.Wavelength.tolist()))
Z = [item for sublist in areas for item in sublist]

#ax.scatter3D(X, Y, Z, color='blue')
surf = ax.plot_trisurf(X, Y, Z, cmap=cm.jet, linewidth=0.1)

ax.set_xticks(led_df.Wavelength.tolist())
ax.set_yticks(pd_df.Wavelength.tolist())
ax.set_zticks([0,1])

fig.show()
print()