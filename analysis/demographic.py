# # --------------Cleaning----------------
# import csv
# with open('DemographicData.csv', 'r') as file:
#     content = file.read()
# updated_content = content.replace(',', '.').replace(';',',').replace(';;', ' ').replace(';;;', ' ').replace(';;;;', ' ').replace(';;;;;', ' ')

# with open('DemographicData.csv', 'w') as file:
#     file.write(updated_content)

# with open('DemographicData.csv', 'r') as file:
#     content = file.read()
# rows = content.split('\n')

#---------------mean and SD of demographic data ------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the CSV file
df = pd.read_csv('DemographicData.csv')

# List of numeric columns to analyze
numeric_columns = [
    'Age'
]

# Calculate mean and standard deviation for numeric columns
means = df[numeric_columns].mean()
stds = df[numeric_columns].std()

# Print the results
print("Means of numeric columns:")
print(means)
print("\nStandard deviations of numeric columns:")
print(stds)
#------------ploting---------------
# # Set up the matplotlib figure
# plt.figure(figsize=(15, 10))

# # Create histograms for each numeric column
# for i, column in enumerate(numeric_columns):
#     plt.subplot(2, 3, i + 1)
#     sns.histplot(df[column], kde=True)
#     plt.title(f'Histogram of {column.split(" (")[0]}')
#     plt.xlabel(column.split(" (")[0])
#     plt.ylabel('Frequency')

# plt.tight_layout()
# plt.show()

# # Set up the matplotlib figure
# plt.figure(figsize=(15, 10))

# # Create box plots for each numeric column
# for i, column in enumerate(numeric_columns):
#     plt.subplot(2, 3, i + 1)
#     sns.boxplot(data=df, y=column)
#     plt.title(f'Box Plot of {column.split(" (")[0]}')
#     plt.ylabel(column.split(" (")[0])

# plt.tight_layout()
# plt.show()
