import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.style.use('../../fig_formatting.mplstyle')


Kp_0_1 = pd.read_csv("../../IMWUT_Data/Intensity_Calibration/Kp_0_1.csv", delimiter=',', header=None)
Kp_0_01 = pd.read_csv("../../IMWUT_Data/Intensity_Calibration/Kp_0_01.csv", delimiter=',', header=None)
Kp_0_001 = pd.read_csv("../../IMWUT_Data/Intensity_Calibration/Kp_0_001.csv", delimiter=',', header=None)
Kp_0_0001 = pd.read_csv("../../IMWUT_Data/Intensity_Calibration/Kp_0_0001.csv", delimiter=',', header=None)

Kp_0_1.columns = ['LED', 'Steps', 'Intensity']
Kp_0_01.columns = ['LED', 'Steps', 'Intensity']
Kp_0_001.columns = ['LED', 'Steps', 'Intensity']
Kp_0_0001.columns = ['LED', 'Steps', 'Intensity']

Kp_0_1['LED'] = Kp_0_1['LED'].str.extract('(\d+)', expand=False)
Kp_0_1['Steps'] = Kp_0_1['Steps'].str.extract('(\d+)', expand=False)
Kp_0_1['Intensity'] = Kp_0_1['Intensity'].str.extract('(\d+)', expand=False)

Kp_0_01['LED'] = Kp_0_01['LED'].str.extract('(\d+)', expand=False)
Kp_0_01['Steps'] = Kp_0_01['Steps'].str.extract('(\d+)', expand=False)
Kp_0_01['Intensity'] = Kp_0_01['Intensity'].str.extract('(\d+)', expand=False)

Kp_0_001['LED'] = Kp_0_001['LED'].str.extract('(\d+)', expand=False)
Kp_0_001['Steps'] = Kp_0_001['Steps'].str.extract('(\d+)', expand=False)
Kp_0_001['Intensity'] = Kp_0_001['Intensity'].str.extract('(\d+)', expand=False)

Kp_0_0001['LED'] = Kp_0_0001['LED'].str.extract('(\d+)', expand=False)
Kp_0_0001['Steps'] = Kp_0_0001['Steps'].str.extract('(\d+)', expand=False)
Kp_0_0001['Intensity'] = Kp_0_0001['Intensity'].str.extract('(\d+)', expand=False)

Kp_0_1['Steps'] = Kp_0_1['Steps'].astype('int')
Kp_0_01['Steps'] = Kp_0_01['Steps'].astype('int')
Kp_0_001['Steps'] = Kp_0_001['Steps'].astype('int')
Kp_0_0001['Steps'] = Kp_0_0001['Steps'].astype('int')

Kp_0_1['Intensity'] = Kp_0_1['Intensity'].astype('int')
Kp_0_01['Intensity'] = Kp_0_01['Intensity'].astype('int')
Kp_0_001['Intensity'] = Kp_0_001['Intensity'].astype('int')
Kp_0_0001['Intensity'] = Kp_0_0001['Intensity'].astype('int')

print(Kp_0_1.groupby('LED')['Steps'].max().mean())
print(Kp_0_01.groupby('LED')['Steps'].max().mean())
print(Kp_0_001.groupby('LED')['Steps'].max().mean())
print(Kp_0_0001.groupby('LED')['Steps'].max().mean())

print(Kp_0_1.groupby('LED')['Steps'].max().std())
print(Kp_0_01.groupby('LED')['Steps'].max().std())
print(Kp_0_001.groupby('LED')['Steps'].max().std())
print(Kp_0_0001.groupby('LED')['Steps'].max().std())


Kp_0_1 = Kp_0_1.loc[Kp_0_1['LED'] == '5']
Kp_0_01 = Kp_0_01.loc[Kp_0_01['LED'] == '5']
Kp_0_001 = Kp_0_001.loc[Kp_0_001['LED'] == '5']
Kp_0_0001 = Kp_0_0001.loc[Kp_0_0001['LED'] == '5']

print(Kp_0_1.head())


fig = plt.figure(figsize=(10,6))
plt.plot(Kp_0_1['Steps'], Kp_0_1['Intensity'], label = '0.1', color = 'lightgrey')
plt.plot(Kp_0_1['Steps']+22, Kp_0_1['Intensity'],color = 'lightgrey')
plt.plot(Kp_0_1['Steps']+44, Kp_0_1['Intensity'],color = 'lightgrey')
plt.plot(Kp_0_1['Steps']+66, Kp_0_1['Intensity'],color = 'lightgrey')
plt.plot(Kp_0_01['Steps'], Kp_0_01['Intensity'], label = '0.01', color='blue')
plt.plot(Kp_0_001['Steps'], Kp_0_001['Intensity'], label = '0.001', color='red')
plt.plot(Kp_0_0001['Steps'], Kp_0_0001['Intensity'], label = '0.0001', color = 'green')

plt.plot(Kp_0_01['Steps'].iat[-1], Kp_0_01['Intensity'].iat[-1], marker="*", markersize=20, color="blue")
plt.plot(Kp_0_001['Steps'].iat[-1], Kp_0_001['Intensity'].iat[-1], marker="*", markersize=20, color="red")


plt.xlim(left =0, right=75)
plt.xlabel('Steps')
#plt.xticks([-15,0,15,30,45,60,75])
plt.ylabel('Intensity')

plt.legend()

fig.savefig("Intensity.pdf", bbox_inches='tight')


