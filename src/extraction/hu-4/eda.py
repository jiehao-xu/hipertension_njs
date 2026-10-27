import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings as wr
import math
wr.filterwarnings('ignore')

df = pd.read_excel("data/raw/medicamentosHU3.xlsx")
print("="*30)
print(df.head())
print("="*30)
print(df.shape)
print("="*30)
print(df.info())
print("="*30)
print(df.describe().T)
print("="*30)
print(df.columns.tolist())
print("="*30)
print(df.isnull().sum())
print("="*30)
print(df.duplicated().sum())
print("="*30)

sns.set_style("darkgrid")

numerical_columns = df.select_dtypes(include=["int64", "float64"]).columns

n_cols = 4
n_rows = math.ceil(len(numerical_columns) / n_cols)

plt.figure(figsize=(16, n_rows * 3))

for idx, feature in enumerate(numerical_columns, 1):
    plt.subplot(n_rows, n_cols, idx)
    sns.histplot(df[feature], kde=True)
    plt.title(f"{feature} | Skewness: {df[feature].skew():.2f}")

plt.tight_layout()
plt.subplots_adjust(hspace=0.5)
plt.show()