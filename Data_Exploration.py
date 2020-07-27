# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 13:25:43 2020

@author: user
"""

#importing modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from  sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression 
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.metrics import mean_squared_error as MSE
#importing dataset
df=pd.read_csv('House_price.csv')

# dataset cleaning
df=df.dropna()
df=df.drop([78,99,173])
df.Prices=df.Prices.str.replace(',','')
df.Prices=df.Prices.astype(int)
df.SqFt=df.SqFt.astype(int)
df.Bedrooms=df.Bedrooms.str.replace('Bedrooms','')
df.Bedrooms=df.Bedrooms.str.replace('Bedroom','').astype(int)
new=df.Address.str.split(',',n=2,expand=True)
df['Region']=new[1]
df['Region']=df['Region'].str.replace('Bangalore','')
df=df[['Bedrooms','SqFt','Furnishing','Region','Address','Prices']]
#data Exploration
print(df.info())
print(df.head())
print(df.describe())

#data Visualisation
_=sns.scatterplot(x='SqFt',y='Prices',data=df,hue='Bedrooms')
plt.show()
_=sns.barplot(x='Region',y='Prices',data=df)
plt.show()
_=sns.distplot(df.Prices,bins=20)
plt.show()

#Converting Text to numeical
from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
df['Furn']=le.fit_transform(df.Furnishing)
df['Reg']=le.fit_transform(df.Region)
data=df[['Bedrooms','SqFt','Furn','Reg',]]

#splitting the data
X=np.array(data.iloc[:,:])
y=np.array(df.iloc[:,5]).reshape((-1,1))
scaler=StandardScaler()
X_scaled=scaler.fit_transform(X)
y_scaled=scaler.fit_transform(y)
X_train,X_test,y_train,y_test=train_test_split(X_scaled, y_scaled, random_state=42, test_size=0.3)
lr=LinearRegression()
lr.fit(X_train,y_train)
y_pred=lr.predict(X_test)
importance=lr.coef_
print(importance)
Error=MSE(y_pred,y_test)
err_sqrt=Error**(1/2)
print('The error for Regression is:',err_sqrt)




