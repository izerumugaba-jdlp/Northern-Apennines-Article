# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 18:23:40 2024

@author: jdlpizerumug
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df_He_SCLMdt= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\df_He_SCLM.xlsx", index_col=("Age (Myr)"))

Ra= 1.4 * 10**-6
RRa_SCM= 6.1
RRa_MORB= 8
RRa_HIMU= 6.7

# HeR= 4He/3He
HeR_SCM= 1 / (RRa_SCM * Ra)                           # HeR_SCM= 118000   HeR= 4He/3He
HeR_HIMU= 1 / (RRa_HIMU * Ra)                         # HeR_HIMU= 90000

# 4He flux from crustal radiogenic production (atoms 4He S-1 m-2). (see excel table of calculations) 
JHe_20= 1.7*10**10
JHe_1_whc= (1.70 * 10**10) / 20
JHe_1_uc= (1.45 * 10**10) / 13
# DC= np.arange(0,50,0.1)
DC= np.array([round (i, 2) for i in (np.arange(0,50,0.1))])

# 3He flux (F) in continents from the SCLM                      
F_SCLM= 10000             # Av of Day et al. 2015_ 3He flux in continents is <1 at s-1 cm-2 ( Sano, 1986; Ballentine,1997;  p117_ Day et al)
F_SCLM_min= 2500          # 0.25 - 2.2 at s-1 cm-2 (calculated by Day et al. 2015)
F_SCLM_max= 22000        
F_SCLM_GM= 23000          # European SCLM as defined by G & M (2002); 100km, F3He= 180 mol yr-1; open system
F_HIMU= 35000             # 3He flux at ridges is 3-4 at s-1 cm-2(Craig et al., 1975; Bianchi et al., 2010; p117_ Day et al)

#SCLM 3He/4He that vary with age (Day et al 2015; stored in df_He_SCLMdt)
AgeSCLM= 300
# Visualising starting R/Ra for a given age 
print("For an age of", AgeSCLM,", RRa_SCLM_sb= ", df_He_SCLMdt.loc[AgeSCLM,"RRa_SCLM_sb"])
print("For an age of", AgeSCLM,", RRa_SCLM_db= ", df_He_SCLMdt.loc[AgeSCLM,"RRa_SCLM_db"])

RRa_SCLM_sb_xage= df_He_SCLMdt.loc[AgeSCLM,"RRa_SCLM_sb"]
HeR_SCLM_sb_xage= 1 / (RRa_SCLM_sb_xage * Ra)

#FOR A HYPOTHETICAL MANTLE COMPOSITION WITH DIFFERENT FRACTIONS OF SCLM (Day et al, average) AND HIMU
# Say a case with 50 - 50
f_HIMU= 0.5                 #Fraction of HIMU
f_SCLM= 1 - f_HIMU

F_mix= (F_HIMU * f_HIMU) + (F_SCLM * f_SCLM)

RRa_mix= (RRa_HIMU * f_HIMU)  + (RRa_SCLM_sb_xage * f_SCLM)
HeR_mix= 1 / (RRa_mix * Ra)

#Representation of all possible mixing fractions
f_HIMU_all= [round (i, 2) for i in (np.arange(0.1, 1, 0.1))]
f_SCLM_all= [1 - i for i in f_HIMU_all]
F_mix_all= [(F_HIMU * i) + (F_SCLM * (1 - i)) for i in f_HIMU_all]
RRa_mix_all= [(RRa_HIMU * i)  + (RRa_SCLM_sb_xage * (1 - i)) for i in f_HIMU_all]
HeR_mix_all= [1 / (RRa_mix_all_i * Ra) for RRa_mix_all_i in RRa_mix_all]

print("F_mix_all= ", F_mix_all)

