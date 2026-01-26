# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 21:38:21 2024

@author: jdlpizerumug
"""

import pandas as pd
import numpy as np
import math
from scipy.stats import t
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


dfnobles= pd.read_excel(r"C:\Users\ijdpe\Documents\DOCS_msi\PhD@UniPau\1. G3-ARTICLE ITALY-REVIEWS\Python_G3art_reviews\GasData_NorthernApennines.xlsx",
                        sheet_name= "Majors_Nobles_Plots", index_col= "annot")
dfendmembers= pd.read_excel(r"C:\Users\ijdpe\Documents\DOCS_msi\PhD@UniPau\1. G3-ARTICLE ITALY-REVIEWS\Python_G3art_reviews\Endmembers.xlsx", index_col= "Environment")
finaldata= pd.read_excel(r"C:\Users\ijdpe\Documents\DOCS_msi\PhD@UniPau\1. G3-ARTICLE ITALY-REVIEWS\Python_G3art_reviews\gasdata_budgets_final.xlsx", index_col="ID")


# dataset
x_data = dfnobles.loc[(j for j in dfnobles.index!=3),"3He"]
y_data = dfnobles.loc[(j for j in dfnobles.index!=3),"R/Ra"]



# AX1_ 3He vs 3He/4He
# Fitting a line (polynomial of degree 1) to the data
coefficients_ax1 = np.polyfit(x_data, y_data, 1)
poly = np.poly1d(coefficients_ax1)
print("Coefficients_ax1:", coefficients_ax1)

# Generating the line of best fit
x_fit = np.linspace(min(x_data), max(x_data), 1000)
y_fit = poly(x_fit)

# plotting ax1
fig, ax1 = plt.subplots()
data_ax1= ax1.scatter(x_data, y_data, color= "blue", label='3He vs 3He/4He')
fitline_ax1, = ax1.plot(x_fit, y_fit, color='red', label='Best fit (3He vs 3He/4He)')
ax1.set_xlabel("$\mathrm{^3He}$ (ppm)", fontweight='normal', fontsize= 13)
ax1.set_ylabel("$\mathrm{^{3}He/^{4}He}$ (R/Ra)", fontweight='normal', fontsize= 13) 

ax1.set_ylim(-0.1, 8)

for i in dfnobles.index:
    if i==18 or i==8:
        ax1.annotate(i, xy=(dfnobles.loc[i,"3He"], dfnobles.loc[i,"R/Ra"]), 
                    xytext=(9, 5), ha='center', va='top',
                    textcoords='offset points', color= "blue")
    elif i==3:
        continue
    else:
        ax1.annotate(i, xy=(dfnobles.loc[i,"3He"], dfnobles.loc[i,"R/Ra"]), 
                    xytext=(-7.5, 5), ha='center', va='top',
                    textcoords='offset points', color= "blue")
        
# calculation of r_squared
# Reshaping x_data into a 2D array if it's a single feature
x_data_ax1 = (np.array(x_data)).reshape(-1, 1)

# Fitting the linear regression model
model = LinearRegression().fit(x_data_ax1, y_data)

# Getting the coefficient of determination (R^2)
r_squared = model.score(x_data_ax1, y_data)
print("R^2 for ax1:", round(r_squared, 2))
plt.annotate((f"R2= {round(r_squared, 2)}"), xy=(1.1*10**-11, 0.7), 
             xytext= (1.1*10**-11, 0.7), color="red")
print()


# AX2_ 3He vs MANTELLIC CONTRIBUTIONS (%)
# ax2 and Creating ax2 for mantellic contribution
z_data = finaldata.loc[(j for j in finaldata.index!=3), "HIMU_He"]
ax2= ax1.twinx()

# Fitting a line (polynomial of degree 1) to the data
coefficients_ax2 = np.polyfit(x_data, z_data, 1)      #coefficients of the polynomial of first order z= mx + b
poly_ax2 = np.poly1d(coefficients_ax2)                # Saving coefficients into the polynomial calculator? 
print("Coefficients_ax2:", coefficients_ax2)



# Generating the line of best fit
x_fit_ax2 = np.linspace(min(x_data), max(x_data), 1000)
z_fit = poly_ax2(x_fit_ax2)

# plotting ax2
data_ax2 = ax2.scatter(x_data, z_data, color= "green", label='3He vs mantle fraction (%)')
fitline_ax2, = ax2.plot(x_fit, z_fit, color='fuchsia', label='Best fit (3He vs mantle fraction)')
ax2.set_ylabel("Mantle fraction (%)", fontweight='normal', fontsize= 13)
ax2.set_ylim(-0.1, 50)

df_3He_mf= pd.DataFrame({"3He": dfnobles.loc[:,"3He"], "HIMUfract_He": finaldata.loc[:,"HIMU_He"]})
# Annotate data on the secondary axis
for i in df_3He_mf.index:
    
    if i==7 or i==8 or i==14 or i==19 or i==20:
        ax2.annotate(i, (df_3He_mf.loc[i,"3He"], df_3He_mf.loc[i,"HIMUfract_He"]), 
                     textcoords="offset points", xytext=(0,-11), ha='center', color= "green")
    
    else:
        ax2.annotate(i, (df_3He_mf.loc[i,"3He"], df_3He_mf.loc[i,"HIMUfract_He"]), 
                     textcoords="offset points", xytext=(0,5), ha='center', color= "green")
    
# calculation of r_squared_ax2
# Reshaping x_data into a 2D array if it's a single feature
x_data_ax2 = (np.array(x_data)).reshape(-1, 1)

# Fitting the linear regression model
model = LinearRegression().fit(x_data_ax2, z_data)

# Getting the coefficient of determination (R^2)
r_squared_ax2 = model.score(x_data_ax2, z_data)
print("R^2 for ax2:", round(r_squared_ax2, 2))
ax2.annotate((f"R2= {round(r_squared_ax2, 2)}"), xy=(1.1*10**-11, 14), 
              xytext= (1.1*10**-11, 14), color="fuchsia")


# CALCULATING 2-TAILED P-VALUE (Probability that the observed correlation is not random, assuming the null hypothesis; 
# i.e the measure of the statistical significance of the observed correlation)

"""
VARIABLES EXPLAINED
# P_value= 2 * (1 - Tcdf(|t|, df))
# t (Test-statistic) is a standardized measure of how far the observed correlation deviates from zero, the larger |t| the stronger the evidence against the null hypothesis.

