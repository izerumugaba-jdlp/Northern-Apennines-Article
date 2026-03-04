# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 03:35:19 2026

@author: ijdpe
"""

import pandas as pd
import numpy as np
import math
from scipy.stats import t
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# -------------------------
# IMPORTING THE DATA
# -------------------------
dfnobles = pd.read_excel(r"GasData_NorthernApennines.xlsx", sheet_name="Majors_Nobles_Plots", index_col="annot")

finaldata = pd.read_excel(r"gasdata_budgets_final.xlsx", index_col="ID")

mask = dfnobles.index != 3

# -------------------------
# PLOTTING
# -------------------------
fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(15, 5))

# =========================================================
# AX1: 3He vs 3He/4He
# =========================================================
x_data = dfnobles.loc[mask, "3He"]
y_data = dfnobles.loc[mask, "R/Ra"]

coefficients_ax1 = np.polyfit(x_data, y_data, 1)
poly_ax1 = np.poly1d(coefficients_ax1)

x_fit = np.linspace(min(x_data), max(x_data), 1000)
y_fit = poly_ax1(x_fit)

data_ax1 = ax1.scatter(x_data, y_data, color="blue",
                       label="$\mathrm{^{3}He}$ vs $\mathrm{^{3}He}/\mathrm{^{4}He}$")
fitline_ax1, = ax1.plot(x_fit, y_fit, color="red",
                        label="Best fit ($\mathrm{^{3}He}$ vs $\mathrm{^{3}He}/\mathrm{^{4}He})$")

ax1.set_xlabel("$\\mathrm{^3He}$ (ppm)", fontsize=13)
ax1.set_ylabel("$\\mathrm{^{3}He/^{4}He}$ (R/Ra)", fontsize=13)
ax1.set_ylim(-0.1, 8)

# --- annotations ---
for i in dfnobles.index:
    if i == 18 or i == 8:
        ax1.annotate(i,
                     xy=(dfnobles.loc[i, "3He"], dfnobles.loc[i, "R/Ra"]),
                     xytext=(9, 5), ha="center", va="top",
                     textcoords="offset points", color="blue")
    elif i == 3:
        continue
    else:
        ax1.annotate(i,
                     xy=(dfnobles.loc[i, "3He"], dfnobles.loc[i, "R/Ra"]),
                     xytext=(-7.5, 5), ha="center", va="top",
                     textcoords="offset points", color="blue")

# R squared
X1 = x_data.to_numpy().reshape(-1, 1)
model1 = LinearRegression().fit(X1, y_data)
r_squared = model1.score(X1, y_data)

ax1.annotate(
    fr"$\mathrm{{R}}^2 = {r_squared:.2f}$",
    xy=(1.1e-11, 0.7),
    xytext=(1.1e-11, 0.7),
    color="red")


# =========================================================
# AX2 : Mantle fraction (twin y-axis)
# =========================================================
z_data = finaldata.loc[mask, "HIMU_He"]
ax2 = ax1.twinx()

coefficients_ax2 = np.polyfit(x_data, z_data, 1)
poly_ax2 = np.poly1d(coefficients_ax2)

z_fit = poly_ax2(x_fit)

data_ax2 = ax2.scatter(x_data, z_data, color="green",
                       label= "$\mathrm{^3He}$ vs mantle fraction (%)")
fitline_ax2, = ax2.plot(x_fit, z_fit, color="fuchsia",
                        label="Best fit ($\mathrm{^3He}$ vs mantle fraction)")

ax2.set_ylabel("Mantle fraction (%)", fontsize=13)
ax2.set_ylim(-0.1, 50)

df_3He_mf = pd.DataFrame({
    "3He": dfnobles["3He"],
    "HIMUfract_He": finaldata["HIMU_He"]})

# --- annotations ---
for i in df_3He_mf.index:
    if i in [7, 8, 14, 19, 20]:
        ax2.annotate(i,
                     (df_3He_mf.loc[i, "3He"], df_3He_mf.loc[i, "HIMUfract_He"]),
                     textcoords="offset points", xytext=(0, -11), ha="center", color="green")
    else:
        ax2.annotate(i,
                     (df_3He_mf.loc[i, "3He"], df_3He_mf.loc[i, "HIMUfract_He"]),
                     textcoords="offset points", xytext=(0, 5), ha="center", color="green")

# R squared ax2
X2 = x_data.to_numpy().reshape(-1, 1)
model2 = LinearRegression().fit(X2, z_data)
r_squared_ax2 = model2.score(X2, z_data)

ax2.annotate(fr"$\mathrm{{R}}^2$= {round(r_squared_ax2, 2)}",
             xy=(1.1e-11, 14), xytext=(1.1e-11, 14), color="fuchsia")

# =========================================================
# AX3 : 4He vs 3He/4He
# =========================================================
x4 = dfnobles.loc[mask, "4He"]
y4 = dfnobles.loc[mask, "R/Ra"]

coefficients = np.polyfit(x4, y4, 1)
poly = np.poly1d(coefficients)

x_fit4 = np.linspace(min(x4), max(x4), 1000)
y_fit4 = poly(x_fit4)

ax3.scatter(x4, y4, color="blue", label="4He vs 3He/4He")
ax3.plot(x_fit4, y_fit4, color="red", label="Line of Best Fit")

ax3.set_xlabel("$\\mathrm{^{4}He}$ (ppm)", fontsize=13)
ax3.set_ylabel("$\\mathrm{^{3}He/^{4}He}$ (R/Ra)", fontsize=13)
ax3.set_xlim(0, 1.4e-5)
ax3.set_ylim(-0.1, 8)

# --- annotations ---
for i in dfnobles.index:
    if i == 19 or i == 18:
        ax3.annotate(i,
                     xy=(dfnobles.loc[i, "4He"],
                         dfnobles.loc[i, "R/Ra"]),
                     xytext=(10, 5),
                     ha="center",
                     va="top",
                     textcoords="offset points")
    elif i == 3:
        continue
    else:
        ax3.annotate(i,
                     xy=(dfnobles.loc[i, "4He"],
                         dfnobles.loc[i, "R/Ra"]),
                     xytext=(-7.5, 5),
                     ha="center",
                     va="top",
                     textcoords="offset points")
        
ax3.annotate(fr"$\mathrm{{R}}^2$= 0.05",
             xy=(1.1e-5, 0.7), xytext=(1.1e-5, 0.7), color="red")

# =========================================================
# LEGEND & SAVING
# =========================================================
handles = [data_ax1, fitline_ax1, data_ax2, fitline_ax2]
labels = [h.get_label() for h in handles]

fig.legend(handles, labels,
           loc="center right",
           bbox_to_anchor=(0.4750, 0.78))

plt.savefig("Figure_9_3Hevs3He4HevsMantleFraction-&-4Hevs3He4He_Apennines.svg", format="svg", bbox_inches="tight")
plt.savefig("Figure_9_3Hevs3He4HevsMantleFraction-&-4Hevs3He4He_Apennines.tiff", format="tiff", bbox_inches="tight")

plt.show()
