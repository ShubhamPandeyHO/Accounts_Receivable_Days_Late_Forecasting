# -*- coding: utf-8 -*-
"""Accounts Receivable Days-Late Forecasting.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16tewhVpMSAodorj8s4nxosg7mvF0hg2w
"""



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import explained_variance_score
import warnings
warnings.filterwarnings("ignore")

df=pd.read_csv('/content/WA_Fn-UseC_-Accounts-Receivable.csv')

df.head()

df.shape

df.info()

sns.heatmap(df.isnull(),cmap='Blues')

df.isnull().sum()

df.describe().T

df.head()

#split year from Duedate
df['year']=pd.to_datetime(df['DueDate']).dt.year

# Assign countryCode with country name
df['countryName'] = df['countryCode'].replace({ 391:'Germany',406:'Australia',818:'California, US',897:'Kansas, US',770:'Georgia, US' })
df.drop('countryCode',axis = 1,inplace = True)

country_frame = pd.DataFrame({'Germany':[391],'Australia':[406], 'California, US':[818],'Kansas, US ':[897], 'Georgia, US':[770] })
country_frame

#Store Year 2012
year_2012=df[df['year']==2012]
year_2012.head()

#Store Year 2013
year_2013=df[df['year']==2013]
year_2013.head()

#Store Year 2014
year_2014=df[df['year']==2014]
year_2014.head()

sns.barplot(x=[2012, 2013, 2014], y=[year_2012['DaysLate'].sum(), year_2013['DaysLate'].sum(), year_2014['DaysLate'].sum()], palette=['red', 'green', 'blue'])

"""The significant increase in late payments during the years 2012 and 2013, followed by a sharp decline in 2014, indicates potential improvements in business processes, client engagement, economic conditions, and operational efficiencies. Further qualitative analysis and stakeholder consultations would be beneficial to gain deeper insights into the factors driving these trends and to establish effective strategies for maintaining timely payment patterns in the future."""

df.head()

df['countryName'].value_counts()

Germany=df[df['countryName']=='Germany']
Australia=df[df['countryName']=='Australia']
Georgia=df[df['countryName']=='Georgia, US']
Kansas=df[df['countryName']=='Kansas, US']
California=df[df['countryName']=='California, US']

sns.barplot(x=['Germany', 'Australia', 'Georgia','Kansas','California'], y=[Germany['DaysLate'].sum(), Australia['DaysLate'].sum(), Georgia['DaysLate'].sum(),Kansas['DaysLate'].sum()
,California['DaysLate'].sum()],palette=['red', 'green', 'blue','purple','orange'])

keys = list(dict(year_2012.groupby(['countryName']).sum()['DaysLate']).keys())
items = list(dict(year_2012.groupby(['countryName']).sum()['DaysLate']).values())


plt.figure(figsize = (14,6))
sns.set_style('whitegrid')

sns.barplot(x=items, y=keys, palette=['red', 'green', 'blue','purple','orange'], saturation=.5)
plt.title('Countries that are late in paying invoices for 2012', fontsize = 16)
plt.xlabel('Total Number of Days')
plt.ylabel('CountryName')
plt.show()

keys = list(dict(year_2013.groupby(['countryName']).sum()['DaysLate']).keys())
items = list(dict(year_2013.groupby(['countryName']).sum()['DaysLate']).values())

plt.figure(figsize = (14,6))
sns.set_style('whitegrid')

sns.barplot(x=items, y=keys, palette=['red', 'green', 'blue','purple','orange'], saturation=.5)
plt.title('Countries that are late in paying invoices for 2013', fontsize = 16)
plt.xlabel('Total Number of Days')
plt.ylabel('CountryName')
plt.show()

keys = list(dict(year_2014.groupby(['countryName']).sum()['DaysLate']).keys())
items = list(dict(year_2014.groupby(['countryName']).sum()['DaysLate']).values())

plt.figure(figsize = (14,6))
sns.set_style('whitegrid')

sns.barplot(x=items, y=keys,palette=['red', 'green', 'blue','purple','orange'], saturation=.5)
plt.title('Countries that are late in paying invoices for 2014', fontsize = 16)
plt.xlabel('Total Number of Days')
plt.ylabel('CountryName')
plt.show()

# Scatter plot of InvoiceAmount vs. DaysToSettle
sns.scatterplot(x='InvoiceAmount', y='DaysToSettle', data=df, hue='Disputed', palette='Set2')
plt.title('InvoiceAmount vs. DaysToSettle')
plt.show()

# Histogram of DaysLate
sns.histplot(df['DaysLate'], kde=True, color='skyblue')
plt.title('Histogram of DaysLate')
plt.show()

df.head(1)

groups = [df[df['DaysToSettle'] < 30]['InvoiceAmount'].sum(),
          df[(df['DaysToSettle'] > 30) & (df['DaysToSettle'] < 60)]['InvoiceAmount'].sum(),
          df[(df['DaysToSettle'] > 60) & (df['DaysToSettle'] < 90)]['InvoiceAmount'].sum(),
          df[df['DaysToSettle'] == 90]['InvoiceAmount'].sum()]

categories = ['0-30', '31-60', '61-90', '90']

plt.figure(figsize=(14, 6))
plt.bar(categories, groups, color='skyblue')
plt.title('Time Bucket Size', fontsize=16)
plt.xlabel('Categories')
plt.ylabel('Collected Invoices')
plt.show()

"""Most of the payments are collected within a month and the maximum often 60 days"""

on_time = df[df['DaysLate'] == 0]['customerID'].count()
late = df[df['DaysLate'] != 0 ]['customerID'].count()
labels = ['On Time', 'Late']

plt.figure(figsize = (16,6))
colors = sns.color_palette('Blues')
pie = plt.pie([on_time, late], labels = labels, autopct = '%0.0f%%',colors = colors)