# t = r * math.sqrt(df / (1 - r**2)) [known as t-stat]
# r= math.sqrt(R^2)   [r is Pearson's degree of correlation, R^2 is the coefficient of determination]
# df= n-2 [Represents the number of independent data points available to estimate variability after fitting a linear relationship]
# n is the sample size

# Tcdf= The probability that a t-distributed random variable with df degrees of freedom is less than or equal to t.
"""
n= (dfnobles.shape[0]) - 1   #number of samples without including the anomalous sample 3.
df= n - 2

r= math.sqrt(r_squared)
t_stat = r * math.sqrt(df / (1 - r**2)) 
P_value= 2 * (1 - t.cdf(abs(t_stat), df))
print()
print(f"P_value = {P_value:.3f}")

r_ax2= math.sqrt(r_squared_ax2)
t_stat_ax2 = r_ax2 * math.sqrt(df / (1 - r_ax2**2)) 
P_value_ax2= 2 * (1 - t.cdf(abs(t_stat_ax2), df))
print()
print(f"P_value_ax2 = {P_value_ax2:.3f}")






# Legend handles and labels
handles = [data_ax1, fitline_ax1, data_ax2, fitline_ax2]
labels = [h.get_label() for h in handles]

fig.legend(handles, labels, loc= "center right", bbox_to_anchor=(0.90, 0.75))

plt.savefig('3He_vs_3He4He_vs_Mantle-fraction_Apennines.svg', format='svg', bbox_inches='tight')

plt.show()

"""
for i, (xi, yi) in enumerate(zip(x_data, z_data)):
    ax2.annotate(i, (xi, yi), textcoords="offset points", xytext=(0,10), ha='center')
    
--> Enumerate and zip functions are very important:
    Enumerate pairs each element in an iterable (say a list) with its index;
    Zip pairs two iterables element by element. 

"""