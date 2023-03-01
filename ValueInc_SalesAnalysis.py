# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 18:03:45 2023

@author: Mona V.
"""


import pandas as pd

# how to bring a .csv file --> file_name = pd.read_csv('file.csv')
# read_csv is a function inside Pnadas library
data = pd.read_csv('transaction.csv')

#to prepare the .csv file to eliminate ","
data = pd.read_csv('transaction.csv', sep=';') 

#summary of the data
data.info()

#--------------------------
# WORKING WITH CALCULATIONS

#cost purchase transaction column calculation
# variable = dataframe['column_name']
CostPerItem = data['CostPerItem']
PurchasedQty = data['NumberOfItemsPurchased']
CostPerTransaction = CostPerItem * PurchasedQty

#adding a new column to dataframe
data['CostPerTransaction'] = CostPerTransaction
data['SalesPerTransaction'] = data['SellingPricePerItem'] * data['NumberOfItemsPurchased']
data['Profit'] = data['SalesPerTransaction'] - data['CostPerTransaction']
#mark up calculation: (Sales - Cost)/Cost
data['Markup'] = (data['Profit']/data['CostPerTransaction'] * 100) #how much we mark up the price from its cost price?
#to show % in fornt of the Mark u value:
# data['Markup'] = data['Markup'].astype(str) + '%'

data['Markup'] = round(data['Markup'],2)

#---------------------------------
#COMBINING DATA FILEDS
data.info()

#to check columns data type
print(data['Day'].dtype)

#adding column Date to cncat day, month, and year in format like Feb-12-2023
#data['Date'] = data['Day'].astype(str)  + '-' + data['Month'] + '-' + data['Year'].astype(str) #or
day = data['Day'].astype(str) 
year = data['Year'].astype(str)
data['Date'] = day + '-' + data['Month'] + '-' + year

#-----------------------------------
data.head(5) #brings in first 5 rows

#-------------------------------------
#SPLIT FILED
split_col = data['ClientKeywords'].str.split(',', expand = True)

#assign each column from the splited columns to a new column
data['ClientAge'] = split_col[0]
data['Client Type'] = split_col[1]
data['LengthOfContract'] = split_col[2]

#-------------------------------------
#REPLACE FUNCTION
#syntax: new_var = column.str.replace('current value', 'what to be replaced')
data['ClientAge'] = data['ClientAge'].str.replace('[', '')
data['LengthOfContract'] = data['LengthOfContract'].str.replace(']', '')

#----------------------------------------
#USING THE LOWER FUNCTION TO CHANGE ITEM TO LOWERCASE
data['ItemDescription'] = data['ItemDescription'].str.lower()

#------------------------------------------
#HOW TO MERGE FILES

#bringing a new dataset
seasons = pd.read_csv('value_inc_seasons.csv', sep=';')

#merging files syntax:  merge_df = pd.merge(df_old, df_new, on = 'key')
data = pd.merge(data, seasons, on = 'Month')

#------------------------------------
#DROPPING A COLUMN
#syntax: df = df.drop('column_name', axis = 1)   axis1 means to remove column
data = data.drop(columns = 'ClientKeywords', axis = 1)
data = data.drop(columns = ['Day', 'Month', 'Year']) #without axis = 1 is also working

#-------------------------------
#EXPORT TO CSV FILE
#index = False means we don't need to have a seperate column for index - in this example we already have our unique key which is cusotmer id
data.to_csv('ValueInc_Cleaned.csv', index = False)
