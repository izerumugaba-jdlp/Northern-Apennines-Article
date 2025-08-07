# -*- coding: utf-8 -*-
"""
Created on Wed Aug  6 19:57:04 2025

@author: jdlpizerumug
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Importing files
dfnobles= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\dfnobles_output.xlsx", 
                        index_col= "annot")   
dfendmembers= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\endmembers.xlsx", index_col=("Environment"))
andesCHe= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\AndesC-He_ Barryetal2022.xlsx")

# Fixed end-member values (Sano and Marty, 1995; Marty and Jambon, 1987)

VPDB1312= 0.0112372

d13CO2_sediments= -30
d13CO2_limestone= 0
d13CO2_himu= -3.75                  #Marty et al., 1994

d13CO2_limestone2= 2

CO2_He3_sediments= 1e13
CO2_He3_limestone= 1e13
CO2_He3_himu= 3e09

CO2_He3_limestone2= 1e13

# for CO2-dominated gases in subduction zone, consider 90 mol% CO2 i.e 0.9 mol/mol.
CO2_sediments= 0.9
CO2_limestone= 0.9
CO2_himu= 0.9

CO2_limestone2= 0.9

# Calculating 3He from CO2 and CO2/3He: 3He= CO2 / (CO2/3He)
He3_sediments = CO2_sediments / CO2_He3_sediments
He3_limestone = CO2_limestone / CO2_He3_limestone
He3_himu= CO2_himu / CO2_He3_himu

He3_limestone2 = CO2_limestone2 / CO2_He3_limestone2

# Mixing fractions, given f
f = np.linspace(0, 1, 100000)

# Mixing between sediments and himu
CO2_sed_lim= (CO2_sediments * f) + (CO2_limestone * (1-f))
He3_sed_lim= (He3_sediments * f) + (He3_limestone * (1-f))
CO2_He3_sed_lim= CO2_sed_lim / He3_sed_lim

d13CO2_sed_lim= (d13CO2_sediments * f) + (d13CO2_limestone * (1-f)) 

# Mixing between sediments and himu
CO2_sed_himu= (CO2_sediments * f) + (CO2_himu * (1-f))
He3_sed_himu= (He3_sediments * f) + (He3_himu * (1-f))
CO2_He3_sed_himu= CO2_sed_himu / He3_sed_himu

d13CO2_sed_himu= (d13CO2_sediments * f) + (d13CO2_himu * (1-f))

# Mixing between himu and limestone
CO2_himu_limestone= (CO2_himu * f) + (CO2_limestone * (1-f))
He3_himu_limestone= (He3_himu * f) + (He3_limestone * (1-f))
CO2_He3_himu_limestone= CO2_himu_limestone / He3_himu_limestone

d13CO2_himu_limestone= (d13CO2_himu * f) + (d13CO2_limestone * (1-f))

# Mixing between himu and limestone2
CO2_himu_limestone2= (CO2_himu * f) + (CO2_limestone2 * (1-f))
He3_himu_limestone2= (He3_himu * f) + (He3_limestone2 * (1-f))
CO2_He3_himu_limestone2= CO2_himu_limestone2 / He3_himu_limestone2

d13CO2_himu_limestone2= (d13CO2_himu * f) + (d13CO2_limestone2 * (1-f))

# PLOTTING
fig, ax = plt.subplots()

# Data
ax.scatter(dfnobles["d13C_CO2"], ((dfnobles["CO2"]/100)/dfnobles["3He"]), marker= "o", color= "blue", label="This study")    
ax.scatter(andesCHe.loc[:,"d13C_CO2"], andesCHe.loc[:,"CO2/3He"], marker= "o", s= 10, color= "grey", label="Andes")

#Annotating sampling points
for i in dfnobles.index:
    if i==20 or i==3 or i==19 or i==5:
        ax.annotate(i, xy=(dfnobles.loc[i,"d13C_CO2"], dfnobles.loc[i,"CO2/3He"]), 
               xytext=(5, -2.7), ha='center', va='top', textcoords='offset points', fontsize= 8)

# Endmembers
plt.plot(dfendmembers["d13C_CO2"], dfendmembers["CO2/3He"], "r*", ms=13, label= "Endmembers")

# Annotation of endmembers
ax.annotate("S", xy=(-29, 10**13), xytext=(5, -2.7), ha='center', va='top', textcoords='offset points', fontsize= 15, color= "red")
ax.annotate("L", xy=(0.5, 10**13), xytext=(5, -2.7), ha='center', va='top', textcoords='offset points', fontsize= 15, color= "red")
ax.annotate("M", xy=(-9, 3*10**9), xytext=(5, -2.7), ha='center', va='top', textcoords='offset points', fontsize= 15, color= "red")
ax.annotate("H", xy=(-3, 3*10**9),xytext=(5, -2.7), ha='center', va='top', textcoords='offset points', fontsize= 15, color= "red")

#rectangles for zones of uncertainity (coordinates in clockwise order)
#around sed
xrS= [-40, -20, -20, -40, -40]
yrS= [10**14, 10**14, 10**12, 10**12, 10**14]

#around Lim
xrL= [-2, 2, 2, -2, -2]
yrL= [10**14, 10**14, 10**12, 10**12, 10**14]

#around himu
xrMc= [-10, 0, 0, -10, -10]
yrMc= [3*10**9, 3*10**9, 8*10**8, 8*10**8, 3*10**9]

ax.plot(xrS, yrS, color="red")
ax.plot(xrL, yrL, color="red")
ax.plot(xrMc, yrMc, color="red")

# Mixing curves
plt.plot(d13CO2_sed_lim, CO2_He3_sed_lim, "k")
plt.plot(d13CO2_sed_himu, CO2_He3_sed_himu, "k")
plt.plot(d13CO2_himu_limestone, CO2_He3_himu_limestone, "k")
plt.plot(d13CO2_himu_limestone2, CO2_He3_himu_limestone2, "k--")

# Annotating figure number
# plt.annotate("A", xy=(-40.5, 8e14), xytext=(0, 0), ha='center', va='top', textcoords='offset points', fontsize= 20, fontweight= "bold", zorder=6)

# Setting axes and labels
plt.yscale("log")
# plt.xlim(-43,7)
plt.ylim(10**8, 10**15)
plt.xlabel(r"$\mathbf{δ13C(CO_2)}$", fontweight='bold', fontsize= 13) 
plt.ylabel(r"$\mathbf{CO_2/^3He}$", fontweight='bold', fontsize= 13)
plt.legend(loc= "lower left")

plt.savefig('d13CO2_vs_CO23He_Apennines.svg', format='svg', bbox_inches='tight')
plt.show()








































