import numpy as np
import pandas as pd
from matplotlib import gridspec, pyplot as plt
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
import luxpy as lx
import luxpy.toolboxes.spdbuild as spb

from Spectral_Response_of_Medium.Data.pull_data import process_df

plt.style.use('../../fig_formatting.mplstyle')

#exp_df = pd.read_csv("Data/Experimental_Mediums.csv")

print('------------------------Creating Spectrum Graphs------------------------')

#Import LEDs and PDs
led_df = pd.read_csv("../../../Spectral_Response_of_Medium/Data/LEDs_watch.csv")
pd_df = pd.read_csv("../../../Spectral_Response_of_Medium/Data/PDs.csv")

#Import Air Medium
air_df = pd.read_csv("../../../Spectral_Response_of_Medium/Data/IMWUT_Data/Medium/air.csv", usecols = ['1', '2', '5'])
air_df = process_df(air_df)
air_df = air_df.sort_values('timestamp')
air_df = air_df.iloc[85:]
led_order = [530,940,660,470,568,450,633,415,599]
xx=air_df.iloc[0]['timestamp']

i=0
if i != 1:
    for led in led_order:
        air_df.loc[air_df.timestamp.between(xx+ 1000,xx+ 26000), 'LED'] = led
        xx=xx+30000
    i=i+1
plt.show()
air_df = air_df[air_df['LED'].notna()]
air_df.LED = air_df.LED.astype(int)

exp_df = air_df
print(exp_df)
#Set Up the Graphs
total_graphs = len(led_df) * len(pd_df) +len(led_df)
print(total_graphs)
count = 0

gs = gridspec.GridSpec(2,4)
fig = plt.figure(figsize=(28,10))

df_save = pd.DataFrame(columns=pd_df.Wavelength)
print(df_save.head())

for index_led, led in led_df.iterrows():
    print("______________________________________")
    print(led.Wavelength)
    areas = []
    if(led.Wavelength == 530):
        for index_pd, pd in pd_df.iterrows():
            print(pd.Wavelength)


            #Plot the LED and PD
            ax = fig.add_subplot(gs[count])

            S1 = spb.spd_builder(peakwl=[led.Wavelength], fwhm=[np.multiply(led.FWHM, 2)])
            S2 = spb.spd_builder(peakwl=[pd.Wavelength], fwhm=[np.multiply(pd.FWHM, 2)])
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
            ax.text(0.05, 0.95, f'Overlap: {area:.3f}', color='black', ha='left', va='top', transform=ax.transAxes, fontsize=20)

            led_str = str(led.Wavelength)+"nm LED"
            #print(led_str)
            pd_str = str(pd.Wavelength)+"nm PD"
            #ax.legend([led_str,pd_str])
            ax.set_title(pd_str)

            """Graph Formatting"""
            ax.set_ylabel('')
            ax.set_xlabel('')
            # label y axis
            if ax.get_subplotspec().is_first_col():
                #ax.set_ylabel(led.Wavelength)
                ax.set_ylabel('Relative Intensity [A.U.]')

            # label x axis
            #if ax.is_first_row():
                #ax.set_title(pd.Wavelength)

            if ax.get_subplotspec().is_last_row():
                ax.set_xlabel('Wavelength(nm)')

            #ax.set_ylabel('Relative Intensity [A.U.]')
            #rax.set_xlabel('Wavelength(nm)')

            #Got to next plot
            count = count + 1


        """Final Plot to combine theory values"""
        print(exp_df)
        exp_plot_df = exp_df.loc[exp_df['LED'] == (int(led.Wavelength))]
        print(exp_plot_df)
        #exp_plot_df = exp_plot_df.loc[exp_df['Filter'] == 0.0]
        exp_plot_df = exp_plot_df.drop(['LED', 'timestamp'], axis=1)
        exp_plot_df.columns = exp_plot_df.columns.str.rstrip('_counts')

        #Calculate bias from 0 values
        zero_indexes = [i for i, v in enumerate(areas) if v < 0.001]
        non_zero_indexes = [i for i, v in enumerate(areas) if v >= 0.001]
        print(exp_plot_df)
        bias_arr = [exp_plot_df.iloc[0][i] for i in zero_indexes]
        if (len(bias_arr) == 0):
            bias = 0
        else:
            bias = sum(bias_arr) / len(bias_arr)

        sf_idx = exp_plot_df.iloc[0].tolist().index(max(exp_plot_df.iloc[0].tolist()))
        sf = exp_plot_df.iloc[0].tolist()[sf_idx]/areas[sf_idx]
        #print(sf,sf_idx)

        #Plot Final fig
        fig2 = plt.figure(figsize=(7, 5))
        ax2 = fig2.add_subplot(111)


        #Experimental
        for index, row in exp_plot_df.iterrows():
            bias_arr.extend(row[zero_indexes].tolist())
            #ax2.scatter(list(map(int, exp_plot_df.columns.tolist())), row.tolist(), marker='x', color='red')

        #Theory
        ax3 = ax2.twinx()
        ax3.scatter(pd_df.Wavelength, areas, marker='s', color='blue', label='Theoretical')
        ax3.set_ylim([0, 1])
        print(bias)
        ax2.axhline(y=bias, color='red', linestyle='--', label = 'Leakage Cur')


        #Scaled Theory
        ax2.scatter(list(map(int, exp_plot_df.columns.tolist())), [x*sf+bias for x in areas], marker='^', color='green', label='Scaled')

        #ax2.set_ylim([0, 70000])

        ax2.set_xlabel('Wavelength(nm)')
        ax2.set_ylabel('Counts')
        ax3.set_ylabel('Relative Intensity [A.U.]')
        fig2.legend(bbox_to_anchor=(0.9, 0.9))

plt.show()
fig.savefig("green_theory_graph.pdf", bbox_inches='tight')
fig2.savefig("green_theory_graph_final.pdf", bbox_inches='tight')