# CALCULATING EXPECTED R/RA GIVEN DIFFERENT PARAMETERS 
# For a 3He flux value of a given mantle signature (F_mantle), the expected HeR after delamination is HeR_Phcry= HeR_mantle + ((JHe_1_whc * DC / F_mantle)).
# Values are calculated in details in the hidden loop below (but not quite saved..), but HeR is recalculated immediately in RRa
for i in DC:
    #For HIMU
    HeR_Phcry_HIMU_whc= HeR_HIMU + (JHe_1_whc * i/F_HIMU)
    HeR_Phcry_HIMU_uc= HeR_HIMU + (JHe_1_uc * i/F_HIMU)
    
    #For SCLM as defined by Gautheron and Moreira (2002 i.e steady state, R/Ra= 6.1 everywhere)
    HeR_Phcry_SCM_whc= HeR_SCM + (JHe_1_whc * i/F_SCLM_GM)
    HeR_Phcry_SCM_uc= HeR_SCM + (JHe_1_uc * i/F_SCLM_GM)
    
    #For SCLM whose R/Ra varies with age (Day et al 2015), average SCLM 3He flux of 1
    HeR_Phcry_SCLM_sb_xage_whc= HeR_SCLM_sb_xage + (JHe_1_whc * i/F_SCLM)
    HeR_Phcry_SCLM_sb_xage_uc= HeR_SCLM_sb_xage + (JHe_1_uc * i/F_SCLM)
    
    # For min and max SCLM 3He flux; for SCLM whose R/Ra varies with age (Day et al. 2015)
    HeR_Phcry_SCLM_sb_xage_whc_min3He= HeR_SCLM_sb_xage + (JHe_1_whc * i/F_SCLM_min)
    HeR_Phcry_SCLM_sb_xage_whc_max3He= HeR_SCLM_sb_xage + (JHe_1_whc * i/F_SCLM_max)
    
    #For SCLM - HIMU mix
    HeR_Phcry_mix_whc= HeR_mix + (JHe_1_whc * i/F_mix)
    HeR_Phcry_mix= HeR_mix + (JHe_1_uc * i/F_mix)
    
    #For all SCLM - HIMU mixtures
    
    HeR_Phcry_mix_all_whc= [j + (JHe_1_whc * i/j) for j in HeR_mix_all]
        
#RRa in  with respect to DC. the following are dataframes with RRa data and corresponding DC
RRa_Phcry_HIMU_whc= pd.DataFrame(((1/(HeR_HIMU + (JHe_1_whc * DC/F_HIMU)))/(Ra)), index= DC)
RRa_Phcry_HIMU_uc= pd.DataFrame(((1/(HeR_HIMU + (JHe_1_uc * DC/F_HIMU)))/(Ra)), index= DC)

RRa_Phcry_SCM_whc= pd.DataFrame(((1/(HeR_SCM + (JHe_1_whc * DC/F_SCLM_GM)))/(Ra)), index= DC)
RRa_Phcry_SCM_uc= pd.DataFrame(((1/(HeR_SCM + (JHe_1_uc * DC/F_SCLM_GM)))/(Ra)), index= DC)

RRa_Phcry_SCLM_sb_xage_whc= pd.DataFrame(((1/(HeR_SCLM_sb_xage + (JHe_1_whc * DC/F_SCLM)))/(Ra)), index= DC)
RRa_Phcry_SCLM_sb_xage_uc= pd.DataFrame(((1/(HeR_SCLM_sb_xage + (JHe_1_uc * DC/F_SCLM)))/(Ra)), index= DC)

RRa_Phcry_SCLM_sb_xage_whc_min3He= pd.DataFrame(((1/(HeR_SCLM_sb_xage + (JHe_1_whc * DC/F_SCLM_min)))/(Ra)), index= DC)
RRa_Phcry_SCLM_sb_xage_whc_max3He= pd.DataFrame(((1/(HeR_SCLM_sb_xage + (JHe_1_whc * DC/F_SCLM_max)))/(Ra)), index= DC)

RRa_Phcry_mix_whc= pd.DataFrame(((1/(HeR_mix + (JHe_1_whc * DC/F_mix)))/(Ra)), index= DC)
RRa_Phcry_mix_uc= pd.DataFrame(((1/(HeR_mix + (JHe_1_uc * DC/F_mix)))/(Ra)), index= DC)

# For all possible mixing fractions (variation of the fraction of HIMU f_HIMU)
# Index names represent DC (km) and column names represent the fraction of HIMU into the mixture 
RRa_Phcry_mix_all_whc= [(1/(HeR_mix_all[i] + (JHe_1_whc * DC/F_mix_all[i])))/(Ra) for i in range(len(f_HIMU_all))]
dfRRa_Phcry_mix_all_whc= pd.DataFrame(data= np.transpose(RRa_Phcry_mix_all_whc), columns= (i for i in f_HIMU_all), index= DC)

# RETRIEVING DC for HeR_phenocrysts (HeR_phcry_trgt = 0.93 Ra)
RRa_Phcry= 0.93                                #Average R/Ra for phenocrysts in the zone of study (Data of MArtelli et al. 2004, see excel file_ final calc.)
HeR_phcry_trgt = 1/ (RRa_Phcry * Ra)

