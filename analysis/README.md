# 📈 EEG & Behavioral Data Analysis Scripts

This folder contains Python scripts used to analyze EEG and behavioral data collected during my lab rotation project on chronotype and cognitive control using the Psychomotor Vigilance Task (PVT).

## 📄 Script Descriptions

- `EEG_analysis.py`  
  Preprocesses EEG-derived measures and performs repeated measures ANOVA to assess differences in P1 amplitude across sessions and channels.

- `behavioral_analysis.py`  
  Analyzes reaction time data from the PVT task, including summary statistics, outlier removal, boxplots, and linear mixed-effects modeling.

- `demographic.py`  
  Summarizes participant demographics (e.g., age) and visualizes distributions using histograms and boxplots.

## 🛠 Tools & Libraries

- `pandas`, `numpy` for data manipulation  
- `matplotlib`, `seaborn` for visualization  
- `statsmodels` for statistical modeling (ANOVA, linear mixed models)  
- `csv` for initial data cleaning steps

## 💡 Notes

These scripts reflect a complete analysis pipeline for cognitive neuroscience research — from raw behavioral/EEG data to statistical testing and visualization. While no statistically significant findings were observed, the code demonstrates reproducible and methodologically sound research practices.

