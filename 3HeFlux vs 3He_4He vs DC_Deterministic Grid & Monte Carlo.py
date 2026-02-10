# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 18:47:23 2026

@author: ijdpe
"""

# MODEL BEHAVIOUR AND ASSOCIATED UNCERTAINTY: DETERMINISTIC GRID AND MONTE CARLO

import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import seaborn as sns
from SALib.sample import saltelli
from SALib.analyze import sobol

# Importing variables already calculated in the other file
from Models_He_isotopic_ratios_HeR_vs_DC_himu import F_SCLM, F_SCLM_min, F_SCLM_max, F_mix, F_SCLM_GM, F_HIMU
from Models_He_isotopic_ratios_HeR_vs_DC_himu import RRa_SCLM_sb_xage, RRa_SCM, RRa_HIMU
from Models_He_isotopic_ratios_HeR_vs_DC_himu import HeR_SCLM_sb_xage, HeR_mix, HeR_SCM, HeR_HIMU
from Models_He_isotopic_ratios_HeR_vs_DC_himu import DC_SCLM, DC_SCLM_min, DC_SCLM_max, DC_mix, DC_HIMU


# --------------------------------
# 1. Constants
# --------------------------------
Ra = 1.4e-6
JHe_1_whc = (1.70e10) / 20  # atoms/m2/s  ; Crustal 4He production
he4_he3_phncryst = 1 / (0.93 * Ra)




# --------------------------------------
# 2. Deterministic grid analysis
# --------------------------------
grid_size= 1000                # Using a 100x100 grid for visualization
he3_he4_ratios_grid = np.flip(np.linspace(1e-3, 8, grid_size) * Ra) #3He/4He ratios (Y-axis); flipped for accurate image representation purpuses
he4_he3_st_mantle_grid = 1 / he3_he4_ratios_grid
he3_flux_grid = np.linspace(1e-03, 5, grid_size) * 1e4     
DC_grid = np.zeros((len(he4_he3_st_mantle_grid), len(he3_flux_grid)))

for i, F in enumerate(he3_flux_grid):
    for j, mantle_ratio in enumerate(he4_he3_st_mantle_grid):
        DC_grid[j, i] = ((he4_he3_phncryst * F) - (mantle_ratio * F)) / JHe_1_whc
        
# DataFrame from the computed array of values (DC_grid)
df_DC_grid_index= [round(i, 2) for i in (he3_he4_ratios_grid/Ra)]
df_DC_grid_columns= [round(j, 2) for j in (he3_flux_grid / (10**4))]
df_DC_grid = pd.DataFrame(data=DC_grid, index= df_DC_grid_index, columns= df_DC_grid_columns)

# The DataFrame printed
print(df_DC_grid)
print()



# ---------------------------------------------------
# 3. Plotting: Parameter space heatmap grid 
# ---------------------------------------------
plt.figure(figsize=(15, 5))

plt.subplot(1, 2, 1)

# Creating masks for values < 0 and those > 0
mask_negative = df_DC_grid <= 0
mask_positive = ~mask_negative

# Defining the colormap for negative values (e.g., solid color)
negative_cmap = ListedColormap(['black'])

# Plotting the negative values
sns.heatmap(df_DC_grid, mask=mask_positive, cmap=negative_cmap, cbar=False, annot=False)

# Creating a custom colormap for positives
# cmap options: viridis, Spectral, plasma, flare, [solid]s, Accent, Paired, Pastel1, Pastel2, Set1_r, RdGy_r, PuOr_r, RdBu_r
cmap_positive = plt.cm.RdBu_r     # colormap

boundaries = np.arange(0, (math.ceil(DC_grid.max()/5)*5)+5, 5)  # Defining the sharp breaks in color
norm_colors = BoundaryNorm(boundaries, cmap_positive.N)  # Normalizing the color scale to the defined boundaries

# Plotting the positive values using the standard colormap
heatmap_positives= sns.heatmap(df_DC_grid, mask=mask_negative, cmap=cmap_positive, norm=norm_colors, cbar=True, 
                               cbar_kws={'ticks': boundaries, "label": "Delaminated Crust Thickness (km)"}, annot=False)

# Highlighting the main model outcomes based on parameters constrained in section 3.2
# ------------------------------------------------ 
# X and Y values
xvalues= he3_flux_grid
yvalues= he4_he3_st_mantle_grid

# points to indicate
F_3He_cases= [F_SCLM, F_SCLM_min, F_SCLM_max, F_mix, F_SCLM_GM, F_HIMU]
HeR_cases= [HeR_SCLM_sb_xage, HeR_SCLM_sb_xage, HeR_SCLM_sb_xage, HeR_mix, HeR_SCM, HeR_HIMU]

# Conversion of true X and Y values onto heatmap indices, and then extracting the index location of point to indicate
scatter_x_idx = np.searchsorted(xvalues, F_3He_cases)
scatter_y_idx = np.searchsorted(yvalues, HeR_cases)

# Plotting the points
plt.scatter(scatter_x_idx+0.5, scatter_y_idx+0.5, marker= "s", s= 100, c="yellow", edgecolors="black") #+0.5 for proper centering
# -------------------------------------------------------------

# Labels
plt.xlabel("$\mathrm{^3He Flux (atoms/cm^2/s)}$", fontweight= "normal", fontsize=13)
plt.ylabel("Initial $\mathrm{^3He/^4He}$ (Ra)", fontweight= "normal", fontsize= 13)
# plt.xlabel(r"$^3He$ Flux (atoms/cm²/s)", fontsize=13)
# plt.ylabel(r"$^3He/^{4}He$ (Ra)", fontsize= 13)

# Setting x and y ticks positions and labels
x_ticks_positions = np.arange(0, len(xvalues), int(len(xvalues)/10))             # every 10 values
y_ticks_positions = np.arange(0, len(yvalues), int(len(yvalues)/8))              # every 20 values
x_ticks_labels = np.round([(he3_flux_grid/10000)[i] for i in x_ticks_positions], decimals=1)       # label with a value located in the index position as the tick_position...
y_ticks_labels= np.round([(he3_he4_ratios_grid/Ra)[i] for i in y_ticks_positions], decimals=1)

# Customising x-y-tick labels
plt.xticks(ticks= x_ticks_positions, labels= x_ticks_labels, rotation=0)
plt.yticks(ticks= y_ticks_positions, labels= y_ticks_labels, rotation=0)




# ---------------------------------------------------------------
# 4. Monte Carlo error propagation (Uniform sampling)
# -------------------------------------------------------
n_samples_MC = 100000
# he3_he4_ratios_MC = np.random.uniform(2.3, 6.7, n_samples_MC) * Ra
# he4_he3_st_mantle_MC = 1 / he3_he4_ratios_MC

he3_flux_MC = np.random.uniform(0.25, 5, n_samples_MC) * 1e4
he3_he4_ratios_MC = np.random.uniform(2.3, 6.7, n_samples_MC) * Ra
he4_he3_st_mantle_MC = 1 / he3_he4_ratios_MC

DC_MC = ((he4_he3_phncryst * he3_flux_MC) - (he4_he3_st_mantle_MC * he3_flux_MC)) / JHe_1_whc

# Statistics
mean_DC = np.mean(DC_MC)
median_DC = np.median(DC_MC)
std_DC = np.std(DC_MC)
ci95 = np.percentile(DC_MC, [2.5, 97.5])
ci80 = np.percentile(DC_MC, [10, 90])




# --------------------------------
# 6. Plotting: Monte Carlo PDF
# --------------------------------

plt.subplot(1, 2, 2)
plt.hist(DC_MC, bins=500, density=True, color='orange', alpha=0.7)
plt.axvline(mean_DC, color='red', linestyle='--', label=f'Mean={mean_DC:.2f}')
plt.axvline(median_DC, color='blue', linestyle='--', label=f'Median={median_DC:.2f}')
plt.xlabel('DC (km)', fontsize= 13)
plt.ylabel('Probability Density', fontsize= 13)
# plt.title('Monte Carlo PDF')
plt.legend()
plt.savefig('deterministic grid & monte carlo.tiff', format='tiff', bbox_inches='tight')




# --------------------------------
# 5. Sobol sensitivity analysis
# --------------------------------

# Defining problem for SALib
problem = {
    'num_vars': 2,
    'names': ['he3_flux', 'he4_he3_mantle'],
    'bounds': [[0.25e4, 5e4], [min(he4_he3_st_mantle_MC), max(he4_he3_st_mantle_MC)]]
}

# Saltelli sampling
param_values = saltelli.sample(problem, 10000, calc_second_order=True) #base samples number= 10000

# Model function
def DC_model(X):
    F = X[:, 0]
    mantle_ratio = X[:, 1]
    return ((he4_he3_phncryst * F) - (mantle_ratio * F)) / JHe_1_whc

Y = DC_model(param_values)

# Sobol indices
Si = sobol.analyze(problem, Y, print_to_console=False)




# --------------------------------
# 6. Printing results
# --------------------------------

print("Monte Carlo DC statistics:")
print(f"Mean = {mean_DC:.2f}, Median = {median_DC:.2f}, Std = {std_DC:.2f}, 95% CI = [{ci95[0]:.2f}, {ci95[1]:.2f}] km\n")
print(f"80% CI = [{ci80[0]:.2f}, {ci80[1]:.2f}] km\n")

print("Sobol sensitivity indices (first-order S1):")
for name, s1 in zip(problem['names'], Si['S1']):
    print(f"{name}: {s1:.3f}")

print("\nSobol total-order indices (ST):")
for name, st in zip(problem['names'], Si['ST']):
    print(f"{name}: {st:.3f}")



"""
# --------------------------------------
# 7. Printing: Solib sensitivity indices
# --------------------------------------
# plt.subplot(1, 3, 3)
plt.figure(2)
plt.bar(problem['names'], Si['S1'], color='green', alpha=0.7)
plt.ylabel('First-order Sobol index')
plt.ylim(0, 1)
plt.title('Parameter Sensitivity (S1)')

plt.tight_layout()
plt.show()
"""