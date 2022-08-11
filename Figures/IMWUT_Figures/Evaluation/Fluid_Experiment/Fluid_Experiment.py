import numpy as np
import pandas as pd

from Data.pull_data import process_df

print('------------------------Temperature Figure------------------------')
import matplotlib.pyplot as plt
plt.style.use('../../../fig_formatting.mplstyle')

spec1 = pd.read_csv("../../../../Data/IMWUT_Data/temp_fluid_exp/Cold/spec_1.csv", usecols = ['1', '2', '5'])
spec1 = process_df(spec1)
spec1 = spec1.sort_values('timestamp')
spec1 = spec1[3700:4275]
spec1 = spec1[(((spec1['timestamp'] - spec1['timestamp'].iloc[1])/100000) < 1) | (((spec1['timestamp'] - spec1['timestamp'].iloc[1])/100000) >1.55)]
spec1 = spec1[(((spec1['timestamp'] - spec1['timestamp'].iloc[1])/100000) < 2.15) | (((spec1['timestamp'] - spec1['timestamp'].iloc[1])/100000) >2.6)]


spec2 = pd.read_csv("../../../../Data/IMWUT_Data/temp_fluid_exp/Heat/spec_2.csv", usecols = ['1', '2', '5'])
spec2 = process_df(spec2)
spec2 = spec2.sort_values('timestamp')
spec2 = spec2[3850:4425]
spec2 = spec2[(((spec2['timestamp'] - spec2['timestamp'].iloc[1])/100000) < 1) | (((spec2['timestamp'] - spec2['timestamp'].iloc[1])/100000) >1.58)]
spec2 = spec2[(((spec2['timestamp'] - spec2['timestamp'].iloc[1])/100000) < 2.15) | (((spec2['timestamp'] - spec2['timestamp'].iloc[1])/100000) >2.65)]


spec3 = pd.read_csv("../../../../Data/IMWUT_Data/temp_fluid_exp/Heat/spec_3.csv", usecols = ['1', '2', '5'])
spec3 = process_df(spec3)
spec3 = spec3.sort_values('timestamp')
spec3 = spec3[3500:4070]
spec3 = spec3[(((spec3['timestamp'] - spec3['timestamp'].iloc[1])/100000) < 1) | (((spec3['timestamp'] - spec3['timestamp'].iloc[1])/100000) >1.60)]
spec3 = spec3[(((spec3['timestamp'] - spec3['timestamp'].iloc[1])/100000) < 2.15) | (((spec3['timestamp'] - spec3['timestamp'].iloc[1])/100000) >2.65)]



fig = plt.figure(figsize=(10,6))
plt.plot((spec1['timestamp'] - spec1['timestamp'].iloc[1])/100000, spec1['445_counts']+20000, label = 'Lumos 1', color='b')
plt.plot((spec2['timestamp'] - spec2['timestamp'].iloc[1])/100000, spec2['445_counts']+20000, label = 'Lumos 2', color='g')
plt.plot((spec3['timestamp'] - spec3['timestamp'].iloc[1])/100000, spec3['445_counts']+20000, label = 'Lumos 3', color='r')

#plt.axvline(x=0.1, color='black', linestyle='--')
plt.axvline(x=0.8, color='black', linestyle='--',label='Spray')
plt.axvline(x=1.8, color='black', linestyle='--')
plt.axvline(x=2.7, color='black', linestyle='--')


#plt.ylim(bottom =0, top=65355)
plt.xlabel('Time (minutes)')
#plt.xticks([-15,0,15,30,45,60,75])
plt.ylabel('Spectral Response (counts)')

plt.legend()

print((spec1['445_counts'].iloc[-1])-(spec1['445_counts'].iloc[0]))
print((spec2['445_counts'].iloc[-1])-(spec2['445_counts'].iloc[0]))
print((spec3['445_counts'].iloc[-1])-(spec3['445_counts'].iloc[0]))

#plt.show()
fig.savefig("fluid.pdf", bbox_inches='tight')
