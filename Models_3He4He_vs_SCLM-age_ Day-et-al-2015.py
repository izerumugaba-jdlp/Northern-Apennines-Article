# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 19:28:15 2024

@author: jdlpizerumug
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from sympy import symbols, Eq, solve

"""
Day et al. 2015 propose a mainly closed system model for the 3He and 4He systematics in the SCLM, 
where the radiogenic production of 4He in the phenocrysts; xenocrysts mineral lattice causes the evolution
(i.e reduction) of the 3He/4He with time.
--> check out McDonough, 1990; Pearson and Wittig, 2008 to see why u would have a conservative SCLM while it sits
directly onto the asthenosphere. WHY ISN'T THERE 3He flux in asthenosphere (or is it considered in the model)

This is an improvement onto Gautheron and Morreira 2002, who had proposed an open system model where there is a
steady state situation in the SCLM with respect to Helium: constant 4He production and constant 3He influx from the
asthenosphere.

The model by Day et al 2015:
    He3/He4_SCLM= (He3_o / f) + (He3_A * m) / (He4_o / f) + (He4_A * m) + (px /f)
    
    with: 
        He3_o and He4_o: initial inventory of He in the SCLM at the time of formation
        He3_A and He4_A: The concentrations of Helium in the asthenosphere
        m, f: the mass-balance fractions of metasomatism and flux into other terrestrial reservoirs from the CLM
        px: He4 production ratio in cm3 STP yr-1 (after Graham et al 1987; for time<10 Myr!!)
        
        px= JHe= 2.8 * 10**-8 * (4.35 + ThU) * U * t 
        with:
            ThU= Th/U
            U= Concentration of Uranium in ppm. for the typical SCLM, U= 4 - 40 ppb, Th/U= 3.5 (page 126)
            t= time in Myr   
"""

#The formula below for Px is checked; we obtain the same value as Day et al using parameters of sample PHN 5273.
#i.e for t= 1179 Ma, Px= 17800 ncm3 STP g-1 (17.8 µcm3 STP g-1); p125. 
#but Graham et al use it for t<10**7 yrs i.e t<10Ma
#Note that Day et al 2015 do not cube the n, µ prefixes! they use them just to indicate powers of 6 and 9
#To reproduce fig 7 of Day et al 2015 we consider separate U contents for closed (b) vs open (g) system models
#...Hence the He production is also separate (but in both cases we can of course attribute the same values)

U_sclm_d_b= 0.04                                # Cratonic lith. (250km; 0.004 - 0.01 ppm U)
U_sclm_d_g= 0.004                               # Non cratonic lith. (100-150km; 0.01 - 0.04 ppm U)
# ppm; normally sclm  U= 4 - 40 ppb (p126). take average?                             
# but if a number in this range we get a very quick change. The concentration in U affects greatly the rate of change
# Also the initial concentration in 4He. quick change if 0.01 and slowest if 1; fig 6
ThU_sclm_d= 3.5                                  #ratio Th/U= ~3.5 (p126)
t= np.arange(0, 4500, 1) 
# 4He production in a CLOSED system                                         #Myr
Px_b= 2.8 * 10**-8 * (4.35 + ThU_sclm_d) * U_sclm_d_b * t 
Px_b_m= Px_b * 10**6
Px_b_n= Px_b * 10**9                                 # ncm3 STP g-1 yr-1

# 4He production in an OPEN system
Px_g= 2.8 * 10**-8 * (4.35 + ThU_sclm_d) * U_sclm_d_g * t 
Px_g_m= Px_g * 10**6
Px_g_n= Px_g * 10**9 

# print("Px_b_m= ", Px_b_m, "cm3 STP g-1 yr-1")
# print("Px_g_m= ", Px_g_m, "cm3 STP g-1 yr-1")

print()

