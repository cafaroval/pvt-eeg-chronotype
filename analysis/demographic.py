"""
Demographic Data Summary – PVT EEG Study
Author: Lala Jafarova
Description: Calculates summary statistics for participant age and visualizes the distribution 
using histograms and boxplots. Includes optional file cleaning step.
"""

# ----------------------------- #
#  Import Packages
# ----------------------------- #
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------- #
# File Cleaning (if using raw .csv exports)
# ----------------------------- #
"""

import csv
with open('DemographicData.csv', 'r') as file:
    content = file.read()

updated_content = content.replace(',', '.').replace(';',',').replace(';;', ' ').replace(';;;', ' ').replace(';;;;', ' ').replace(';;;;;', ' ')

with open('DemographicData.csv', 'w') as file:
    file.write(updated_content)
"""

# ----------------------------- #
# Load Cleaned Data
# ----------------------------- #
df = pd.read_csv('DemographicData.csv')

# ----------------------------- #
#  Basic Stats
# ----------------------------- #
numeric_columns = ['Age']

# Calculate mean and standard deviation
means = df[numeric_columns].mean()
stds = df[numeric_columns].std()

print(" Means of numeric columns:")
print(means)

print("\n📉 Standard deviations of numeric columns:")
print(stds)

# ----------------------------- #
#  Visualization – Histograms
# ----------------------------- #
plt.figure(figsize=(8, 4))
for i, column in enumerate(numeric_columns):
    plt.subplot(1, len(numeric_columns), i + 1)
    sns.histplot(df[column], kde=True)
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# ----------------------------- #
#  Visualization – Boxplots
# ----------------------------- #
plt.figure(figsize=(8, 4))
for i, column in enumerate(numeric_columns):
    plt.subplot(1, len(numeric_columns), i + 1)
    sns.boxplot(data=df, y=column)
    plt.title(f'Boxplot of {column}')
    plt.ylabel(column)
plt.tight_layout()
plt.show()
