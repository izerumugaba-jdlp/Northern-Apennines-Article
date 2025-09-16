# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 00:57:10 2025

@author: jdlpizerumug
"""

import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap, BoundaryNorm

# Importing variables already calculated in the other file (both files must be stored in the same folder)
from Models_He_isotopic_ratios_HeR_vs_DC_himu import F_SCLM, F_SCLM_min, F_SCLM_max, F_mix, F_SCLM_GM, F_HIMU
from Models_He_isotopic_ratios_HeR_vs_DC_himu import RRa_SCLM_sb_xage, RRa_SCM, RRa_HIMU
from Models_He_isotopic_ratios_HeR_vs_DC_himu import HeR_SCLM_sb_xage, HeR_mix, HeR_SCM, HeR_HIMU
from Models_He_isotopic_ratios_HeR_vs_DC_himu import DC_SCLM, DC_SCLM_min, DC_SCLM_max, DC_mix, DC_HIMU


# Variables
he3_flux = np.arange(1e-3, 5, 0.01) * 10**4                # 3He flux in atoms/m²/s (X-axis), set step 0.01 to smoothen, 0.05 to quick visual
Ra = 1.4 * 10**-6
he3_he4_ratios = np.flip(np.arange(1e-3, 8, 0.01) * Ra)    # 3He/4He ratios (Y-axis); flipped for image representation purpuses later
he4_he3_st_mantle = 1 / he3_he4_ratios           # 4He/3He mantle ratios (Y-axis)

he4_he3_phncryst = 1 / (0.93 * Ra)

JHe_1_whc = (1.70 * 10**10) / 20  # 4He flux from crustal radiogenic production atoms/m²/s

# Initialize DC as an empty 2D array
DC = np.zeros((len(he4_he3_st_mantle), len(he3_flux))) #number of rows for Y, number of columns for X

# Computing DC values using loops (we enumerate to extract indices as well as values)
for i, he3_f in enumerate(he3_flux):
    for j, he4_he3 in enumerate(he4_he3_st_mantle):
        DC[j, i] = ((he4_he3_phncryst * he3_f) - (he4_he3 * he3_f)) / JHe_1_whc  # Compute DC

# DataFrame from the computed array of values (DC)
df_DC_index= [round(i, 2) for i in (he3_he4_ratios/Ra)]
df_DC_columns= [round(j, 2) for j in (he3_flux / (10**4))]
df_DC = pd.DataFrame(data=DC, index= df_DC_index, columns= df_DC_columns)

# The DataFrame printed
# print(df_DC)
print()

#PLOTTING
plt.figure(figsize=(8, 6))

# Creating masks for values < 0 and those > 0
mask_negative = df_DC < 0
mask_positive = ~mask_negative

# Defining the colormap for negative values (e.g., solid color)
negative_cmap = ListedColormap(['black'])

# Plotting the negative values
sns.heatmap(df_DC, mask=mask_positive, cmap=negative_cmap, cbar=False, annot=False)

# Creating a custom colormap for positives
# cmap options: viridis, Spectral, plasma, flare, [solid]s, Accent, Paired, Pastel1, Pastel2, Set1_r, RdGy_r, PuOr_r, RdBu_r
cmap_positive = plt.cm.YlGnBu_r     # colormap
boundaries = np.arange(0, (math.ceil(DC.max()/5)*5)+5, 5)  # Defining the sharp breaks in color
norm_colors = BoundaryNorm(boundaries, cmap_positive.N)  # Normalizing the color scale to the defined boundaries

# Plotting the positive values using the standard colormap
heatmap_positives= sns.heatmap(df_DC, mask=mask_negative, cmap=cmap_positive, norm=norm_colors, cbar=True, 
                               cbar_kws={'ticks': boundaries, "label": "Delaminated Crust Thickness (km)"}, annot=False)

# Indicating results of certain case studies (Obtained DC, given a certain 3He Flux & 3He/4He)

# X and Y values
xvalues= he3_flux
yvalues= he4_he3_st_mantle

# points to indicate
F_3He_cases= [F_SCLM, F_SCLM_min, F_SCLM_max, F_mix, F_SCLM_GM, F_HIMU]
HeR_cases= [HeR_SCLM_sb_xage, HeR_SCLM_sb_xage, HeR_SCLM_sb_xage, HeR_mix, HeR_SCM, HeR_HIMU]

# Conversion of true X and Y values onto heatmap indices, and then extracting the index location of point to indicate
scatter_x_idx = np.searchsorted(xvalues, F_3He_cases)
scatter_y_idx = np.searchsorted(yvalues, HeR_cases)

# Plotting the points
plt.scatter(scatter_x_idx+0.5, scatter_y_idx+0.5, marker= "s", s= 100, c="yellow", edgecolors="black") #+0.5 for proper centering

# Labels
plt.xlabel("$\mathrm{^3He}$ Flux (atoms/cm²/s)", fontweight= "normal", fontsize=13)
plt.ylabel("$\mathrm{^3He/^4He}$ (R/Ra)", fontweight='normal', fontsize= 13)

# Setting x and y ticks positions and labels
x_ticks_positions = np.arange(0, len(xvalues), int(len(xvalues)/10))             # every 10 values
y_ticks_positions = np.arange(0, len(yvalues), int(len(yvalues)/8))              # every 20 values
x_ticks_labels = np.round([(he3_flux/10000)[i] for i in x_ticks_positions], decimals=1)       # label with a value located in the index position as the tick_position...
y_ticks_labels= np.round([(he3_he4_ratios/Ra)[i] for i in y_ticks_positions], decimals=1)

# Customising x-y-tick labels
plt.xticks(ticks= x_ticks_positions, labels= x_ticks_labels, rotation=0)
plt.yticks(ticks= y_ticks_positions, labels= y_ticks_labels, rotation=0)

plt.savefig(f'Model_3He-flux_vs_3He4He_vs_DC.svg', format='svg', bbox_inches='tight')


plt.show()

