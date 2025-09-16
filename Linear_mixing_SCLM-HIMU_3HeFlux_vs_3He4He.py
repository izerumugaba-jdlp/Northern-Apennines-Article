# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 16:09:15 2024

@author: jdlpizerumug
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from sympy import symbols, Eq, solve

# F_3He_LAmix= np.arange(0, 5.5, 0.5)
# He3He4_LAmix= np.arange(0, 10, 1)

df_He_SCLMdt= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\df_He_SCLM.xlsx", index_col=("Age (Myr)"))

#Endmember values
SCLM_age= 300                                                           # Enter the SCLM age in Ma 
RRa_SCLM_sb_300= round ((df_He_SCLMdt.loc[SCLM_age, "RRa_SCLM_sb"]), 2) # Picking the SCLM signature given the age
# RRa_SCLM_sb_300= round (2.354452054794521, 2)                         # RRa for a 300Ma SCLM; see main file to check values of other ages                    
F3He_SCLM= 1
F3He_MORB= 3.5
F3He_HIMU= 3.5
RRa_MORB= 8
RRa_HIMU= 6.7


EMsignt= {"F_3He_LA": [F3He_SCLM, F3He_MORB], "He3He4_LA": [RRa_SCLM_sb_300, RRa_HIMU]}
df_EMsignt= pd.DataFrame(data= EMsignt, index= ("SCLM_LA", "HIMU_LA") )

f_HIMU_LA= np.arange(0.1, 1, 0.1)                 #Fraction of HIMU
f_SCLM_LA= [round (j, 2) for j in [1 - i for i in f_HIMU_LA]] 
print ("f_HIMU_LA:", f_HIMU_LA)
print ("f_SCLM_LA:", f_SCLM_LA)

F_3He_LAmix= []
He3He4_LAmix= []

for i in f_HIMU_LA:
    F_3He_LAmix_i= (i * df_EMsignt.loc["HIMU_LA", "F_3He_LA"]) + ((1-i) * df_EMsignt.loc["SCLM_LA", "F_3He_LA"])
    F_3He_LAmix.append(F_3He_LAmix_i)
    He3He4_LAmix_i= (i * df_EMsignt.loc["HIMU_LA", "He3He4_LA"]) + ((1-i) * df_EMsignt.loc["SCLM_LA", "He3He4_LA"])
    He3He4_LAmix.append(He3He4_LAmix_i)
        
print()
print("F_3He_LAmix:", [round (j, 2) for j in F_3He_LAmix])
print("He3He4_LAmix:", [round (j, 2) for j in He3He4_LAmix])

#PLOTTING
fig, ax= plt.subplots()

#Endmember values
handle_HIMU_em1= ax.scatter(df_EMsignt.loc["HIMU_LA", "F_3He_LA"], df_EMsignt.loc["HIMU_LA", "He3He4_LA"], marker= "*", s= 100, color= "red")
handle_sclm_em1= ax.scatter(df_EMsignt.loc["SCLM_LA", "F_3He_LA"], df_EMsignt.loc["SCLM_LA", "He3He4_LA"], marker= "*", s= 100, color= "black")

#Mixing line  
plt.plot(np.array(df_EMsignt.loc[:, "F_3He_LA"]), np.array(df_EMsignt.loc[:, "He3He4_LA"]), "k--")

# Mix ratio Compositions
handle_mix_1= plt.scatter(F_3He_LAmix, He3He4_LAmix, marker= "o", color= "magenta")
for i in range(len(F_3He_LAmix)):
    plt.annotate((round(F_3He_LAmix[i], 2), round(He3He4_LAmix[i], 2)), (F_3He_LAmix[i], He3He4_LAmix[i]), 
                 fontsize= 7.85, xytext=(5, -2.7), textcoords='offset points', fontweight= "bold")

plt.annotate((round(df_EMsignt.loc["HIMU_LA", "F_3He_LA"], 2), round(df_EMsignt.loc["HIMU_LA", "He3He4_LA"], 2)), (df_EMsignt.loc["HIMU_LA", "F_3He_LA"], df_EMsignt.loc["HIMU_LA", "He3He4_LA"]), fontsize= 7.85, xytext=(5, -2.7), textcoords='offset points', fontweight= "bold")
plt.annotate((round(df_EMsignt.loc["SCLM_LA", "F_3He_LA"], 2), round(df_EMsignt.loc["SCLM_LA", "He3He4_LA"], 2)), (df_EMsignt.loc["SCLM_LA", "F_3He_LA"], df_EMsignt.loc["SCLM_LA", "He3He4_LA"]), fontsize= 7.85, xytext=(5, -2.7), textcoords='offset points', fontweight= "bold")
plt.xlabel("$\mathrm{^3He \ Flux \ (atoms \ cm^{-2}\ s^{-1})}$", fontsize= 13)
plt.ylabel("$\mathrm{^{3}He/^{4}He}$ (R/Ra)", fontsize= 13)

plt.xlim(0, 4.5, 0.5)
plt.ylim(0, 8.5, 1)

plt.legend([handle_HIMU_em1, handle_sclm_em1, handle_mix_1],
           ["Starting HIMU signature", "Starting SCLM signature", "Starting mixture signatures"])

plt.savefig('Lineral_mixing_SCLM-HIMU_3HeFlux_vs_3He4He.svg', format='svg', bbox_inches= "tight")

plt.show()