DC_SCLM= (HeR_phcry_trgt - HeR_SCLM_sb_xage) * F_SCLM / JHe_1_whc
print("DC_SCLM= ", round(DC_SCLM, 1), "km")

DC_SCLM_min= (HeR_phcry_trgt - HeR_SCLM_sb_xage) * F_SCLM_min / JHe_1_whc
print("DC_SCLM_min3He= ", round(DC_SCLM_min, 1), "km")

DC_SCLM_max= (HeR_phcry_trgt - HeR_SCLM_sb_xage) * F_SCLM_max / JHe_1_whc
print("DC_SCLM_max3He= ", round(DC_SCLM_max, 1), "km")

DC_SCLM_GM= (HeR_phcry_trgt - HeR_SCM) * F_SCLM_GM / JHe_1_whc
print("DC_SCLM_GM= ", round(DC_SCLM_GM, 1), "km")

DC_HIMU= (HeR_phcry_trgt - HeR_HIMU) * F_HIMU / JHe_1_whc
print("DC_HIMU= ", round(DC_HIMU, 1), "km")

DC_mix= (HeR_phcry_trgt - HeR_mix) * F_mix / JHe_1_whc
print("DC_mix= ", round(DC_mix, 1), "km")

# For all possible mixing fractions (variation of the fraction of HIMU f_HIMU)
DC_mix_all_f= [(HeR_phcry_trgt - HeR_mix_all[i]) * F_mix_all[i] / JHe_1_whc for i in range(len(f_HIMU_all))]
DC_mix_all= [round (i,2) for i in DC_mix_all_f]
print ("f_HIMU_all= ", f_HIMU_all)
print("DC_mix_all", DC_mix_all)

#PLOTTING

# FIGURE 1
fig1, ax = plt.subplots()
plt.plot(DC, np.ones(len(DC))*RRa_Phcry, color= "green", label="Phenocrysts' 3He/4He")

plt.plot(DC, RRa_Phcry_HIMU_whc, "r", label="HIMU; F_3He= "+str(F_HIMU/10000)+"; $\\mathbf{DC=} \\mathbf{"+str(round(DC_HIMU, 1))+"}$", alpha= 0.5)
# plt.plot(DC, RRa_Phcry_HIMU_uc, "r--", label="HIMU_uc") 

plt.plot(DC, RRa_Phcry_SCM_whc, "b", label="SCLM_ G&M; F_3He= "+str(F_SCLM_GM/10000)+"; $\\mathbf{DC=} \\mathbf{"+str(round(DC_SCLM_GM, 1))+"}$", alpha= 0.5)
# plt.plot(DC, RRa_Phcry_SCM_uc, "b--", label="SCLM_uc")

plt.plot(DC, RRa_Phcry_SCLM_sb_xage_whc, "k", label="SCLM_ "+str(AgeSCLM)+"Ma; F_3He_av.= "+str(F_SCLM/10000)+"; $\\mathbf{DC=} \\mathbf{"+str(round(DC_SCLM, 1))+"}$")
# plt.plot(DC, RRa_Phcry_SCLM_sb_xage_uc, "k--", label="SCLM"+str(AgeSCLM)+"_uc")

plt.plot(DC, RRa_Phcry_SCLM_sb_xage_whc_min3He, "k-.", label="SCLM_ "+str(AgeSCLM)+"Ma; F_3He_min= "+str(F_SCLM_min/10000)+"; $\\mathbf{DC=} \\mathbf{"+str(round(DC_SCLM_min, 1))+"}$")
plt.plot(DC, RRa_Phcry_SCLM_sb_xage_whc_max3He, "k--", label="SCLM_ "+str(AgeSCLM)+"Ma; F_3He_max= "+str(F_SCLM_max/10000)+"; $\\mathbf{DC=} \\mathbf{"+str(round(DC_SCLM_max, 1))+"}$")

plt.plot(DC, RRa_Phcry_mix_whc, color= "dodgerblue", label="SCLM-HIMU mix; F_3He_mix= "+str(F_mix/10000)+"; $\\mathbf{DC=} \\mathbf{"+str(round(DC_mix, 1))+"}$", alpha= 1)


# plt.title("Evolution of source R/Ra with delamination", fontweight='bold')                            #DC vs R/Ra(phenocrysts)
plt.xlabel("Delaminated crust thickness (DC in km)", fontweight='bold', fontsize= 13) 
plt.ylabel("$\mathbf{^3He/^4He}$ (R/Ra)", fontweight='bold', fontsize= 13)
# plt.grid()
ax.annotate("6.7Ra", xy=(1.5, 6.5), xytext=(1.5, 6.5), color= 'red', alpha= 0.5)
ax.annotate("6.1Ra", xy=(1.5, 6), xytext=(1.5, 6), color= 'blue', alpha= 0.5)
ax.annotate("4.5Ra", xy=(1.5, 4.5), xytext=(1.5, 4.5), color= 'dodgerblue', alpha= 1)

