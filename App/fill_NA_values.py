import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from sklearn.datasets import load_iris
from sklearn import metrics
import seaborn as sns
import matplotlib.pyplot as plt

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory


data = pd.read_csv("..\\influxdata_2023-10-29T05_35_44Z.csv")

data.head()
data.shape
data.info()
print ("Summation of NAN values :")
data.isnull().sum()
data_knn = data.copy()

data_knn['humidity'].interpolate(method="linear", inplace=True)
data_knn['light_intensity'].interpolate(method="linear", inplace=True)
data_knn['pressure'].interpolate(method="linear", inplace=True)
data_knn['soil_moisture'].interpolate(method="linear", inplace=True)
data_knn['temperature'].interpolate(method="linear", inplace=True)

data_knn.head(100)
data_knn.to_csv('..\\influxdata_filled_NA.csv', index=False)
