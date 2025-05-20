"""
EEG_analysis.py
Performs data cleaning, conversion, and statistical analysis (RM ANOVA) 
on EEG amplitude data for morning vs. evening sessions during a PVT task.
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.anova import AnovaRM

# -------------------------------------------------------------
# STEP 1: TEXT FILE CLEANING & CONVERSION
# -------------------------------------------------------------
"""
Use this section only if starting from raw .txt files. It converts semicolon-delimited EEG export files 
into clean CSVs for further analysis.

# ---- Clean Evening File ----
with open('Area70-130_evening.txt', 'r') as file:
    content = file.read()
updated_content = content.replace(';', ' ').replace('  ', ' ').replace(' ', ',').replace(',', '.').replace(';', ',')
with open('Area70-130_evening.csv', 'w') as file:
    file.write(updated_content)

# ---- Clean Morning File ----
with open('Area70-130_morning.txt', 'r') as file:
    content = file.read()
updated_content2 = content.replace(';', ' ').replace('  ', ' ').replace(' ', ',').replace(',', '.').replace(';', ',')
with open('Area70-130_morning.csv', 'w') as file:
    file.write(updated_content2)
"""

# -------------------------------------------------------------
# STEP 2: Load and Prepare Data
# -------------------------------------------------------------

# Load the CSV files 
morning_data = pd.read_csv('Area70-130_morning.csv')
evening_data = pd.read_csv('Area70-130_evening.csv')

# Define target EEG channels
channels = ['P7-Average', 'P8-Average', 'P3-Average', 'Pz-Average', 'P4-Average', 'Oz-Average']
columns = ['File'] + channels

# Filter only necessary columns
morning_data = morning_data[columns]
evening_data = evening_data[columns]

# Add Condition and Participant IDs
morning_data['Condition'] = 'Morning'
evening_data['Condition'] = 'Evening'
morning_data['Participant'] = range(1, len(morning_data) + 1)
evening_data['Participant'] = range(1, len(evening_data) + 1)

# Merge datasets
data = pd.concat([morning_data, evening_data])

# Ensure numeric data types and drop NaNs
data[channels] = data[channels].apply(pd.to_numeric, errors='coerce')
data = data.dropna(subset=channels)

# Convert to long format for RM ANOVA
long_data = pd.melt(data, 
                    id_vars=['Participant', 'Condition'], 
                    value_vars=channels, 
                    var_name='Channel', 
                    value_name='Amplitude')

# -------------------------------------------------------------
# STEP 3: Repeated Measures ANOVA
# -------------------------------------------------------------

print(" Repeated Measures ANOVA across Condition and Channel:")
rm_model = AnovaRM(long_data, 'Amplitude', 'Participant', within=['Condition', 'Channel']).fit()
print(rm_model.summary())

# -------------------------------------------------------------
# STEP 4: Visualization
# -------------------------------------------------------------

# --- Boxplot by channel and condition ---
plt.figure(figsize=(10, 6))
sns.boxplot(x='Channel', y='Amplitude', hue='Condition', data=long_data)
plt.title('Amplitude by EEG Channel and Condition')
plt.ylabel('Amplitude (µV)')
plt.xlabel('EEG Channel')
plt.tight_layout()
plt.show()

# --- Optional: Channel-wise detailed plots ---
"""
# Point plots for each channel
num_cols = 3
num_rows = (len(channels) + num_cols - 1) // num_cols
plt.figure(figsize=(16, 12))

for i, ch in enumerate(channels, 1):
    plt.subplot(num_rows, num_cols, i)
    sns.pointplot(data=long_data[long_data['Channel'] == ch], 
                  x='Condition', y='Amplitude', ci='sd', capsize=.2)
    plt.title(f'{ch}')
    plt.xlabel('Condition')
    plt.ylabel('Amplitude')
    plt.grid(True)

plt.tight_layout()
plt.suptitle('Mean Amplitude by Condition for Each Channel', y=1.02)
plt.show()
"""
