# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 14:08:35 2023

@author: Mona V.
"""


import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#METHOD 1 TO READ JSON DATA
#json_file = open('loan_data_json.json')
#data = json.load(json_file)

#METHOD 2 TO READ JSON DATA
with open('loan_data_json.json') as json_file:
    data = json.load(json_file)


#TRANSOFRM JSON FILE TO DATAFRAM
LoanData = pd.DataFrame(data) #credit ploicy = 1 means customer is eligible to get loan

LoanData.info()
LoanData.describe()
#finding unique values  or the purpose column
LoanData['purpose'].unique()

#describe the data for a specific column
LoanData['int.rate'].describe()
LoanData['fico'].describe()
LoanData['dti'].describe()

#--------------
#USING EXP() TO GET THE ANNUAL INCOME
income = np.exp(LoanData['log.annual.inc'])
LoanData['annual_income'] = income
print(LoanData['annual_income'])

#----------------------
#FICO score - Credit Score
#ERROR HANDLING

# fico >= 300 and < 400: very poor
# fico >= 400 and  < 600: poor
# fisco >= 601 and < 660: fair
# fico >= 660 and < 780: good
# fico >= 780 : excellent
   
FicoCategory = []    
for i in range(len(LoanData)):
    #category = 'Red'
    category = LoanData['fico'][i]
    try:
    
        if category >= 300 and category  < 400:
           cat = 'Very Poor'
        elif category  >= 400 and category  < 600:
           cat = 'Poor'
        elif category  >= 601 and category  < 660:
           cat = 'Fair'
        elif category  >= 660 and LoanData['fico'][i]  < 780:
           cat = 'Good'
        elif category  >= 780:
           cat = 'Excellent'
        else:
           cat = 'Unknown'
            
    except:
            cat = 'Unknown'
            print('error! fico is not available')
    FicoCategory.append(cat)
            
FicoCategory = pd.Series(FicoCategory)
LoanData['FicoCategory'] = FicoCategory

#------------------------------
#DF.LOC CONDITIONAL STATEMENTS
#syntax: df.loc[df[columnname] condition, newcolumnname] = 'value if the condition is met'

#for interest rates, a new column is needed. rate > 0.12 then high, else low.
LoanData.loc[LoanData['int.rate'] > 0.12, 'int.rate.type'] = 'high'
LoanData.loc[LoanData['int.rate'] <= 0.12, 'int.rate.type'] = 'low'


#------------------------------------
#VISUALIZATION
#Bar charts
#number of loans (rows) by fico category
catplot = LoanData.groupby(['FicoCategory']).size()
catplot.plot.bar(color = 'green', width = 0.8)
plt.show()

purposecount = LoanData.groupby(['purpose']).size()
purposecount.plot.bar()
plt.show()

#Scatter plots
xpoint = LoanData['dti']
ypoint = LoanData['annual_income']

plt.scatter(xpoint, ypoint, color = 'red')
plt.show()

#-----------------
#EXTRACT THE DATA TO csv. FILE
LoanData.to_csv('loandata_cleaned.csv', index = True)
