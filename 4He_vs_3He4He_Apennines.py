# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 22:42:51 2024

@author: jdlpizerumug
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

dfnobles= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\dfnobles_output.xlsx")
dfnobles.set_index(['annot'], inplace=True) 
dfendmembers= pd.read_excel(r"C:\Users\jdlpizerumug\Documents\DOCS_msi\PhD@UniPau\ACADEMICS\python_phD\endmembers.xlsx", index_col=("Environment"))


# dataset
x_data = dfnobles.loc[(j for j in dfnobles.index!=3),"4He"]
y_data = dfnobles.loc[(j for j in dfnobles.index!=3),"R/Ra"]

# Fitting a line (polynomial of degree 1) to the data
coefficients = np.polyfit(x_data, y_data, 1)
poly = np.poly1d(coefficients)
print("Coefficients:", coefficients)

# Generating the line of best fit
x_fit = np.linspace(min(x_data), max(x_data), 1000)
y_fit = poly(x_fit)

fig, ax = plt.subplots()
plt.scatter(x_data, y_data, color= "blue", label='4He vs 3He/4He')
plt.plot(x_fit, y_fit, color='red', label='Line of Best Fit')
plt.xlabel("$\mathrm{^{4}He}$ (ppm)", fontweight='normal', fontsize= 13)
plt.ylabel("$\mathrm{^{3}He/^{4}He}$ (R/Ra)", fontweight='normal', fontsize= 13)
plt.xlim(0, 1.4*10**-5)
plt.ylim(-0.1, 8)
for i in dfnobles.index:
    if i==19 or i==18:
        ax.annotate(i, xy=(dfnobles.loc[i,"4He"], dfnobles.loc[i,"R/Ra"]), 
                    xytext=(10, 5), ha='center', va='top',
                    textcoords='offset points')
    elif i==3:
        continue
    else:
        ax.annotate(i, xy=(dfnobles.loc[i,"4He"], dfnobles.loc[i,"R/Ra"]), 
                    xytext=(-7.5, 5), ha='center', va='top',
                    textcoords='offset points')
# CALCULATION OF R_SQUARED
# Reshaping x_data into a 2D array if it's a single feature
x_data = (np.array(x_data)).reshape(-1, 1)

# Fitting the linear regression model
model = LinearRegression().fit(x_data, y_data)

# Getting the coefficient of determination (R^2)
r_squared = model.score(x_data, y_data)
print("R^2:", round(r_squared, 2))
plt.annotate((f"R2= {round(r_squared, 2)}"), xy=(1.1*10**-5, 0.7), 
             xytext= (1.1*10**-5, 0.7), color="red")


plt.legend()

plt.savefig('4He_vs_3He4He_Apennines.svg', format='svg', bbox_inches='tight')

plt.show()

