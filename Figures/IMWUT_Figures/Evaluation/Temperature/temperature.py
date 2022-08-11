import numpy as np
import pandas as pd

from Data.pull_data import process_df

print('------------------------Temperature Figure------------------------')
import matplotlib.pyplot as plt
plt.style.use('../../../../Figures/fig_formatting.mplstyle')

spec1_heat = pd.read_csv("../../../../Data/IMWUT_Data/temp_fluid_exp/Heat/spec_1.csv", usecols = ['1','2','5'])
spec1_heat = process_df(spec1_heat)
spec1_heat = spec1_heat[2875:3400]
spec1_heat['temp'] = np.linspace(-15,70,len(spec1_heat))

spec2_heat = pd.read_csv("../../../../Data/IMWUT_Data/temp_fluid_exp/Heat/spec_2.csv", usecols = ['1','2','5'])
spec2_heat = process_df(spec2_heat)
spec2_heat = spec2_heat[2875:3400]
spec2_heat['temp'] = np.linspace(-15,70,len(spec2_heat))

spec3_heat = pd.read_csv("../../../../Data/IMWUT_Data/temp_fluid_exp/Heat/spec_3.csv", usecols = ['1','2','5'])
spec3_heat = process_df(spec3_heat)
spec3_heat = spec3_heat[2875:3400]
spec3_heat['temp'] = np.linspace(-15,70,len(spec3_heat))

spec1_cold = pd.read_csv("../../../../Data/IMWUT_Data/temp_fluid_exp/Cold/spec_1.csv", usecols = ['1','2','5'])
spec1_cold = process_df(spec1_cold)
spec1_cold = spec1_cold[spec1_cold['timestamp'].between(1635708210000,16357116920000)]
spec1_cold = spec1_cold[300:]
spec1_cold['temp'] = np.linspace(73,0,len(spec1_cold))
print(spec1_cold)


spec2_cold = pd.read_csv("../../../../Data/IMWUT_Data/temp_fluid_exp/Cold/spec_2.csv", usecols = ['1','2','5'])
spec2_cold = process_df(spec2_cold)
spec2_cold = spec2_cold[spec2_cold['timestamp'].between(1635708210000,16357116920000)]
spec2_cold = spec2_cold[100:]
spec2_cold['temp'] = np.linspace(73,0,len(spec2_cold))
print(spec2_cold)


spec3_cold = pd.read_csv("../../../../Data/IMWUT_Data/temp_fluid_exp/Cold/spec_3.csv", usecols = ['1','2','5'])
spec3_cold = process_df(spec3_cold)
spec3_cold = spec3_cold[spec3_cold['timestamp'].between(1635708210000,16357116920000)]
spec3_cold = spec3_cold[2800:]
spec3_cold['temp'] = np.linspace(73,0,len(spec3_cold))
print(spec3_cold)


fig = plt.figure(figsize=(10,6))
plt.plot(spec1_heat['temp'], spec1_heat['445_counts']+20000, label = 'Lumos 1', color='b')
plt.plot(spec2_heat['temp'], spec2_heat['445_counts']+20000, label = 'Lumos 2', color='g')
plt.plot(spec3_heat['temp'], spec3_heat['445_counts']+20000, label = 'Lumos 3', color='r')

#plt.plot(spec1_cold['temp'], spec1_cold['445_counts'], color='b')
#plt.plot(spec2_cold['temp'], spec2_cold['445_counts'], color='g')
#plt.plot(spec3_cold['temp'], spec3_cold['445_counts']- (spec3_heat['445_counts'].iloc[0]) , color='r')
#plt.ylim(bottom =0, top=65355)
plt.xlabel('Temperature ($^\circ C$)')
plt.xticks([-15,0,15,30,45,60,75])
plt.ylabel('Spectral Response(Counts)')

plt.legend()

print((spec1_heat['445_counts'].iloc[-1])-(spec1_heat['445_counts'].iloc[0]))
print((spec2_heat['445_counts'].iloc[-1])-(spec2_heat['445_counts'].iloc[0]))
print((spec3_heat['445_counts'].iloc[-1])-(spec3_heat['445_counts'].iloc[0]))

fig.savefig("temp.pdf", bbox_inches='tight')