ax.annotate(str(round(df_He_SCLMdt.loc[AgeSCLM,"RRa_SCLM_sb"], 1))+"Ra", xy=(0.5, df_He_SCLMdt.loc[AgeSCLM,"RRa_SCLM_sb"]),
            xytext=(0.5, df_He_SCLMdt.loc[AgeSCLM,"RRa_SCLM_sb"]), color= 'black')
ax.annotate(str(RRa_Phcry)+"Ra", xy=(43, 1.1), xytext=(43, 1.1), color= 'green')
# ax.annotate("F_3He_SCLM_av.= "+str(F_SCLM), xy=(30, 7.8), xytext=(30, 7.8))
# ax.annotate("F_3He_SCLM_min= "+str(F_SCLM_min), xy=(30, 7.2), xytext=(30, 7.2))
# ax.annotate("F_3He_SCLM_max= "+str(F_SCLM_max), xy=(30, 6.6), xytext=(30, 6.6))
# ax.annotate("F_3He_ HIMU= "+str(F_HIMU), xy=(30, 6.0), xytext=(30, 6.0))

# indicating DC by vertical lines (intercept btn curves of evolution and R/Ra= 0.82)
# for dc in [DC_SCLM,DC_mix]:
#     plt.axvline(x= dc, color='red', linestyle='dashed', linewidth=1)
#     plt.text(dc, 0.1, f'dc= {dc}', rotation=90, verticalalignment='bottom')

plt.legend(loc= "upper right")
plt.xlim(-0.3,50)
plt.ylim(0,8.5)
plt.savefig('Helium models_DC thicknesses_ALL.svg', format='svg', bbox_inches='tight')


# FIGURE 2
# PLot for different possible mixtures (with different f_HIMU)
fig2, ax= plt.subplots()
handle_phen= ax.plot(DC, np.ones(len(DC))*RRa_Phcry, color= "green")
handle_HIMU= ax.plot(DC, RRa_Phcry_HIMU_whc, "r", alpha= 0.5)
handle_sclm_sb= plt.plot(DC, RRa_Phcry_SCLM_sb_xage_whc, "k")
curve_handles= []
for i in dfRRa_Phcry_mix_all_whc.columns:
    curve, = ax.plot(DC, dfRRa_Phcry_mix_all_whc.loc[:, i], linestyle= "-", color= "dodgerblue", linewidth= 1.1)
    curve_handles.append(curve)
    handle_smantle= ax.scatter(DC[0], dfRRa_Phcry_mix_all_whc.loc[0, i], color= "magenta", s= 20)

handle_HIMU_em= ax.scatter(DC[0], RRa_HIMU, marker= "*", color= "red", s= 100 )
handle_sclm_em= ax.scatter(DC[0], RRa_SCLM_sb_xage, marker= "*", color= "black", s= 100 )

#plotting the table of values of f_HIMU and DC
#Data
f_M_table= [0] + f_HIMU_all + [1]
DC_table= [DC_SCLM] + DC_mix_all + [DC_HIMU] 
f_HIMU_n_dc_data= {" f - A ":f_M_table, " DC ":[round(i,1) for i in DC_table]}
f_HIMU_n_dc_tabledata= []
for key, values in f_HIMU_n_dc_data.items():
    f_HIMU_n_dc_tabledata.append([key] + values)
    
table_f_HIMU_n_dc= ax.table(cellText=f_HIMU_n_dc_tabledata, loc='top')
table_f_HIMU_n_dc.auto_set_font_size(False)
table_f_HIMU_n_dc.set_fontsize(9)
# table_f_HIMU_n_dc.set_fontfamily("monospace")
table_f_HIMU_n_dc.scale(1, 1)  # Adjust the size of the table

plt.xlabel("Delaminated crust thickness (DC in km)", fontweight='bold', fontsize= 13) 
plt.ylabel("$\mathbf{^3He/^4He}$ (R/Ra)", fontweight='bold', fontsize= 13)
plt.legend([handle_HIMU_em, handle_sclm_em, handle_smantle, handle_HIMU[0], handle_sclm_sb[0], curve_handles[0], handle_phen[0]],
           ["Starting HIMU signature", "Starting SCLM signature", "Starting mixture signatures", "Evolution of the HIMU signature", 
            "Evolution of the SCLM signature", "Evolution of the mixtures", "Phenocrysts' 3He/4He"])
