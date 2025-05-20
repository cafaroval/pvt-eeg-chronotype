# ###Cleaning evening text file and converting into csv
# import csv
# with open('Area70-130_evening.txt', 'r') as file:
#     content = file.read()
# updated_content = content.replace(';', ' ').replace(';;', ' ').replace(';;;', ' ').replace(';;;;', ' ').replace(';;;;;', ' ').replace('  ', ' ').replace(' ', ';').replace(',', '.').replace(';',',')

# with open('Area70-130_evening.txt', 'w') as file:
#     file.write(updated_content)

# with open('Area70-130_evening.txt', 'r') as file:
#     content = file.read()
# rows = content.split('\n')

# # Define the filename for the CSV file
# csv_filename = 'Area70-130_evening.csv'

# with open(csv_filename, 'w', newline='') as csvfile:
#     csv_writer = csv.writer(csvfile)
    
#     for row in rows:
#         cells = row.split(',')
#         csv_writer.writerow(cells)

# ###cleaning the morning text file and converting into csv
# with open('Area70-130_morning.txt', 'r') as file:
#     content = file.read()
# updated_content2 = content.replace(';', ' ').replace(';;', ';').replace(';;;', ' ').replace(';;;;', ' ').replace(';;;;;', ' ').replace(';;;;;;', ' ').replace(';;;;;;;', ' ').replace('  ', ' ').replace(' ', ';').replace(',', '.').replace(';',',')

# with open('Area70-130_morning.txt', 'w') as file:
#     file.write(updated_content2)

# with open('Area70-130_morning.txt', 'r') as file:
#     content = file.read()
# rows = content.split('\n')

# # Define the filename for the CSV file
# csv_filename2 = 'Area70-130_morning.csv'

# with open(csv_filename2, 'w', newline='') as csvfile:
#     csv_writer = csv.writer(csvfile)
    
#     for row in rows:
#         cells = row.split(',')
#         csv_writer.writerow(cells)

#-------RM ANOVA-----------------------------------------------------------------------------------------------------
import pandas as pd
from statsmodels.stats.anova import AnovaRM
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV files
morning_data = pd.read_csv('Area70-130_morning.csv', delimiter=',', decimal='.', skipinitialspace=True)
evening_data = pd.read_csv('Area70-130_evening.csv', delimiter=',', decimal='.', skipinitialspace=True)

# Select the relevant columns for analysis
columns_of_interest = ['File', 'P7-Average', 'P8-Average', 'P3-Average', 'Pz-Average', 'P4-Average', 'Oz-Average']
filtered_morning_data = morning_data[columns_of_interest]
filtered_evening_data = evening_data[columns_of_interest]

# Add a 'Condition' column to each DataFrame
filtered_morning_data['Condition'] = 'Morning'
filtered_evening_data['Condition'] = 'Evening'

# Add a 'Participant' column
filtered_morning_data['Participant'] = range(1, len(filtered_morning_data) + 1)
filtered_evening_data['Participant'] = range(1, len(filtered_evening_data) + 1)

# Concatenate the data
combined_data = pd.concat([filtered_morning_data, filtered_evening_data])

# Ensure all amplitude columns are numeric, coerce errors to NaN
amplitude_columns = ['P7-Average', 'P8-Average', 'P3-Average', 'Pz-Average', 'P4-Average', 'Oz-Average']
combined_data[amplitude_columns] = combined_data[amplitude_columns].apply(pd.to_numeric, errors='coerce')

# Drop rows with any NaN values in the amplitude columns
combined_data = combined_data.dropna(subset=amplitude_columns)

# Melt the DataFrame to long format, excluding the 'File' column
long_data = pd.melt(combined_data, id_vars=['Participant', 'Condition'], 
                    value_vars=amplitude_columns, var_name='Channel', value_name='Amplitude')


# Perform repeated measures ANOVA considering both 'Condition' and 'Channel'
model = AnovaRM(long_data, 'Amplitude', 'Participant', within=['Condition', 'Channel']).fit()

print("General ANOVA results:")
print(model.summary())

# Plot the data
plt.figure(figsize=(10, 6))
sns.boxplot(x='Channel', y='Amplitude', hue='Condition', data=long_data)
plt.title('Amplitude by Channel and Condition')
plt.show()

# # Perform repeated measures ANOVA for each channel
# anova_results = {}
# for channel in amplitude_columns:
#     channel_data = long_data[long_data['Channel'] == channel]
#     try:
#         model = AnovaRM(channel_data, 'Amplitude', 'Participant', within=['Condition']).fit()
#         anova_results[channel] = model
#         print(f"ANOVA results for {channel}:")
#         print(model.summary())
#     except Exception as e:
#         print(f"Error analyzing {channel}: {e}")
#---------Ploting-----------------------------------------------------------------------------
# Combined boxplot for all channels
# plt.figure(figsize=(16, 12))
# sns.set(style="whitegrid")

# num_channels = len(amplitude_columns)
# num_cols = 3
# num_rows = (num_channels + num_cols - 1) // num_cols  # Calculate number of rows needed

# for i, channel in enumerate(amplitude_columns, 1):
#     plt.subplot(num_rows, num_cols, i)
#     sns.boxplot(data=long_data[long_data['Channel'] == channel], x='Condition', y='Amplitude')
#     plt.title(f'{channel}')
#     plt.xlabel('Condition')
#     plt.ylabel('Amplitude')
#     plt.grid(True)

# plt.tight_layout()
# plt.suptitle('Amplitude Distribution by Condition for Each Channel', y=1.02)
# plt.show()

# # Combined line plot with error bars (mean and confidence intervals) for all channels
# plt.figure(figsize=(16, 12))

# for i, channel in enumerate(amplitude_columns, 1):
#     plt.subplot(num_rows, num_cols, i)
#     sns.pointplot(data=long_data[long_data['Channel'] == channel], x='Condition', y='Amplitude', ci='sd', capsize=.2)
#     plt.title(f'{channel}')
#     plt.xlabel('Condition')
#     plt.ylabel('Amplitude')
#     plt.grid(True)

# plt.tight_layout()
# plt.suptitle('Mean Amplitude with CI by Condition for Each Channel', y=1.02)
# plt.show()