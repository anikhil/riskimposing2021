# -*- coding: utf-8 -*-
"""DELHI junee 2006-09 anjtry.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15nV65qT81YVIeQ77CfXm_RGstKKJ2Lrr
"""

from IPython.display import display
import pandas as pd

# Displaying data in sumarized way
def display_data(dataframe):
    display(dataframe.head())
    print('...')
    display(dataframe.tail())
    print("DataFrame shape: {}".format(dataframe.shape))

# Loading data from Excel file
# df = pd.read_excel('A2TierDelhi.xlsx')
# df = pd.read_excel('delhi2013.xlsx')
# df = pd.read_excel('JunDelhi2008.xlsx')
# df = pd.read_excel('JuneDelhi2k0809.xlsx')
# df = pd.read_excel('Delhidot5yr.xlsx')

#df = pd.read_excel('modcld2006to2009sep15.xlsx')

df = pd.read_excel('2006 to 2009-Data.xlsx')

#df = pd.read_excel('modcld20142016sep15.xlsx')

display(df.describe(include='all'))

# Printing Unique values in Time, Date, Day and H&R Status
print('Before:', df['Day'].unique())



# Printing Unique values in Time, Date, Day and H&R Status
print('Before:', df['Victim'].unique())

#print
print('Before:', df['Accused'].unique())

# Replacing 9 in Day and Vacation because are in the same row with Unknown in Accused
df.loc[df.Day == 9, 'Day'] = df['Day'].mode()[0]
df.loc[df.Vacation == 9, 'Vacation'] = df['Vacation'].mode()[0]

# Fill nan values with the mode
df['Time'] = df['Time'].fillna(df['Time'].mode()[0])
df['Date'] = df['Date'].fillna(df['Date'].mode()[0])
df['Day'] = df['Day'].fillna(df['Day'].mode()[0])                                
df['Timeofday'] = df['Timeofday'].fillna(df['Timeofday'].mode()[0])  
df['H&R Status'] = df['H&R Status'].fillna(df['H&R Status'].mode()[0])

# Printing Unique values in Day
print('After:', df['Day'].unique())

#Displaying columns Tier and Severity values
print('Tier:', df['Tier'].unique())
print('Severity:', df['Severity'].unique())

# Display Severity Injury and Type of Road
display(df.loc[df['Severity'] == 'Day'])

# Given that Injury is just in Category 2 with Unknown value, we drop columns
## Continue with TiERor type of road
df = df.drop(['Tier','Severity'], axis=1)

# Displaying category columns 
print('Victim:', df['Victim'].unique())

print('Accused:', df['Accused'].unique())

#print('\nType of Road:', df['Type of Road'].unique())   ----------------------------------------Type of Road into Char
#print('\nType of Road:', df['Type of Road'].unique())
print('\nCategory 2:', df['Accused'].unique())
#print('test')
print('\nCategory 1:', df['Victim'].unique())



# Displaying category columns 
print('\nCategory 1:', df['Victim'].unique())

display_data(df)

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

display(sns.pairplot(df[['Day','Time','Timeofday','Vacation','H&R Status','Totalvehicle']],hue='H&R Status'))


#display(sns.pairplot(df[['Day','H&R Status','Victim', 'Accused']],hue='H&R Status'))
#display(sns.pairplot(df[[Death', 'Injury', 'Total vehicle', 'Collision Type', 'Collision Spot','H&R Status']],hue = 'Death'))

display(sns.pairplot(df[['Day','Time','Timeofday','Vacation','H&R Status','Totalvehicle']],hue='Timeofday'))
#display(sns.pairplot(df[['Day','Time','Vacation','H&R Status','Total vehicle']],hue='Time'))
#display(sns.pairplot(df[['Day','H&R Status','Victim', 'Accused']]))#,hue='H&R Status'))

#category_label = ['Day', 'Vacation', 'H&R Status', 'Death', 'Injury', 'Total vehicle', 'Collision Type', 'Collision Spot', 'Type of Road', 'Divider', 'Catogory1', 'Catogory2']
category_label = ['Time','Date','Day','Timeofday','Vacation', 'H&R Status', 'Totalvehicle', 'Victim', 'Accused'] 
fig, axes = plt.subplots(5, 2, figsize=(16,12))

for ax, x in zip(axes.reshape(-1), category_label):
    sns.countplot(x=x, data=df, ax=ax)

fig.tight_layout()

plt.xlabel('Victim', fontsize='large')
plt.ylabel('Accused', fontsize='large');
#plt.scatter(xlabel,ylabel)

plt.scatter(x,y)
plt.show()

from patsy import dmatrices

#formula = 'Accused ~ C(Day) + C(Vacation) + C(Q("H&R Status")) + Death + Injury + Q("Total vehicle") + C(Q("Collision Type")) + C(Q("Collision Spot")) + C(Q("Type of Road")) + C(Divider) + C(Victim)'

#formula = '''Accused ~ C(Day) + C(Vacation) + C(Q("H&R Status")) + Death + Injury + Q("Total vehicle") +  ==================Updated Below
#                        C(Q("Collision Type")) + C(Q("Collision Spot")) + C(Divider) + C(Victim)'''

# 8 June formula = '''Accused ~ C(Day) + C(Vacation) + C(Q("H&R Status")) +  Q("Total vehicle") + C(Divider) + C(Victim)'''
formula = '''Accused ~ C(Day) +C(Date)+ +C(Time) + C(Timeofday) + C(Vacation) + C(Q("H&R Status")) +  Q("Totalvehicle") + C(Victim)'''