ax.annotate(str(RRa_Phcry)+"Ra", xy=(43, 1.1), xytext=(43, 1.1), color= 'green')

plt.xlim(-0.3,50)
plt.ylim(0,8.5)
plt.savefig('Helium models_ DC thicknesses_SCLM-HIMU.svg', format='svg', bbox_inches='tight')
# plt.close()
plt.show()

# POST-ERUPTION CONTAMINATON
# The delaminated crust - contaminated magma is prone to contamination by the remaining 20km-thick crust upon eruption.
# The starting magma signature is that recorded in Phenocrysts, and the 3He/4He ratio pursuant shallow crust contamination is calculated below
# Equation 2 is used, variables are RRa_Phcry, F_3He_LAmix, SCT , JHe_1_whc, RRa_surf

F_3He_LAmix1= [j*10000 for j in np.arange(1, 3.75, 0.25)]            
SCT= 20                                           #Shallow crust thickness (km)   
He4He3_Phcry= 1 / (RRa_Phcry*Ra)
RRa_surf= []
for i in F_3He_LAmix1:
    RRa_surf_i= (1/((((He4He3_Phcry * i) + (JHe_1_whc * SCT)) / i))) / Ra
    RRa_surf.append(RRa_surf_i)
    
dfRRasurf= pd.DataFrame({"F_3He": F_3He_LAmix1, "RRa_surf": RRa_surf})
dfRRasurf.index= np.arange(1, 3.75, 0.25)
print()
print(dfRRasurf)
    

"""
#INDIVIDUAL PLOTS

#SCLM
fig, ax = plt.subplots()
plt.plot(DC, RRa_Phcry_SCM_whc, "b", label="SCLM_whc", alpha= 0.5)
# plt.plot(DC, RRa_Phcry_SCM_uc, "b--", label="SCLM_uc", alpha= 0.5)

plt.plot(DC, RRa_Phcry_SCLM_sb_xage_whc, "k", label="SCLM"+str(AgeSCLM)+"_whc")
# plt.plot(DC, RRa_Phcry_SCLM_sb_xage_uc, "k--", label="SCLM"+str(AgeSCLM)+"_uc")

plt.plot(DC, RRa_Phcry_SCLM_sb_xage_whc_min3He, "k")
plt.plot(DC, RRa_Phcry_SCLM_sb_xage_whc_max3He, "k")

plt.plot(DC, np.ones(len(DC))*0.88, "g", label="Phenocrysts")

# plt.title("Evolution of source R/Ra with delamination", fontweight='bold')                            #DC vs R/Ra(phenocrysts)
plt.xlabel("Delaminated crust thickness (km)", fontweight='bold') 
plt.ylabel("R/Ra (phenocrysts)", fontweight='bold')
# plt.grid()
ax.annotate("6.1Ra (SCLM)", xy=(1.5, 6), xytext=(1.5, 6), color= 'blue')
ax.annotate("0.88Ra", xy=(43, 1), xytext=(43, 1), color= 'green')
ax.annotate("3He flux_ SCLM= "+str(F_SCLM), xy=(31, 7.8), xytext=(31, 7.8))
plt.legend(loc= "center right")
plt.xlim(-0.3,50)
plt.ylim(0,8.5)

#HIMU
fig1, ax = plt.subplots()

plt.plot(DC, RRa_Phcry_HIMU_whc, "r", label="HIMU_whc")
plt.plot(DC, RRa_Phcry_HIMU_uc, "r--", label="HIMU_uc") 
plt.plot(DC, np.ones(len(DC))*0.88, "g", label="Phenocrysts")

# plt.title("Evolution of source R/Ra with delamination", fontweight='bold')                            #DC vs R/Ra(phenocrysts)
plt.xlabel("Delaminated crust thickness (km)", fontweight='bold') 
plt.ylabel("R/Ra (phenocrysts)", fontweight='bold')
# plt.grid()
ax.annotate("8Ra (HIMU)", xy=(1.5, 7.8), xytext=(1.5, 7.8), color= 'red')
ax.annotate("0.88Ra", xy=(43, 1), xytext=(43, 1), color= 'green')
ax.annotate("3He flux_ HIMU= "+str(F_HIMU), xy=(31, 7.2), xytext=(31, 7.2))
plt.legend(loc= "center right")
plt.xlim(-0.3,50)
plt.ylim(0,8.5)

"""