# He concentration in the asthenosphere.  
# p122_ recent peridotite olivine and cpx from Vitim (Siberia) with 7.3 - 9.6 Ra showed He4 of 2 - 40 ncm3 STP g-1 4He
He4_A= 1                                             #µcc STP g 4He
Ra_A= 8                                              
He3_A= He4_A * Ra_A * 1.4 * 10**-6                   #µcc STP g 3He
# print("He3_A= ", He3_A, "ncm3 STP g-1 4He ")

#Initial inventory of He in the SCLM
# We use the same starting Ra and 4He content of sclm as asthenosphere (reasonable, prior to beginning of cooling)
He4_o= 1                                             #µcc STP g 4He
Ra_o= 8
He3_o= He4_o * Ra_o * 1.4 * 10**-6                   #µcc STP g 3He
print("He3_o= ", He3_o, "ncm3 STP g-1 4He ")
print("He3_A= ", He3_A, "ncm3 STP g-1 4He ")
print()

#Fractions of helium contributed by metasomatism (influx from MORB; m) and flux out from SCLM (f). Note they are fractions relative to the initial He concentration in the SCLM. 
#Trying to use values used in Day et al 2015_ fig 7.
#Values of f and m in the following dataframe; in clmn names s: solid, d: dashed, b:black, g:grey. (fig 7) 

#Closed system, 4He in growth
f_sb= 0.1           # flux out from the SCLM 
m_sb= 1             # flux in from the asthenosphere

f_db= 1
m_db= 1

#Open system
f_sg= 0.9           # They say flux out is 10% but typo? given open system, flux out should be high! here fluxout= 90% 
m_sg= 10

f_dg= 10
m_dg= 10

#Saving f and m parameters to a dataframe
# with data
data_mf = {'sb': [f_sb, m_sb], 'db': [f_db, m_db], 'sg': [f_sg, m_sg], 'dg': [f_dg, m_dg]}

# Create DataFrame of m and f values
df_mf = pd.DataFrame(data_mf, index=['f', 'm'])
print(df_mf)
print()

# Calculation of He3/He4 in the SCLM for different flux in & flux out values of 3He and 4He
# For the following formulas all units of He3 and He4 are in µcc STP g He; f and m are unitless, and hence He3/He4 is unitless. 
# For the flux out, why do we divide by percentage, rather than remaining with 90% (given 10% fluxed out?!)
He3_He4_SCLM_sb= ((He3_o / f_sb) + (He3_A * m_sb)) / ((He4_o / f_sb) + (He4_A * m_sb) + (Px_b_m /f_sb))
RRa_SCLM_sb= He3_He4_SCLM_sb / (1.4 * 10**-6)

He3_He4_SCLM_db= ((He3_o / f_db) + (He3_A * m_db)) / ((He4_o / f_db) + (He4_A * m_db) + (Px_b_m /f_db))
RRa_SCLM_db= He3_He4_SCLM_db / (1.4 * 10**-6)

He3_He4_SCLM_sg= ((He3_o / f_sg) + (He3_A * m_sg)) / ((He4_o / f_sg) + (He4_A * m_sg) + (Px_g_m /f_sg))
RRa_SCLM_sg= He3_He4_SCLM_sg / (1.4 * 10**-6)

He3_He4_SCLM_dg= ((He3_o / f_dg) + (He3_A * m_dg)) / ((He4_o / f_dg) + (He4_A * m_dg) + (Px_g_m /f_dg))
RRa_SCLM_dg= He3_He4_SCLM_dg / (1.4 * 10**-6)

# print ("He3/He4= ", He3_He4_SCLM)
# print ("R/Ra= ", RRa_SCLM)


# ADDING THE EFFECT OF 4He PRODUCTION IN THE DELAMINATED CRUST
# 4He poduction_ parameters for the zone of study_ see the excel table
U_dc= 1.58                 #in ppm; average U content of the crust in the zone of study
Th_dc= 6.39
ThU_dc= Th_dc / U_dc
t_dc= 500                 #Age of the crust in our zone of study. considered the oldest possible

