# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 13:58:10 2024

@author: jdlpizerumug
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

dfnobles= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\dfnobles_output.xlsx")
dfnobles.set_index(["annot"], inplace=True)
dfendmembers= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\endmembers.xlsx")

x_M= [10**9, 10**9, 10**10, 10**10, 10**9]
y_M= [0.01, 1.2, 1.2, 0.01, 0.01]

# Plotting
# Main figure
fig, ax = plt.subplots()
# plt.fill(x_M, y_M, hatch= ".", color= "none", edgecolor= "black")
plt.fill(x_M, y_M, color= "orange", alpha= 0.5, label ="Magmatic CO2")    # hatch= "."
plt.plot(x_M, y_M, "k", alpha= 0.5)

ax.scatter(dfnobles.loc[:,"CO2/3He"],[i/100 for i in dfnobles.loc[:,"CO2"]], marker= "o", s=35, color= "blue", label="This study")
# dfendmembers_f= dfendmembers.drop([2, 3])           #dropping indices whose data i dont wanna show on the plot
# plt.plot(dfendmembers.loc[:,"CO2/3He"], dfendmembers.loc[:,"CO2"], "r*", ms=13, label= "Endmembers")

for i in dfnobles.index:
    if i in [3, 5, 7, 20]:
        ax.annotate(i, xy=(dfnobles.loc[i,"CO2/3He"], (dfnobles.loc[i,"CO2"]/100)), 
                    xytext= (1, 0), textcoords= "offset points", fontsize= 11)
    
ax.annotate("Magmatic CO2", xy=(2.3*10**9, 0.3), fontweight='normal', fontsize= 13, rotation= 90) 
ax.annotate("Crustal CO2", xy=(5*10**12, 0.3), fontweight='normal', fontsize= 13, rotation= 90)  
 
    
plt.xlim(10**7, 10**13)
plt.ylim(0.01, 1.1)
plt.xscale("log")
# plt.yscale("log")

# Creating CO2-rich rectangle, setting transform=ax.transData
rect = patches.Rectangle((7*10**10, 0.9), width= 7*10**12, height=0.15, linestyle= "--", linewidth=1, edgecolor='black', facecolor='none')
ax.add_patch(rect)
ax.annotate("CO2-rich", xy=(2*10**11, 0.85), fontweight='normal', fontsize= 11, rotation= 0)


# arrow1_ decrease of CO2
arrow1= patches.FancyArrowPatch((3*10**12, 0.85), (2*10**10, 0.05), 
                        connectionstyle="arc3,rad=-0.2",  # Controls the curvature
                        arrowstyle="simple",  mutation_scale=8, color="black", lw= 0, alpha= 1)
ax.add_patch(arrow1)
ax.annotate("Dilution/ Loss of CO2", xy=(0.8*10**11, 0.05), fontweight='normal', fontsize= 11, rotation= 50)

# arrow2_ increase of 3He
arrow2= patches.FancyArrowPatch((8*10**11, 0.62), (2*10**10, 0.62), 
                        connectionstyle="arc3,rad=0",  # Controls the curvature
                        arrowstyle="simple",  mutation_scale=8, color="black", lw= 0, alpha= 1)
ax.add_patch(arrow2)
ax.annotate("Increase of 3He", xy=(1.8*10**10, 0.56), fontweight='normal', fontsize= 11, rotation= 0)


plt.xlabel(r"$\mathrm{CO_2/^3He}$", fontweight='normal', fontsize= 13)
plt.ylabel(r"$\mathrm{CO_2}$ fraction", fontweight='normal', fontsize= 13)
# plt.legend(loc= "upper left")
plt.savefig('CO2-3He_vs_CO2_Apennines.svg', format='svg', bbox_inches='tight')


"""
# Zoom in figure
fig1, ax = plt.subplots()
ax.scatter(dfnobles.loc[:,"CO2/3He"],[i/100 for i in dfnobles.loc[:,"CO2"]], marker= "o", s=35, color= "blue", label="This study")
for i in dfnobles.index:
    if i in [3, 5, 7, 20]:
        ax.annotate(i, xy=(dfnobles.loc[i,"CO2/3He"], (dfnobles.loc[i,"CO2"]/100)), xytext= (2,0), textcoords= "offset points",)
        
plt.xlim(6*10**9, 10**13)
plt.ylim(0, 1.1)
plt.xscale("log")
plt.xlabel("CO"+"\u2082"+"/"+"\u00B3"+"He", fontweight='bold', fontsize= 13) 
plt.ylabel("CO"+"\u2082"+" v/v", fontweight='bold', fontsize= 13)
plt.savefig('CO2-3He vs CO2_ zoomed.svg', format='svg', bbox_inches='tight')
"""






