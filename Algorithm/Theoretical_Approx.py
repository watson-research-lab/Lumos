import numpy as np
from matplotlib import pyplot as plt
import luxpy as lx
import luxpy.toolboxes.spdbuild as spb
from colormap import rgb2hex

def wavelength_to_hex(wavelength, gamma=0.8):

    '''This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).
    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''

    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    R *= 255
    G *= 255
    B *= 255
    hex = rgb2hex(int(R), int(G), int(B))
    return (hex)

class Theoretical_Approx:
    def __init__(self, led_df, pd_df):
        self.led_cw = led_df.Wavelength
        self.led_fwhw = led_df.FWHM
        self.pd_cw = pd_df.Wavelength
        self.pd_fwhw = pd_df.FWHM


    def theory_approx(self):

        areas_final = []

        for led_cw, led_fwhm in zip(self.led_cw, self.led_fwhw):
            print("\n______________" + str(led_cw) + "______________")
            areas = []
            for pd_cw, pd_fwhm in zip(self.pd_cw, self.pd_fwhw):
                print(str(pd_cw), end=' ')

                fig_ta = plt.figure(figsize=(10, 5))
                ax = fig_ta.add_subplot(111)
                # Plot the LED and PD
                S1 = spb.spd_builder(peakwl=[led_cw], fwhm=[np.multiply(led_fwhm, 2)])
                S2 = spb.spd_builder(peakwl=[pd_cw], fwhm=[np.multiply(pd_fwhm, 2)])

                lx.SPD(S1).plot(ax, color=wavelength_to_hex(led_cw))
                lx.SPD(S2).plot(ax, color=wavelength_to_hex(pd_cw), linestyle='--')

                # Calculate and Plot Area between the curves
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

                ax.fill_between(x, y, color="black", alpha=0.3)  # Plot

                area = np.trapz(y, x)  # Calculate Area
                areas.append(area / area_pd)
                #print(areas)
                ax.text(0.05, 0.95, f'Overlap: {area:.3f}', color='black', ha='left', va='top', transform=ax.transAxes)
            areas_final.append(areas)

        #print('\n',areas_final)
        return areas_final