print('------------------------IMWUT Figures------------------------')
# Import module luxpy.spdbuild:
import numpy as np
import luxpy as lx
import luxpy.toolboxes.spdbuild as spb
import matplotlib.pyplot as plt
plt.style.use('../../../Figures/fig_formatting.mplstyle')

#https://www.tandfonline.com/doi/pdf/10.1080/15502724.2018.1518717
#TODO: Make the Graphs automatic

"""------------------------LED Spectra------------------------"""
#TODO: Fix x axis range
#Set peak wavelengths:
peakwl = [415,450,470,515,545,590,630,680]#,830,850,890,935] #940
# Set Full-Width-Half-Maxima:
fwhm = np.multiply([13.7,20,20,30,100,20,20,20],2)#9,20,40,25 #20

S = spb.spd_builder(peakwl = peakwl, fwhm = fwhm)
# Plot component spds:
lx.SPD(S).plot()
plt.ylabel('Normalized Intensity')
plt.legend(('415','445','470','515','555','590','630','680'))#'940'))#,'830','850','890','935'))
plt.savefig("LED_Spectra.pdf",bbox_inches='tight')
plt.show()

"""------------------------PD Spectra------------------------"""
#TODO: Add NIR PD
# Set peak wavelengths:
peakwl = [415,445,480,515,555,590,630,680]
# Set Full-Width-Half-Maxima:
fwhm = np.multiply([26,30,36,39,39,40,50,52],2)

S = spb.spd_builder(peakwl = peakwl, fwhm = fwhm)
#print(S)
# Plot component spds:
lx.SPD(S).plot()
plt.ylabel('Normalized Intensity')
plt.legend(('415','445','480','515','555','590','630','680'))
plt.savefig("PD_Spectra.pdf",bbox_inches='tight')
plt.show()

print('-------------------------------------------------------------')


"""------------------------Green Example------------------------"""
#TODO: Add NIR PD
# Set peak wavelengths:
peakwl = [515]
# Set Full-Width-Half-Maxima:
fwhm = np.multiply([39],2)

S = spb.spd_builder(peakwl = peakwl, fwhm = fwhm)
#print(S)
# Plot component spds:
lx.SPD(S).plot(color = '#1fff00', label='515')
half_max = 0.5

plt.hlines(y = 0.5, xmin=493 , xmax = 536, color = 'blue', linestyle='--', label = 'FWHM')

plt.axvline(x = 515, color = 'black', linestyle='--', label = 'CW')
plt.ylabel('Normalized Intensity')
plt.legend()
plt.savefig("Green_Spectra.pdf",bbox_inches='tight')
plt.show()

print('-------------------------------------------------------------')
