"""
Behavioral Analysis – Reaction Times in the PVT
Author: Lala Jafarova
Description: This script analyzes reaction time data from a Psychomotor Vigilance Task (PVT)
administered at two times of day. Includes repeated measures ANOVA, outlier removal, and 
a linear mixed-effects model.
"""

# ----------------------------- #
#  Import Packages
# ----------------------------- #
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.anova import AnovaRM
from statsmodels.formula.api import mixedlm

# ----------------------------- #
#  Load and Prepare Data
# ----------------------------- #
df = pd.read_csv('PVT_Behavioral_Lala.csv')

# Filter for correct responses ( Accuracy == 1)
df = df[df['Accuracy'] == 1]

# Drop rows with missing reaction times
df = df.dropna(subset=['ReactionTime'])

# ----------------------------- #
#  Aggregate Reaction Times
# ----------------------------- #
# Compute mean RT per participant per condition
agg_df = df.groupby(['Participant', 'Time'], as_index=False).agg({'ReactionTime': 'mean'})

# ----------------------------- #
#  Repeated Measures ANOVA
# ----------------------------- #
print("\n Repeated Measures ANOVA:")
aovrm = AnovaRM(agg_df, 'ReactionTime', 'Participant', within=['Time'])
anova_result = aovrm.fit()
print(anova_result)

# ----------------------------- #
#  Boxplot (Raw RTs)
# ----------------------------- #
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='Time', y='ReactionTime')
plt.title('Reaction Times by Time of Day (All Data)')
plt.xlabel('Time of Day')
plt.ylabel('Reaction Time (ms)')
plt.grid(True)
plt.tight_layout()
plt.show()

# ----------------------------- #
#  Outlier Removal Function
# ----------------------------- #
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df[column] >= lower) & (df[column] <= upper)]

# Remove outliers from aggregated data
cleaned_df = remove_outliers(agg_df, 'ReactionTime')

# ----------------------------- #
#  Linear Mixed Effects Model
# ----------------------------- #
print("\n Linear Mixed Effects Model (after outlier removal):")
lme_model = mixedlm("ReactionTime ~ Time", cleaned_df, groups=cleaned_df["Participant"])
lme_result = lme_model.fit()
print(lme_result.summary())

# ----------------------------- #
#  Boxplot (Outliers Removed)
# ----------------------------- #
plt.figure(figsize=(8, 6))
sns.boxplot(data=cleaned_df, x='Time', y='ReactionTime')
plt.title('Reaction Times by Time of Day (Outliers Removed)')
plt.xlabel('Time of Day')
plt.ylabel('Reaction Time (ms)')
plt.grid(True)
plt.tight_layout()
plt.show()
