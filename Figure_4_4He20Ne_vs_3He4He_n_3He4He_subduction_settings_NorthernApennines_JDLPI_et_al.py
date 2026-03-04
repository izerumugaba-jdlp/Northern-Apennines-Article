# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 16:12:05 2026

@author: ijdpe
"""

# ======================================================================
# 3.4 Figure 4 — Northern Apennines
# Left: 4He/20Ne vs 3He/4He mixing
# Right: 3He/4He in subduction settings
# ======================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# DATA IMPORT
# ----------------------------------------------------------------------

dfnobles = pd.read_excel(r"GasData_NorthernApennines.xlsx", sheet_name="Majors_Nobles_Plots", index_col="annot")

dfendmembers = pd.read_excel(r"Endmembers.xlsx")

centralItalyHe = pd.read_excel(r"gas_data_compilation_central_Italy_Minissale_2004_all.xlsx")

andesCHe_CVZ = pd.read_excel(r"AndesC_He_Barry_et_al_2022.xlsx", sheet_name="CVZ")

pacificHe = pd.read_excel(r"He_signature_in_subduction_zones_pacific.xlsx", sheet_name="datatreat")

sundabandaHe = pd.read_excel(r"He_data_SundanBanda_Indo_Hilton_et_al_1991.xlsx", sheet_name="He_data")

southItalyHe = pd.read_excel(r"gas_data_southern_Italy_Sano_et_al_1989.xlsx")

phenocrystsHeVA = pd.read_excel(r"Phenocrysts_He_Sr_RCP.xlsx")

phenocrystsHeVFRI= pd.read_excel(r"PhenocrystsHe_Sr_rest_It.xlsx")


# ----------------------------------------------------------------------
# CONSTANTS & FUNCTIONS (UNCHANGED)
# ----------------------------------------------------------------------
# Fixed end-member values
Ra= 1.4e-06
Conversion_factor_4He_cm3_g= 1.79e-04    #1 cm3 of 4He at STP= 1.79e-04 g of 4He

# Air
He_air = 5.24e-06    #mol/mol
He3_He4_air = 1 * Ra
He4_Ne20_air = 0.318

# Crust
He_crust_ccg= 5e-05                                          #cm3/g (Martelli et al., 2004)
He_crust= He_crust_ccg * Conversion_factor_4He_cm3_g      #8.95e-09
print(f"He_crust_gg= {He_crust:.2e}")  

He3_He4_crust= 0.02 *Ra
He4_Ne20_crust = 1000

# Mantle (MORB)
He_morb_ccg= 1.5e-05                                         #cm3/g (Martelli et al., 2004)
He_morb= He_morb_ccg * Conversion_factor_4He_cm3_g        #2.68e-09
print(f"He_morb_gg= {He_morb:.2e}")  

He3_He4_morb= 6.7 * Ra
He4_Ne20_morb = 1000

#-------------------------------------------------------------------------------------------------------------------------------------------------

# Function for getting isotope concentrations_ He3 and He4; from their ratio and sum(total He)
def get_concs_he3_he4(total, ratio):
    He4 = total / (1 + ratio)
    He3 = ratio * He4
    return He3, He4

# Function for getting Ne20 concentration;
def get_conc_Ne20 (He4_Ne20, He4):
    Ne20= He4 / He4_Ne20
    return Ne20

# Mixing fractions, f is the fraction of air in the mix
f = np.linspace(0, 1, 1000000)

# Getting the concentrations of isotopes in endmembers
He3_air, He4_air = get_concs_he3_he4(He_air, He3_He4_air)
He3_crust, He4_crust = get_concs_he3_he4(He_crust, He3_He4_crust)
He3_morb, He4_morb = get_concs_he3_he4(He_morb, He3_He4_morb)

Ne20_air= get_conc_Ne20 (He4_Ne20_air, He4_air)
Ne20_crust= get_conc_Ne20 (He4_Ne20_crust, He4_crust)
Ne20_morb= get_conc_Ne20 (He4_Ne20_morb, He4_morb)

#--------------------------------------------------------------------------------------------------------------------------------------------

# MIXING BTN AIR AND CRUST
# Performing mixing air-crust (ac) i.e calculating isotopes concentration at each step of the mixture
He3_mix_ac = (f * He3_air) + ((1 - f) * He3_crust)
He4_mix_ac = (f * He4_air) + ((1 - f) * He4_crust)
Ne20_mix_ac = (f * Ne20_air) + ((1 - f) * Ne20_crust)

# Computing ratios at each step of of the mixture
He3_He4_mix_ac = (He3_mix_ac / He4_mix_ac) / Ra
He4_Ne20_mix_ac = (He4_mix_ac / Ne20_mix_ac)

# MIXING BTN AIR AND MORB
# Performing mixing air-morb (am) i.e calculating isotopes concentration at each step of the mixture
He3_mix_am = (f * He3_air) + ((1 - f) * He3_morb)
He4_mix_am = (f * He4_air) + ((1 - f) * He4_morb)
Ne20_mix_am = (f * Ne20_air) + ((1 - f) * Ne20_morb)

# Computing ratios at each step of of the mixture
He3_He4_mix_am = (He3_mix_am / He4_mix_am) / Ra
He4_Ne20_mix_am = (He4_mix_am / Ne20_mix_am)

# ----------------------------------------------------------------------
# FIGURE SETUP

plt.rcParams["font.family"] = "Calibri"

fig = plt.figure(figsize=(15, 5))

# ======================================================================
# SUBPLOT (A): 4He/20Ne vs 3He/4He
# ======================================================================

ax1 = plt.subplot(1, 2, 1)

# Error bars
lowest_err_value = dfnobles["R/Ra"] - 1.1 * 0.01
lower_err = np.where(dfnobles["err_R/Ra"] > dfnobles["R/Ra"],
                     lowest_err_value,
                     dfnobles["err_R/Ra"])
upper_err = dfnobles["err_R/Ra"]

ax1.errorbar(dfnobles["4He/20Ne"], dfnobles["R/Ra"], yerr=[lower_err, upper_err], fmt="o", color="blue", capsize=4)

# Endmembers (dropping unwanted rows)
dfendmembers_f = dfendmembers.drop([2, 3])
ax1.scatter(dfendmembers_f["4He/20Ne"], dfendmembers_f["R/Ra"], marker="*", s=200, color="red")

# Plotting mixing curves
plt.plot(He4_Ne20_mix_ac, He3_He4_mix_ac, "k")
plt.plot(He4_Ne20_mix_am, He3_He4_mix_am, "k")

#-------------------------------------------------------------------------------------------------------------------------------------------

# MIXING BTN AIR, and different fractional mixing between CRUST AND MORB
# We go from different mixing ratios, considering the mantle fraction f_m_cm.
# This will result in different values of 3He/4He (Ra), but the 4He/20Ne remains elevated i.e >1000.
f_m_cm= [i/100 for i in [7, 15, 30]]                   # fraction of mantle in mantle-crust mixture
He3_He4_cm= [(j * He3_He4_morb) + ((1 - j) * He3_He4_crust) for j in f_m_cm]
He3_He4_cm_Ra= [k / Ra for k in He3_He4_cm]
print()
print(f"Mantle fr= {f_m_cm}")
print(f"He_He4_CM= {He3_He4_cm_Ra} Ra")

He_cm= [(i * He_morb) + ((1 - i) * He_crust) for i in f_m_cm]
He4_Ne20_cm= [(i * He4_Ne20_morb) + ((1 - i) * He4_Ne20_crust) for i in f_m_cm]


for He3_He4_cm_1, He_cm_1, He4_Ne20_cm1 in zip(He3_He4_cm, He_cm, He4_Ne20_cm):
    
    # Getting the concentrations of isotopes in endmembers
    He3_cm, He4_cm = get_concs_he3_he4(He_cm_1, He3_He4_cm_1)
    Ne20_cm= get_conc_Ne20 (He4_Ne20_cm1, He4_cm)


    # Performing mixing air-cm (am) i.e calculating isotopes concentration at each step of the mixture
    He3_mix_a_cm = (f * He3_air) + ((1 - f) * He3_cm)
    He4_mix_a_cm = (f * He4_air) + ((1 - f) * He4_cm)
    Ne20_mix_a_cm = (f * Ne20_air) + ((1 - f) * Ne20_cm)

    # Computing ratios at each step of of the mixture
    He3_He4_mix_a_cm = (He3_mix_a_cm / He4_mix_a_cm) / Ra
    He4_Ne20_mix_a_cm = (He4_mix_a_cm / Ne20_mix_a_cm)
    
    # Plotting mixing curves
    plt.plot(He4_Ne20_mix_a_cm, He3_He4_mix_a_cm, "k--")

# Sample annotations
for i in dfnobles.index:
    if i in [6, 3, 9]:
        ax1.annotate(i, (dfnobles.loc[i,"4He/20Ne"], dfnobles.loc[i,"R/Ra"]),
                     xytext=(-7, 2.7), textcoords="offset points")
    elif i in [13, 20]:
        ax1.annotate(i, (dfnobles.loc[i,"4He/20Ne"], dfnobles.loc[i,"R/Ra"]),
                     xytext=(4, -8), textcoords="offset points")
    elif i == 7:
        ax1.annotate(i, (dfnobles.loc[i,"4He/20Ne"], dfnobles.loc[i,"R/Ra"]),
                     xytext=(0, -12), textcoords="offset points")
    elif i == 18:
        ax1.annotate(i, (dfnobles.loc[i,"4He/20Ne"], dfnobles.loc[i,"R/Ra"]),
                     xytext=(-10, -13), textcoords="offset points")
    else:
        ax1.annotate(i, (dfnobles.loc[i,"4He/20Ne"], dfnobles.loc[i,"R/Ra"]),
                     xytext=(4, -2.7), textcoords="offset points")
        
#Annotating RRa values      
#Annotating RRa values        
ax1.annotate("0.02Ra", xy=(7*10**2, 0.027), xytext=(0,0), textcoords='offset points', color= 'black')
ax1.annotate("Crust", xy=(7*10**2, 0.012), xytext=(0,0), textcoords='offset points', color= 'black')
ax1.annotate("0.5Ra ", xy=(7*10**2, 0.55), xytext=(0,0), textcoords='offset points', color= 'black')
ax1.annotate("1Ra (Air)", xy=(7*10**2, 1.15), xytext=(0, 0), textcoords='offset points', color= 'black')
ax1.annotate("Air", xy=(0.25, 0.5), xytext=(-13, 20), textcoords='offset points', color= 'black')
ax1.annotate("2Ra", xy=(7*10**2, 2.25), xytext=(0, 0), textcoords='offset points', color= 'black')
# ax.annotate("5Ra (62%)", xy=(3.5*10**2, 5.4), xytext=(0, 0), textcoords='offset points', color= 'black')
# ax.annotate("6.1Ra (SCLM)", xy=(1.3*10**3, 4.7), xytext=(1.3*10**3, 4.7), color= 'black')
ax1.annotate("6.7Ra (HIMU)", xy=(4*10**2, 8.2), xytext=(0, 0), textcoords='offset points', color= 'black')
# ax.annotate("8Ra", xy=(7.5*10**2, 9.7), xytext=(0,0), textcoords='offset points', color= 'black')
# ax.annotate("(MORB)", xy=(5.8*10**2, 5), xytext=(0,0), textcoords='offset points', color= 'black')

ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlim(0.1, 5000)
ax1.set_ylim(0.01, 15)
ax1.set_xlabel(r"$\mathrm{^4He/^{20}Ne}$", fontsize=13)
ax1.set_ylabel(r"$\mathrm{^3He/^4He}$ (R/Ra)", fontsize=13)


# ======================================================================
# SUBPLOT (B): 3He/4He in subduction settings
# ======================================================================

ax2 = plt.subplot(1, 2, 2)

# X positions
Xvals = {"EM": 0, "S": 1, "CI": 2, "IP": 3,
         "SB": 4, "A": 5, "ES": 6, "P": 7}

# plotting
ax2.scatter(np.ones(len(dfendmembers["R/Ra"])) * Xvals["EM"],
            dfendmembers["R/Ra"], marker="*", s=70, color="red",
            label="Endmembers (E.M)")

ax2.scatter(np.ones(len(dfnobles["R/Ra"])) * Xvals["S"],
            dfnobles["R/Ra"], s=15, color="blue",
            label="This study (S, n=12)")

ax2.scatter(np.ones(len(centralItalyHe["Rc/Ra"])) * Xvals["CI"],
            centralItalyHe["Rc/Ra"], s=15, color="cornflowerblue",
            label="Central Italy (C.I, n=66)")

ax2.scatter(np.ones(len(phenocrystsHeVA["R/Ra"])) * Xvals["IP"],
            phenocrystsHeVA["R/Ra"], s=15, color="green",
            label="Tuscany–Roman (I.P, n=13)")

ax2.scatter(np.ones(len(phenocrystsHeVFRI["R/Ra"])) * Xvals["IP"],
            phenocrystsHeVFRI["R/Ra"], s=15, color="orange",
            label= "Campania (I.P, n= 16)")


ax2.scatter(np.ones(len(sundabandaHe["R/Ra"])) * Xvals["SB"],
            sundabandaHe["R/Ra"], s=15, color="plum",
            label="Sunda–Banda (S.B, n=15)")

ax2.scatter(np.ones(len(andesCHe_CVZ["R/Ra"])) * Xvals["A"],
            andesCHe_CVZ["R/Ra"], s=15, color="grey",
            label="Andes CVZ (A, n=23)")

ax2.scatter(np.ones(len(southItalyHe["Rc/Ra"])) * Xvals["ES"],
            southItalyHe["Rc/Ra"], s=15, color="maroon",
            label="Eolian–Sicily (E.S, n=18)")

ax2.scatter(np.ones(len(pacificHe["R/Ra"])) * Xvals["P"],
            pacificHe["R/Ra"], s=15, color="black",
            label="Pacific (P, n=19)")

# Endmember labels
for i in dfendmembers.index:
    if i not in [6, 9]:
        ax2.annotate(dfendmembers.loc[i,"Label"],
                     (Xvals["EM"], dfendmembers.loc[i,"R/Ra"]),
                     xytext=(-28, -2.7), textcoords="offset points", fontsize=9)

ax2.set_xlim(-1, 8)
ax2.set_ylim(-1, 13.5)
ax2.set_xticks(list(Xvals.values()))
ax2.set_xticklabels(["E.M","S","C.I","I.P","S.B","A","E.S","P"])
ax2.set_xlabel("Subduction setting", fontsize=13)
ax2.set_ylabel(r"$\mathrm{^3He/^4He}$ (R/Ra)", fontsize=13)

ax2.legend(loc="upper left", ncol=2, fontsize=10)

# ----------------------------------------------------------------------
# SAVING FIGURE
# ----------------------------------------------------------------------

plt.savefig("Figure_4_4He20Nevs3He4He_n_3He4He_subduction_settings_NorthernApennines_JDLPI_et_al.svg",
            format="svg", bbox_inches="tight")

plt.savefig("Figure_4_4He20Nevs3He4He_n_3He4He_subduction_settings_NorthernApennines_JDLPI_et_al.tiff",
            format="tiff", bbox_inches="tight")

plt.show()
