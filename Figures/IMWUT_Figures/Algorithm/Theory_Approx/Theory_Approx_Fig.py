import numpy as np
import pandas as pd
from matplotlib import gridspec, pyplot as plt
import luxpy as lx
import luxpy.toolboxes.spdbuild as spb

from Data.pull_data import process_df

print('------------------------Creating Spectrum Graphs------------------------')

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
plt.axvline(x = air_df.iloc[0]['timestamp'], color = 'b')
plt.axvline(x = air_df.iloc[0]['timestamp']+28000, color = 'b')
xx=air_df.iloc[0]['timestamp']
i=0
if i != 1:
    for led in led_order:

        plt.axvline(x=xx+ 1000, color='b')
        plt.axvline(x=xx + 26000, color='b')
        #air_df.loc[air_df['timestamp'] > xx+ 1000 and air_df['timestamp'] < xx+ 26000] = 1
        air_df.loc[air_df.timestamp.between(xx+ 1000,xx+ 26000), 'LED'] = led

        xx=xx+30000
        print(xx)
    i=i+1
plt.show()
air_df = air_df[air_df['LED'].notna()]

print(air_df.head())

total_graphs = len(led_df) * len(pd_df) +len(led_df)
print('Creating ' + str(total_graphs) + ' Graphs')
count = 0

gs = gridspec.GridSpec((len(led_df))+1, len(pd_df)+1)
fig = plt.figure(figsize=(60,30))

df_save = pd.DataFrame(columns=pd_df.Wavelength)

for index_led, led in led_df.iterrows():
    print("______________________________________")
    print(led.Wavelength)
    areas = []
    for index_pd, pd in pd_df.iterrows():
        print(pd.Wavelength)

        #Plot the LED and PD
        ax = fig.add_subplot(gs[count])

        S1 = spb.spd_builder(peakwl=[led.Wavelength], fwhm=[led.FWHM])
        S2 = spb.spd_builder(peakwl=[pd.Wavelength], fwhm=[pd.FWHM])

        lx.SPD(S1).plot(ax, color=led.Hex_Code)
        lx.SPD(S2).plot(ax, color=pd.Hex_Code, linestyle ='--')

        #Calculate and Plot Area between the curves
        l1, l2 = ax.lines[0], ax.lines[1]
        x1, y1 = l1.get_xydata().T
        x2, y2 = l2.get_xydata().T
        area_pd = np.trapz(y2, x2)

        xmin = max(x1.min(), x2.min())
        xmax = min(x1.max(), x2.max())
        x = np.linspace(xmin, xmax, 100)
        y1 = np.interp(x, x1, y1)
        y2 = np.interp(x, x2, y2)
        y = np.minimum(y1, y2)

        ax.fill_between(x, y, color="black", alpha=0.3) #Plot

        area = np.trapz(y, x)#Calculate Area
        areas.append(area / area_pd)
        ax.text(0.05, 0.95, f'Overlap: {area:.3f}', color='black', ha='left', va='top', transform=ax.transAxes)

        led_str = str(led)+"nm LED"
        pd_str = str(pd)+"nm PD"

        """Graph Formatting"""
        ax.set_ylabel('Relative Radiant Intensity [A.U.]')
        # label y axis
        if ax.get_subplotspec().is_first_col():
            ax.set_ylabel(led.Wavelength)

        # label x axis
        if ax.get_subplotspec().is_first_row():
            ax.set_title(pd.Wavelength)

        if ax.get_subplotspec().is_last_row():
            ax.set_xlabel('Wavelength(nm)')

        #Got to next plot
        count = count + 1

    """Final Plot to combine theory values"""
    print(led.Wavelength)
    print(air_df.loc[air_df['LED'] == int(led.Wavelength)].head())

    exp_plot_df = air_df.loc[air_df['LED'] == int(led.Wavelength)]
    #exp_plot_df = exp_plot_df.loc[air_df['Filter'] == 0.0]
    exp_plot_df = exp_plot_df.drop(['LED', 'timestamp'], axis=1)
    exp_plot_df.columns = exp_plot_df.columns.str.rstrip('_counts')

    #Calculate bias from 0 values
    zero_indexes = [i for i, v in enumerate(areas) if v < 0.001]
    non_zero_indexes = [i for i, v in enumerate(areas) if v >= 0.001]
    bias_arr = [areas[i] for i in zero_indexes]
    print(bias_arr)
    if(len(bias_arr)==0):
        bias = 0
    else:
        bias = sum(bias_arr) / len(bias_arr)

    #Calculate Scaling Factor
    """# Experimental
    x1 = list(map(int, exp_plot_df.columns.tolist()))
    y1 = exp_plot_df.iloc[0].tolist()
    # Theory
    x0 = list(map(int, exp_plot_df.columns.tolist()))
    y0 = areas

    # x1, y1, x0, y0=x1[non_zero_indexes],y1[:2],x0[:2],y0[:2]
    x1 = [x1[i] for i in non_zero_indexes]
    y1 = [y1[i] for i in non_zero_indexes]
    x0 = [x0[i] for i in non_zero_indexes]
    y0 = [y0[i] for i in non_zero_indexes]

    def target(x):
        # Interpolate set 1 onto grid of set 0 while shifting it by x.
        y0interp = np.interp(x0, x1, (y0 * x) + bias)
        # Compute RMS error between the two data.
        return np.sqrt(np.sum((y1 - y0interp) ** 2.))

    result = minimize(target, method="BFGS", x0=[0.25])  # , bounds=[(-0.2, 0.2)]) # bounds work with some methods only
    print(result)"""
    #print(exp_plot_df.head())
    sf_idx = exp_plot_df.iloc[0].tolist().index(max(exp_plot_df.iloc[0].tolist()))
    sf = exp_plot_df.iloc[0].tolist()[sf_idx]/areas[sf_idx]
    print(sf,sf_idx)

    #Plot Final fig
    ax = fig.add_subplot(gs[count])

    #Experimental
    for index, row in exp_plot_df.iterrows():
        print(row)
        bias_arr.extend(row[zero_indexes].tolist())
        ax.scatter(list(map(int, exp_plot_df.columns.tolist())), row.tolist(), marker='x', color='red')


    #Theory
    ax2 = ax.twinx()
    ax2.scatter(pd_df.Wavelength, areas, marker='.', color='blue', label='Theory')
    ax2.set_ylim([0, 1])


    #Scaled Theory
    ax.scatter(list(map(int, exp_plot_df.columns.tolist())), [x*sf+bias for x in areas], marker='*', color='green', label ='Scaled')
    """x0 = list(map(int, exp_plot_df.columns.tolist()))
    y0 = areas
    x0 = [x0[i] for i in zero_indexes]
    y0 = [y0[i] for i in zero_indexes]
    ax.scatter(x0, [x+bias for x in y0], marker='*', color='green')"""
    ax.legend()
    ax2.legend(loc=0)

    # Got to next plot - extra figure
    count = count + 1
    #df_save = df_save.append({'LED':led.Wavelength}|dict(zip(list(map(int, exp_plot_df.columns.tolist())),[x*sf+bias for x in areas])), ignore_index=True)
    #Save Df with PDs
    #df_save.to_csv('Data/Theory.csv')

fig.savefig("theory_graphs.pdf", bbox_inches='tight')
print('Done!')