import pandas as pd
from matplotlib import gridspec, pyplot as plt
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

from scipy.stats.stats import pearsonr
plt.style.use('../../fig_formatting.mplstyle')

print('------------------------Creating Spectrum Graphs------------------------')

#Import LEDs and PDs
data = pd.read_csv("Theory.csv")
pd_df = pd.read_csv("../../../Spectral_Response_of_Medium/Data/PDs.csv")

#Graphs
total_graphs = 4 * 2
print('Creating ' + str(total_graphs) + ' Graphs')
count = 0

exp_arr=[]
the_arr=[]

gs = gridspec.GridSpec(2, 4)
fig = plt.figure(figsize=(30,12))

df_save = pd.DataFrame(columns=pd_df.Wavelength)

for i, led in data.iterrows():
    print("______________________________________")
    print(int(led.LED))
    #Plot Final fig
    ax = fig.add_subplot(gs[count])

    exp = eval(led.Experimental)
    exp = [(x/max(exp))*44000 for x in exp]

    the = eval(led.Theory)
    the = [(x/max(the))*44000 for x in the]

    #Experimental
    ax.scatter(pd_df.Wavelength.tolist(),exp, marker='o', s=150, color='red', label ='Exp')

    #Scaled Theory
    ax.scatter(pd_df.Wavelength.tolist(),the, marker='v', s=150, color='blue', label ='Theory')

    if ax.get_subplotspec().is_first_col():
        ax.set_ylabel('Spectral Response (Counts)')
        ax.set_yticks([0,10000,20000,30000,40000])

    if not ax.get_subplotspec().is_first_col():
        ax.set_yticks([],[])

    if ax.get_subplotspec().is_last_row():
        ax.set_xticks(pd_df.Wavelength)
        ax.set_xticklabels(ax.get_xticks(), rotation=45)
        ax.set_xlabel('Wavelength(nm)')

    if not ax.get_subplotspec().is_last_row():
        ax.set_xticks([],[])

    ax.legend()
    ax.set_title(str(int(led.LED))+'nm LED')

    count = count + 1
    exp_arr = exp_arr + exp
    the_arr = the_arr + the

print('Pearson: ',pearsonr(exp_arr,the_arr))

plt.show()

fig.savefig("exp_the.pdf", bbox_inches='tight')
print('Done!')