"""# Feature Engineering"""

#Split data , Year and month

df['PaperlessDate'] = pd.to_datetime(df['PaperlessDate'])
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['DueDate'] = pd.to_datetime(df['DueDate'])
df['SettledDate'] = pd.to_datetime(df['SettledDate'])

date_columns = ['PaperlessDate','InvoiceDate','DueDate','SettledDate']

df['PaperlessDate_year'] = df['PaperlessDate'].dt.year
df['PaperlessDate_day'] = df['PaperlessDate'].dt.day
df['PaperlessDate_month'] = df['PaperlessDate'].dt.month

df['InvoiceDate_year'] = df['InvoiceDate'].dt.year
df['InvoiceDate_month'] = df['InvoiceDate'].dt.month
df['InvoiceDate_day'] = df['InvoiceDate'].dt.day

df['DueDate_year'] = df['DueDate'].dt.year
df['DueDate_month'] = df['DueDate'].dt.month
df['DueDate_day'] = df['DueDate'].dt.day

df['SettledDate_year'] = df['SettledDate'].dt.year
df['SettledDate_month'] = df['SettledDate'].dt.month
df['SettledDate_day'] = df['SettledDate'].dt.day

df.drop(['customerID','invoiceNumber','SettledDate','InvoiceDate','PaperlessDate','DueDate'], axis = 1, inplace = True)

category = ['countryName']
encoded_categ = pd.get_dummies(df[category] ,drop_first=True)

df['Disputed'] = df['Disputed'].replace({'Yes':1, 'No':0})
df['PaperlessBill'] = df['PaperlessBill'].replace({'Electronic':1, 'Paper':0})
df = pd.concat([df, encoded_categ], axis = 1)
df = df.drop(columns = category, axis = 1)

df.head()

df.info()

"""#Checking Correlation"""

df.head(1)

corr=df.corr()

sns.heatmap(corr,annot=True,cmap = 'icefire')

"""# Split Dataset for Training and Testing"""

X=df.drop(['DaysLate'],axis=1)
y=df['DaysLate']

X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle = True, test_size = .2, random_state = 44)

scaler=MinMaxScaler()
scaler_x=scaler.fit_transform(X)

"""#Modelling"""

lr = LinearRegression()
dt = DecisionTreeRegressor()
rf = RandomForestRegressor()
knn = KNeighborsRegressor()
gbc = GradientBoostingRegressor()
gnb = GaussianNB()
abc = AdaBoostRegressor()

for model in [lr,dt,rf,knn,gbc,gnb,abc]:
    print('**********\t',model)
    fit=model.fit(X_train,y_train)
    Y_pred_train=fit.predict(X_train)
    Y_pred_test=fit.predict(X_test)
    mse_train = mean_squared_error(y_train, Y_pred_train)
    mse_test = mean_squared_error(y_test, Y_pred_test)
    r2_train = r2_score(y_train, Y_pred_train)
    r2_test = r2_score(y_test, Y_pred_test)
    explained_variance = explained_variance_score(y_test, Y_pred_test)


    print("Training Mean Squared Error\t:", mse_train)

    print("Test Mean Squared Error\t:", mse_test)


    print("Training R2 Score\t:", r2_train)

    print("Test R2 Score\t:", r2_test)

import matplotlib.pyplot as plt

models = ['Linear Regression', 'Decision Tree', 'Random Forest', 'K-Nearest Neighbors', 'Gradient Boosting', 'GaussianNB', 'AdaBoost']

training_mse = [11.751606935577392, 0.0, 0.007673123732251531, 1.6606693711967546, 1.5914337176095643e-07, 0.004563894523326572, 0.2648658964424423]
test_mse = [12.926433035955071, 0.004048582995951417, 0.005452834008097162, 2.333846153846154, 0.004956132514053453, 16.31983805668016, 0.30789075091803697]
training_r2 = [0.6995156837576444, 1.0, 0.9998038010162552, 0.957537288028417, 0.9999999959307618, 0.9998833028765545, 0.9932274753380768]
test_r2 = [0.6872246050430189, 0.9999020381614903, 0.9998680600978032, 0.943528918572692, 0.9998800785723153, 0.6051158289673555, 0.9925500986270436]

plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(models, training_mse, marker='o', label='Training MSE')
plt.plot(models, test_mse, marker='o', label='Test MSE')
plt.title('Mean Squared Error Comparison')
plt.xlabel('Regression Models')
plt.ylabel('Mean Squared Error')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(models, training_r2, marker='o', label='Training R2 Score')
plt.plot(models, test_r2, marker='o', label='Test R2 Score')
plt.title('R2 Score Comparison')
plt.xlabel('Regression Models')
plt.ylabel('R2 Score')
plt.legend()

plt.tight_layout()
plt.show()

"""#Conclusion
From the visualization of the various regression models, it is evident that certain models perform exceptionally well in both the training and testing phases. The Decision Tree, Random Forest, and Gradient Boosting models showcase notably low mean squared error and high R2 scores in both training and testing, indicating robust predictive capabilities and generalization to unseen data. Conversely, the K-Nearest Neighbors model demonstrates relatively higher errors, suggesting a need for further optimization or potentially reconsidering its use in the context of this data. GaussianNB and AdaBoost models also perform relatively well but exhibit slightly higher errors compared to the top-performing models. The Linear Regression model displays moderate performance, with a similar pattern of higher errors compared to the top-performing models.

In summary, for this specific dataset, Decision Tree, Random Forest, and Gradient Boosting models are the most suitable options due to their strong predictive power and generalization ability, making them prime candidates for future use in similar regression tasks. Further fine-tuning and exploration can potentially enhance the performance of the other models as well.
"""