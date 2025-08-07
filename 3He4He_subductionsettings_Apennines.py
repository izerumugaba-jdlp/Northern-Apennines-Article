# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 22:15:55 2023

@author: jdlpizerumug
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dfnobles= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\dfnobles_output.xlsx")   
dffileendmembers= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\fileendmembers.xlsx")  
dfcommonplots= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\commonplots.xlsx")
dfendmembers= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\endmembers.xlsx", sheet_name= 'og_file')
andesCHe= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\AndesC-He_ Barryetal2022.xlsx")
andesCHe_CVZ= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\AndesC-He_ Barryetal2022.xlsx", sheet_name= 'CVZ')
pacificHe= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\He signature in subduction zones_pacific.xlsx", sheet_name= 'datatreat')
sundabandaHe= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\He data_ SundanBanda_Indo_ Hilton et al 1991.xlsx", sheet_name= 'He_data')
centralItalyHe= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\QGIS_PhD\gas data compilation_central Italy_Minissale 2004_all.xlsx")
southItalyHe= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\gas data_ southern Italy_ Sanoetal1989.xlsx")
phenocrystsItHe= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\Phenocrysts_ olivine pyroxene data He Sr_ Martelli et al 2004.xlsx")
phenocrystsHeVA= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\Phenocrysts_He_Sr_RCP.xlsx")
phenocrystsHeVFRI= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\PhenocrystsHe_Sr_ rest It.xlsx")

Xendmembers= np.ones([1, len(dfendmembers.loc[:,"R/Ra"])])*0 
Xdfnobles= np.ones([1, len(dfnobles.loc[:,"R/Ra"])])*1
XcentralItalyHe= np.ones([1,len(centralItalyHe.loc[:,"Rc/Ra"])])*2
XphenocrystsHeVA= np.ones([1,len(phenocrystsHeVA.loc[:,"R/Ra"])])*3
XphenocrystsHeVFRI= np.ones([1,len(phenocrystsHeVFRI.loc[:,"R/Ra"])])*3
XsundabandaHe= np.ones([1,len(sundabandaHe.loc[:,"R/Ra"])])*4
# XandesCHe= np.ones([1,len(andesCHe.loc[:,"R/Ra"])])*5
XandesCHe_CVZ= np.ones([1,len(andesCHe_CVZ.loc[:,"R/Ra"])])*5
XsouthItalyHe= np.ones([1,len(southItalyHe.loc[:,"Rc/Ra"])])*6
XpacificHe= np.ones([1,len(pacificHe.loc[:,"R/Ra"])])*7




# XphenocrystsItHe= np.ones([1,len(phenocrystsItHe.loc[:,"R/Ra"])])*
Xvalues= [Xendmembers[0,0], Xdfnobles[0,0], XcentralItalyHe[0,0], XphenocrystsHeVA[0,0], XsundabandaHe[0,0], XandesCHe_CVZ[0,0], XsouthItalyHe[0,0], XpacificHe[0,0]]
# Xvalues= [Xendmembers, Xdfnobles, XandesCHe, XpacificHe, XphenocrystsHeVA, XphenocrystsHeVFRI]


plt.rcParams['font.family'] = 'Calibri'
fig, ax = plt.subplots()
ax.scatter(Xendmembers, dfendmembers.loc[:,"R/Ra"], marker="*", s=70, color= "red", label= "Endmembers (E.M)")
ax.scatter(Xdfnobles, dfnobles.loc[:,"R/Ra"], marker= "o", s= 15, color= "blue", label= "This study (S, n= 12)")
ax.scatter(XcentralItalyHe, centralItalyHe.loc[:,"Rc/Ra"], marker= "o", s= 15, color= "cornflowerblue", label= "Central Italy (C.I, n= 66)")
ax.scatter(XphenocrystsHeVA, phenocrystsHeVA.loc[:,"R/Ra"], marker= "o", s= 15, color= "green", label= "Tuscany-Roman (I.P, n= 13)")
ax.scatter(XphenocrystsHeVFRI, phenocrystsHeVFRI.loc[:,"R/Ra"], marker= "o", s= 15, color= "orange", label= "Campania (I.P, n= 16)")
ax.scatter(XsundabandaHe, sundabandaHe.loc[:,"R/Ra"], marker= "o", s= 15, color= "plum", label= "Sunda-Banda (S.B, n= 15)")
ax.scatter(XandesCHe_CVZ, andesCHe_CVZ.loc[:,"R/Ra"], marker= "o", s= 15, color= "grey", label= "Andes_CVZ (A, n= 23)")
ax.scatter(XsouthItalyHe, southItalyHe.loc[:,"Rc/Ra"], marker= "o", s= 15, color= "maroon", label= "Eolian-Sicily (E.S, n= 18)")
ax.scatter(XpacificHe, pacificHe.loc[:,"R/Ra"], marker= "o", s= 15, color= "black", label= "Pacific (P, n= 19)")
# ax.scatter(XphenocrystsItHe, phenocrystsItHe.loc[:,"R/Ra"], marker= "o", s= 15, color= "orange")

for i in dfendmembers.index:
    if i!= 6 and i!=9:
        plt.annotate((dfendmembers.loc[i, "Label"]), (Xendmembers[0,0], dfendmembers.loc[i,"R/Ra"]), 
                    fontsize= 9, xytext=(-28, -2.7), textcoords='offset points')
    
plt.ylim(-1, 13.5)
plt.xlim(-1, 8)
# plt.yscale("log") 
# plt.title("R/Ra values in different subduction settings", fontweight='bold')
Xnames= ["E.M", "S", "C.I", "I.P", "S.B", "A", "E.S", "P"]
plt.xticks(Xvalues, Xnames)
plt.xlabel("Subduction setting", fontweight='bold', fontsize= 13) 
plt.ylabel("$\mathbf{^3He/^4He}$ (R/Ra)", fontweight='bold', fontsize= 13)
plt.legend(loc="upper left", ncol= 2, columnspacing=0.4, fontsize= 10)

plt.savefig("3He4He_subductionsettings_Apennines.svg", format="svg", bbox_inches="tight")
plt.show()


