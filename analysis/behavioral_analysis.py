import pandas as pd
from statsmodels.stats.anova import AnovaRM
from statsmodels.formula.api import mixedlm
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv('PVT_Behavioral_Lala.csv')

# Preprocess the data
# Filter for correct responses if 'Accuracy' column is present and correct responses are marked as 1
df = data[data['Accuracy'] == 1]

# Check for missing values and handle them (if any)
df = df.dropna(subset=['ReactionTime'])

# Aggregate data: compute the mean reaction time for each participant at each time of day
agg_df = df.groupby(['Participant', 'Time'], as_index=False).agg({'ReactionTime': 'mean'})

# Perform repeated measures ANOVA
aovrm = AnovaRM(agg_df, 'ReactionTime', 'Participant', within=['Time'])
res = aovrm.fit()
print(res)

#-----Plotting with and without Outliers---------------------
#Plotting boxplot of reaction times by time of day

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='Time', y='ReactionTime')
plt.xlabel('Time of Day')
plt.ylabel('Reaction Time')
plt.title('Distribution of Reaction Times by Time of Day')
plt.grid(True)
plt.show()

# Identifying and removing outliers
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Removing outliers from the aggregated data
cleaned_agg_df = remove_outliers(agg_df, 'ReactionTime')

# Linear Mixed-Effects Model
model = mixedlm("ReactionTime ~ Time", cleaned_agg_df, groups=cleaned_agg_df["Participant"])
result = model.fit()
print(result.summary())

# Plotting boxplot of reaction times by time of day after removing outliers
plt.figure(figsize=(10, 6))
sns.boxplot(data=cleaned_agg_df, x='Time', y='ReactionTime')
plt.xlabel('Time of Day')
plt.ylabel('Reaction Time')
plt.title('Distribution of Reaction Times by Time of Day (Outliers Removed)')
plt.grid(True)
plt.show()
