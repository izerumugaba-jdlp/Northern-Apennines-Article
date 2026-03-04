# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 03:58:36 2026

@author: ijdpe
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# -------------------------
# IMPORTING THE DATA
# -------------------------
dfnobles = pd.read_excel(r"GasData_NorthernApennines.xlsx", sheet_name="Majors_Nobles_Plots", index_col="annot")

dfendmembers = pd.read_excel(r"Endmembers.xlsx", index_col="Label")

andesCHe = pd.read_excel(r"AndesC_He_Barry_et_al_2022.xlsx")

dfcrustRRaCO23He = pd.DataFrame({"crustRRa": [0.02]*6,
                                 "crustCO23He": [10**11, 10**12, 10**13, 10**14, 10**15, 10**16]},
                                index=[11,12,13,14,15,16])

# -------------------------
# MIXING CURVES
# -------------------------
aMc, bMc = 1.4e-6, 1.344e-11
aC, bC   = 1.4e-6, 3e-14
xMc, yMc, yC = 3e9, 6.7, 0.02

B = aMc*bC - aC*bMc
A = aC*bMc*yC - aMc*bC*yMc

def mixing_curve(xC, step):
    X = np.arange(xMc, xC, step)
    C = aC*bMc*xMc - aMc*bC*xC
    D = aMc*bC*xC*yMc - aC*bMc*xMc*yC
    Y = (-D - A*X)/((B*X)+C)
    return X, Y

X12, Y12 = mixing_curve(dfcrustRRaCO23He.loc[12,"crustCO23He"], 1e9)
X13, Y13 = mixing_curve(dfcrustRRaCO23He.loc[13,"crustCO23He"], 1e9)
X14, Y14 = mixing_curve(dfcrustRRaCO23He.loc[14,"crustCO23He"], 1e10)

# -------------------------
# FIGURE SETUP (1x2)
# -------------------------
plt.figure(figsize=(15, 5))

# -------------------------
# LEFT SUBPLOT : R/Ra vs CO2/3He
# -------------------------
ax1 = plt.subplot(1, 2, 1)

ax1.scatter(dfnobles["CO2/3He"], dfnobles["R/Ra"], color="blue", label="This study")
ax1.scatter(dfcrustRRaCO23He["crustCO23He"], dfcrustRRaCO23He["crustRRa"], color="red", label="Crust")
ax1.scatter(andesCHe["CO2/3He"], andesCHe["R/Ra"], s=10, color="grey", label="Andes")

ax1.plot(X12, Y12, "k")
ax1.plot(X13, Y13, "k")
ax1.plot(X14, Y14, "k")

ax1.plot(dfendmembers.loc["HIMU","CO2/3He"], dfendmembers.loc["HIMU","R/Ra"], "r*", ms=13)
ax1.plot(dfendmembers.loc["AIR","CO2/3He"], dfendmembers.loc["AIR","R/Ra"], "ks", ms=8)

ax1.annotate("Air", xy=(dfendmembers.loc["AIR","CO2/3He"], 0.6), ha="center")
ax1.annotate("HIMU", xy=(dfendmembers.loc["HIMU","CO2/3He"], 10), ha="center", color="red")

for i in dfnobles.index:
    ax1.annotate(i, xy=(dfnobles.loc[i,"CO2/3He"], dfnobles.loc[i,"R/Ra"]),
                 xytext=(-6.5, 6.5), textcoords="offset points", ha="center", va="top")

ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlim(1e7, 7e16)
ax1.set_ylim(0.01, 30)
ax1.set_xlabel(r"$\mathrm{CO_2/^3He}$", fontsize=13)
ax1.set_ylabel(r"$\mathrm{^3He/^4He}$ (R/Ra)", fontsize=13)
ax1.legend(loc="upper right")
# ax1.set_title("R/Ra vs CO2/3He")

# -------------------------
# RIGHT SUBPLOT : CO2 fraction vs CO2/3He
# -------------------------
ax2 = plt.subplot(1, 2, 2)

x_M = [10**9, 10**9, 10**10, 10**10, 10**9]
y_M = [0.01, 1.2, 1.2, 0.01, 0.01]

ax2.fill(x_M, y_M, color="orange", alpha=0.5, label="Magmatic $\\mathrm{CO_2}$")
ax2.plot(x_M, y_M, "k", alpha=0.5)

ax2.scatter(dfnobles.loc[:, "CO2/3He"], [i / 100 for i in dfnobles.loc[:, "CO2"]],
            marker="o", s=35, color="blue")

# --- annotations ---
for i in dfnobles.index:
    if i in [3, 5, 7, 20]:
        ax2.annotate(
            i,
            xy=(dfnobles.loc[i, "CO2/3He"], dfnobles.loc[i, "CO2"] / 100),
            xytext=(1, 0), textcoords="offset points", fontsize=11)

# --- text annotations ---
ax2.annotate(
    "Magmatic $\\mathrm{CO_2}$",
    xy=(2.3 * 10**9, 0.3),
    fontweight="normal", fontsize=13, rotation=90)

ax2.annotate(
    "Crustal $\\mathrm{CO_2}$",
    xy=(5 * 10**12, 0.3),
    fontweight="normal", fontsize=13, rotation=90)

# --- CO2-rich rectangle ---
rect = patches.Rectangle((7 * 10**10, 0.9), width=7 * 10**12, height=0.15,
                         linestyle="--", linewidth=1, edgecolor="black", facecolor="none")
ax2.add_patch(rect)

ax2.annotate(
    "$\\mathrm{CO_2}$-rich",
    xy=(2 * 10**11, 0.85),
    fontweight="normal", fontsize=11)

# --- curved arrow: dilution / loss of CO2 ---
arrow1 = patches.FancyArrowPatch(
    (3 * 10**12, 0.85),
    (2 * 10**10, 0.05),
    connectionstyle="arc3,rad=-0.2", arrowstyle="simple",
    mutation_scale=8, color="black", lw=0, alpha=1)
ax2.add_patch(arrow1)

ax2.annotate(
    "Dilution/ Loss of $\\mathrm{CO_2}$",
    xy=(0.8 * 10**11, 0.05),
    fontweight="normal", fontsize=11, rotation=50)

# --- arrow: increase of 3He ---
arrow2 = patches.FancyArrowPatch(
    (8 * 10**11, 0.62),
    (2 * 10**10, 0.62),
    connectionstyle="arc3,rad=0", arrowstyle="simple",
    mutation_scale=8, color="black", lw=0, alpha=1)
ax2.add_patch(arrow2)

ax2.annotate(
    "Increase of $\\mathrm{^3He}$",
    xy=(1.8 * 10**10, 0.56),
    fontweight="normal", fontsize=11)

ax2.set_xscale("log")
ax2.set_xlim(10**7, 10**13)
ax2.set_ylim(0.01, 1.1)

ax2.set_xlabel(r"$\mathrm{CO_2/^3He}$", fontsize=13)
ax2.set_ylabel(r"$\mathrm{CO_2}$ fraction", fontsize=13)
# ax2.set_title("CO2 fraction vs CO2/3He")

plt.tight_layout()

# Saving the figure
plt.savefig("Figure_5_CO2_3He_vs_3He4He_n_CO2_3He_vs_CO2Fraction_NorthernApennines_JDLPI_et_al.svg",
            format="svg", bbox_inches="tight")
plt.savefig("Figure_5_CO2_3He_vs_3He4He_n_CO2_3He_vs_CO2Fraction_NorthernApennines_JDLPI_et_al.tiff",
            format="tiff", bbox_inches="tight")
plt.show()

