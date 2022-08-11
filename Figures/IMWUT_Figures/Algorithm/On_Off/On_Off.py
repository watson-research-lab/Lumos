import pandas as pd
from Data.pull_data import process_df
import matplotlib.pyplot as plt
plt.style.use('../../../fig_formatting.mplstyle')

spec1 = pd.read_csv("../../../../Data/IMWUT_Data/ON_OFF/spec_1.csv", usecols = ['1', '2', '5'])
spec1 = process_df(spec1)
spec1 = spec1.sort_values('timestamp')
spec1 = spec1.reindex()

spec1 = spec1[200:-150]

fig = plt.figure(figsize=(10,6))
plt.plot(spec1['timestamp'], spec1['445_counts'], label = 'Lumos 1', color='b')

#plt.ylim(bottom =0, top=65355)
plt.xlabel('Time')
#plt.xticks([-15,0,15,30,45,60,75])
plt.ylabel('Spectral Response (Counts)')

plt.legend()
plt.show()

fig.savefig("on_off.pdf", bbox_inches='tight')