# Preparing data for ML classifiers
_, X = dmatrices(formula, df, return_type='dataframe')
y = df['Accused']

display_data(X)

display_data(y)

# Dividing Unknown data
unk_data = X.loc[df['Accused'] == 'unknown']
unk_label = y.loc[df['Accused'] == 'unknown']
data = X.loc[df['Accused'] != 'unknown']
label = y.loc[df['Accused'] != 'unknown']

#data = df.loc[df['Accused'] != 'Unknown']

#Display Unknown Data
display_data(unk_data.head())
display_data(unk_label)

#Display KNown Data
display(data.head())
display(label.head())

# scikit-learn k-fold cross-validation
from sklearn.model_selection import KFold

from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import StratifiedKFold

import numpy as np
from collections import defaultdict

#names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", #"Gaussian Process", "Decision Tree", "Random Forest", "Neural Net", "AdaBoost","Naive Bayes","LR","LDA","CART"]

names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", #"Gaussian Process",
         "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
         "Naive Bayes","LR","LDA","CART"]

classifiers = [
    KNeighborsClassifier(45),
    SVC(kernel="linear", gamma='auto'),
    SVC(kernel="rbf", gamma='auto'),
    #GaussianProcessClassifier(1.0 * RBF(1.0)),
    DecisionTreeClassifier(),
    RandomForestClassifier(n_estimators=1000),
    MLPClassifier(alpha=1),
    AdaBoostClassifier(),
    GaussianNB(),
    LogisticRegression(),
    LinearDiscriminantAnalysis(),
    GradientBoostingClassifier()]



accuracies = defaultdict(list)

str_fold = StratifiedKFold(n_splits=10, shuffle=True)

#Xt=data.iloc[train]
#Yt=label.iloc[train]
#for train, dev in kfold.split(data):
for train, dev in str_fold.split(data, label, groups=None):
  
    # Training data
    Xt = data.iloc[train]
    Yt = label.iloc[train]
    # Development data
    Xd = data.iloc[dev]
    Yd = label.iloc[dev]
    
    print('Training...')

for name, clf in zip(names, classifiers):
        # Training
        clf.fit(Xt, Yt)
        # Predict
        Yp = clf.predict(Xd)
        accuracy = accuracy_score(Yd, Yp) * 100
        accuracies[name].append(accuracy)
        #print('Accuracy for {}: {}'.format(name, accuracy)) 

'''
str_fold = StratifiedKFold(n_splits=10, shuffle=False, random_state=None)

Xt=data.iloc[train]
Yt=label.iloc[train] 

for train, dev in str_fold.split(Xt, Yt):
    # Training data
    Xt = data.iloc[train]
    Yt = label.iloc[train]
    # Development data
    Xd = data.iloc[dev]
    Yd = label.iloc[dev]
    
    print('Training...')

    for name, clf in zip(names, classifiers):
        # Training
        clf.fit(Xt, Yt)
        # Predict
        Yp = clf.predict(Xd)
        accuracy = accuracy_score(Yd, Yp) * 100
        accuracies[name].append(accuracy)

'''
'''
# Done on 27 June to test STratified KFold
# Prepare cross validation
kfold = KFold(5, True)
for train, dev in kfold.split(data):
    # Training data
    Xt = data.iloc[train]
    Yt = label.iloc[train]
    # Development data
    Xd = data.iloc[dev] 
    Yd = label.iloc[dev]
    
    print('Training...')

for name, clf in zip(names, classifiers):
        # Training
        clf.fit(Xt, Yt)
        # Predict
        Yp = clf.predict(Xd)
        accuracy = accuracy_score(Yd, Yp) * 100
        accuracies[name].append(accuracy)
        #print('Accuracy for {}: {}'.format(name, accuracy))

'''

'''
    for name, clf in zip(names, classifiers):
        # Training
        clf.fit(Xt, Yt)
        # Predict
        Yp = clf.predict(Xd)
        accuracy = accuracy_score(Yd, Yp) * 100
        accuracies[name].append(accuracy)
        #print('Accuracy for {}: {}'.format(name, accuracy)) 

        '''



# Chosing best model
max_model = ''
max_value = 0
for key, value in accuracies.items():
    print('{}: {}'.format(key, sum(value) / len(value)))
    if sum(value) / len(value) > max_value:
        max_value = sum(value) / len(value)
        max_model = key
        
print('\nOur max accuracy was obtained by {}: {}'.format(max_model, max_value))

for name, clf in zip(names, classifiers):
    clf.fit(data, label)
    
u_data = unk_data[['Severity']].copy()
display(u_data)
for name, clf in zip(names, classifiers):
    pred = clf.predict(unk_data)
    u_data[name] = pred
   # unk_data[name] = pred
# Displaying new labels with models
display(unk_data)

# Re-Loading data from Excel file
df = pd.read_excel('27 JUNE - 15 June 8June-jan2020cld2006to2009sep15.xlsx')

known_data = df.loc[df['Accused'] != 'Unknown'].copy()
unknown_data = df.loc[df['Accused'] == 'Unknown'].copy()

# Replacing Unknown values
unknown_data.drop(['Accused'], axis=1, inplace=True)
unknown_data['Accused'] = u_data[max_model]

new_df = pd.concat([known_data, unknown_data])
new_df.sort_index(inplace=True)

print('Before...')
display(df.groupby('Accused').count())
print('After... {}'.format(max_model))
display(new_df.groupby('Accused').count())

# Exporting to Excel
new_df.to_excel("output-nbkdev-2006o2009.xlsx", index=False)