Pdc= 2.8 * 10**-8 * (4.35 + ThU_dc) * U_dc * t_dc  # cm3 STP g-1 yr-1 
Pdc_m= Pdc * 10**6                                 # µcm3 STP g-1 yr-1 
Pdc_n= Pdc * 10**9                                 # ncm3 STP g-1 yr-1 

# CALCULATION OF NEW R/Ra accounting for 4He production in the crust
# We could do this option as below but the delaminated crust thickness is not taken into consideration
# To do it, need to do units conversion by multiplying by the density of the rock to go from g-1 to cm-3; 
#.... only that we would have to do on all parameters, including those of the SCLM and MORB.
# need to find a way to incorpoprate the thickness in the formula above (to quantify the delaminated crust)
# For comparison, i incorporated the following R/Ra that incl. delaminated crust (4.5Ga) contribution , into the exported df
# We note that the delaminated crust affects quickly and hugely the RRa, even for a crust of 500Ma, where RRa= 0.44
# The point above is when we assume all 4He produced is released, it is prone to change if we apply a fraction of release.

He3_He4_SCLM_sb_dc= ((He3_o / f_sb) + (He3_A * m_sb)) / ((He4_o / f_sb) + (He4_A * m_sb) + (Px_b_m /f_sb) + (Pdc_m) )
RRa_SCLM_sb_dc= He3_He4_SCLM_sb_dc / (1.4 * 10**-6)

# SAVING ALL THE ABOVE DATA INTO A DATAFRAME
df_He_SCLM_data= {"Age (Myr)":t ,"Px_b_m(closed)":Px_b_m, "Px_g_m(open)":Px_g_m,"RRa_SCLM_sb_dc":RRa_SCLM_sb_dc, 
                  "RRa_SCLM_sb": RRa_SCLM_sb, "RRa_SCLM_db": RRa_SCLM_db, "RRa_SCLM_sg": RRa_SCLM_sg, "RRa_SCLM_dg": RRa_SCLM_dg}

df_He_SCLM= pd.DataFrame(df_He_SCLM_data)
df_He_SCLM.set_index("Age (Myr)", inplace=True)

#Exporting the dataframe
#We will use this data to extract exact 3He/4He signatures of the SCLM at specific ages
df_He_SCLM.to_excel('df_He_SCLM.xlsx', index=True)

RRa_Phcry= 0.93
#Finding ages where the 3He/4He is equal to RRa_Phcry
age_sb_RRa_Phcry= np.argmin(np.abs(df_He_SCLM["RRa_SCLM_sb"] - RRa_Phcry))
age_db_RRa_Phcry= np.argmin(np.abs(df_He_SCLM["RRa_SCLM_db"] - RRa_Phcry))


# EXTRACTING PRECISE AGES
age_req= 20
RRa_min_closed= df_He_SCLM.loc[age_req, "RRa_SCLM_sb"]
RRa_max_closed= df_He_SCLM.loc[age_req, "RRa_SCLM_db"]
RRa_min_open= df_He_SCLM.loc[age_req, "RRa_SCLM_sg"]
RRa_max_open= df_He_SCLM.loc[age_req, "RRa_SCLM_dg"]
print()
print(f"* RRa_min_{age_req}= {round(RRa_min_closed, 2)}     #RRa_min_closedsystem at t= {age_req} Ma")
print(f"* RRa_mmax_{age_req}= {round(RRa_max_closed, 2)}   #RRa_max_closedsystem at t= {age_req} Ma")
print(f"* RRa_min_{age_req}= {round(RRa_min_open, 2)}    #RRa_min_opensystem at t= {age_req} Ma")
print(f"* RRa_mmax_{age_req}= {round(RRa_max_open, 2)}    #RRa_max_opensystem at t= {age_req} Ma")


# age_sb_RRa_Phcry = df_He_SCLM[RRa_SCLM_sb].apply(lambda x: round(x, 2)).values[np.argmin(np.abs(df[RRa_SCLM_sb] - RRa_Phcry))]

