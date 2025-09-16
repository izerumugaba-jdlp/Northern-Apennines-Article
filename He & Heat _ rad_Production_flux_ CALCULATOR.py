# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:06:39 2024

@author: jdlpizerumug
"""
# This calculator works in exactly the same way as calculations of O'nions and Oxburgh (1983) as we obtain the same values for JHe and q, for U=6.8ppm, h=8, dr=8.
# Not surprising for helium as exactly the same formula is used, but great for heat as constants are given in o'inons, but here we consider that K contributes 15% of total q

# Reminder of the relevant constants
U_ppm= (5/1000)                                   
Th_ppm= U_ppm * 3.8
                                
dr= 3.3                     # rock density in g/cm3
h= 700                      # He, Heat-generating thickness (km)

# HELIUM PRODUCTION RATE & HELIUM FLUX

# JHe1= 0.2355 * 10**-12 * U_ppm * (1 + (0.123 * (Th_ppm/U_ppm -4))) 

def calculate_total_helium_flux(U_ppm, Th_ppm):
    # 1. The rate of production of He4 (JHe) is calculated in cm3 STP He4 g-1rock yr-1 (Torgersen 1980; Eqn3) as follows
    JHe1= 0.2355 * 10**-12 * U_ppm * (1 + (0.123 * (Th_ppm/U_ppm -4)))  #He production rate in cm3 STP He4 g-1rock yr-1
    
    # 2. Multiplying by the density of the rock (dr) in g cm-3, we obtain JHe in V He4 per V rock (cm3 STP He4 yr-1 cm-3rock)
    JHe_V_He4_per_V_rock= dr * JHe1
    
    # 3. Multiplying by the thickness of U, Th - containing horizon; say a thickness of h km (h * 100 000 cm), 
    #We obtain the flux of He4 in cm3 STP He4 cm-2 yr-1
    flux_He4_n3= JHe_V_He4_per_V_rock * h * 10**5           #in cm3 STP He4 cm-2 yr-1
    
    # 4. Converting cm2 to m2 and yr in s; m2_in_a_cm2= 0.0001 (1*10**-4), # seconds in a year= 31557600 (365.25 * 24 * 3600)   
    flux_He4_n4= flux_He4_n3/ (0.0001 * 31557600)
    
    # 5. Converting the volume of He to atoms from cm3 STP He4 to atoms He4, to obtain the He4 flux JHe in atoms He4 m-2 s-1
    # nAtoms= (N * d * v/ mw) # (education.jlab.org/qa/mathatom_03.html)
    N= 6.022 * 10**23               #Avogadro's number atoms/mole
    d_He= 0.1784 * 10**-3           #density of helium (g/cm3)
    mw_He= 4                        #molecular weight of helium (g/mole)
    JHe= flux_He4_n4 * N * d_He / mw_He
    
    return JHe1, JHe

JHe1, JHe = calculate_total_helium_flux(U_ppm, Th_ppm)
print (f"* JHe1= {JHe1:.2e} cm3 STP He4 g-1rock yr-1 #Helium production")
print()

print (f"* JHe= {JHe:.1e} atoms_He4 m-2 s-1 #Helium Flux")
print()


# HEAT PRODUCTION RATE & HEAT FLUX (Ruedas, 2017)

#Heat production rate per nuclide (W/Kg)
HU1= 9.8314 * 10**-5
HTh1= 2.636817 * 10**-5

#Heat Production rate (W/Kg)
HUm= HU1 * U_ppm * 10**-6            #W/kg
HThm= HTh1 * Th_ppm *10**-6          #W/kg
HKm= ((HUm + HThm)/85)*15            #W/kg
Hm= HUm + HThm + HKm                 #W/kg

#Heat Production rate (mWm-3)
HU= HU1 * U_ppm * 10**-6 * 10**3 * dr * 10**3              #mW m-3
HTh= HTh1 * Th_ppm *10**-6 * 10**3 * dr * 10**3            #mW m-3
HK= ((HU + HTh)/75)*25                                     #mW m-3
H= HU + HTh + HK                                           #mW m-3

#Heat flow (mW m-2)
qU= HU1 * U_ppm * dr * h * 10**3            #mW m-2
qTh= HTh1 * Th_ppm * dr * h * 10**3         #mW m-2
qK= ((qU + qTh)/85)*15                      #mW m-2
q= qU + qTh + qK                            #mW m-2

# Printing solutions
print (f"* H= {Hm:.2e} W/kg")
print()
print (f"* H= {Hm:.2e} mW m-3")
print()
print (f"* q= {round(q, 2)} mW m-2")
print()