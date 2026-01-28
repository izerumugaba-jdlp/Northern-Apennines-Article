# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 18:55:03 2025

@author: jdlpizerumug
"""

import pandas as pd

# Constants
R = 0.082057  # L·atm/(mol·K) - ideal gas constant
T_STP = 273.15  # Kelvin
P_STP = 1  # atm

# Step 1: Calculating molar volume at STP using ideal gas law: PV= nRT i.e V = nRT/P
# For 1 mol: V_m = (R * T) / P
V_molar_L = (R * T_STP) / P_STP  # in liters
V_molar_cm3 = V_molar_L * 1000   # v converted to ml i.e cm3 (molar volume in cm3/mol)

print()
print(f"Molar volume at STP: {V_molar_cm3:.2f} cm3/mol\n") # SOLUTION= Molar volume at STP: 22413.87 cm3/mol

# Molar masses of He isotopes
MOLAR_MASS_3He = 3.016  # g/mol
MOLAR_MASS_4He = 4.0026  # g/mol

# Conversion function 
# Volume_cm3_STP to n_mol [n_mol= volume_cm3 / molar_volume]
def convert_cm3STP_to_mol (volume_cm3, molar_volume):
    return (volume_cm3 / molar_volume)

conversion_factor_4He_1cm3_to_mol= convert_cm3STP_to_mol (1, V_molar_cm3)
print(f"1 cm3 of 4He at STP= {conversion_factor_4He_1cm3_to_mol:.2e} mol of 4He\n")

v_4He= 6.87998E-12
n_mol_for_v_4He= v_4He * conversion_factor_4He_1cm3_to_mol
print(f"{v_4He} cm3 of 4He at STP= {n_mol_for_v_4He:.2e} mol of 4He\n")


#%%
# Volume_cm3_STP to mass_g
# Formula: mass_He(g) = (volume_He(cm3) / molar_volume (cm3/mol)) * molar_mass (g/mol)
def convert_cm3STP_to_grams(volume_cm3, molar_mass, molar_volume):
    return (volume_cm3 / molar_volume) * molar_mass

conversion_factor_4He= convert_cm3STP_to_grams(1, MOLAR_MASS_4He, V_molar_cm3)
print(f"1 cm3 of 4He at STP= {conversion_factor_4He:.2e} g of 4He")