#PLOTTING
fig, ax= plt.subplots()
plt.plot(t, RRa_SCLM_sb, "k", label= "closed system; f= 0.1; m= 1")
plt.plot(t, RRa_SCLM_db, "k--", label= "closed system; f= 1; m= 1")
plt.plot(t, RRa_SCLM_sg, "k", alpha= 0.3, label= "open system; f= 0.9; m= 10")
plt.plot(t, RRa_SCLM_dg, "k--", alpha= 0.3, label= "open system; f= 10; m= 10")
plt.axvline(x=300, color='r', linestyle='--')        #, label= "SCLM age= 300Ma"
# plt.axvline(x= age_req, color='b', linestyle='--')        #, label= "SCLM age= 300Ma"
# plt.axvline(x= age_sb_RRa_Phcry, color='r', linestyle='--')        #, label= "SCLM age where R/Ra==0.93 (phenocrysts value)"
# plt.axvline(x= age_db_RRa_Phcry, color='r', linestyle='--') 

plt.axhline(y= RRa_Phcry, color='g', linestyle='-')  #, label= str(RRa_Phcry)+"Ra"
ax.annotate(str(RRa_Phcry)+"Ra", xy=(3*10**3, 1.2), xytext=(3*10**3, 1.2), color= 'green')
ax.annotate("300 Ma", xy=(3.5*10**2, 5), xytext=(3.5*10**2, 5), color= 'red', rotation= 90)

"""
ax.annotate(f"{age_sb_RRa_Phcry}"+" Ma", xy=(age_sb_RRa_Phcry, 5), xytext=(10,0), color="red", rotation= 90,
            ha='center', va='center', textcoords='offset points')
ax.annotate(f"{age_db_RRa_Phcry}"+" Ma", xy=(age_db_RRa_Phcry, 5), xytext=(10,0), color="red", rotation= 90,
            ha='center', va='center', textcoords='offset points')
"""

plt.xscale("log")
plt.xlabel("SCLM Age (Myrs)", fontsize=13) 
plt.ylabel("$\mathrm{^3He/^4He \ (R/Ra)}$", fontsize=13)
plt.xlim(10**0, 10**4)
plt.ylim(-0.5, 10)
plt.legend(loc= "center left", bbox_to_anchor=(0, 0.3), fontsize= 9)

plt.savefig('Helimum-models_SCLM__Day-et-al-2015.svg', format='svg', bbox_inches='tight')
plt.show()

#GENERAL COMMENTS
# Given the shapes of the curves obtained, it is probable that Day et al 2015 used 
# ...0.004ppm (4ppb) for the open system curves (grey/yellow), and 0.04 ppm (40ppb) for the closed system ingrowth,
# ...as the U concentrations in the SCLM. (Th/U is maintained at 3.5)
# (or else they take different starting concentrations of 4He)
# The taken U concentration greatly affects the rate of evolution of R/Ra

# The question is, will we do the same (for comparison?), or do we rather take an average U concentration?! 

# In figure 7, it is clear that they take 1 µcc STP g 4He as their starting 4He concentration. 
# Presented here, we also take 1 µcc STP g 4He. But in their fig 6, they present cases where they also take 0.1, 0.01 
# These values of starting 4He greatly affect the rate of evolution of R/Ra (see fig6)

# Which values of starting 4He should we consider? this value needs to be chosen very carefully!!
# For instance Day et al 2015 suggest measured values of olivine peridotites of Satim (Europe) with RRa of 7.3 - 9.1
# ...(similar to DDM whose RRa is 8) of 4He to be 2 - 40 ncm3 STP g-1 4He. We could perhaps consider this or look for
# ...other values from a site more closer to ours (or similar geological settings?!)   

# In Fig. 7, Day et al 2015 reproduce the measured 3He flux in continents, given the following parameters:
    # A closed system is considered
    # Mass balance assuming 50% - 90% subject to closed system (yield 3He flux of 2.2 - 0.25 at s-1 cm-2; similar to <1 at s-1 cm-2 measured at continents)
    # They hence conclude that steady state models, while explaining 3He flux at ridges, they fail to agree with measured He flux on the continents.










