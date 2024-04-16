import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#a
# Load the data
df = pd.read_csv(r'C:\Users\pgrev\Downloads\diabetes.csv')

np.random.seed(42)
sample_25 = df.sample(25)

if 'Glucose' in df.columns:
    mean_glucose_population = df['Glucose'].mean()
    max_glucose_population = df['Glucose'].max()
    mean_glucose_sample = sample_25['Glucose'].mean()
    max_glucose_sample = sample_25['Glucose'].max()

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.bar(['Population', 'Sample'], [mean_glucose_population, mean_glucose_sample], color=['blue', 'green'])
    plt.ylabel('Mean Glucose')
    plt.title('Mean Glucose Comparison')

    plt.subplot(1, 2, 2)
    plt.bar(['Population', 'Sample'], [max_glucose_population, max_glucose_sample], color=['red', 'purple'])
    plt.ylabel('Max Glucose')
    plt.title('Max Glucose Comparison')

    plt.tight_layout()
    plt.show()
else:
    print("Column 'Glucose' not found in DataFrame.")
#b

percentile_98_population = np.percentile(df['BMI'], 98)
percentile_98_sample = np.percentile(sample_25['BMI'], 98)

plt.figure(figsize=(8, 6))
plt.bar(['Population', 'Sample'], [percentile_98_population, percentile_98_sample], color=['blue', 'green'])
plt.ylabel('98th Percentile of BMI')
plt.title('Comparison of 98th Percentile BMI Between Population and Sample')
plt.ylim(0, max(percentile_98_population, percentile_98_sample) + 5)
plt.show()

#c
bootstrap_means = []
bootstrap_stds = []
bootstrap_percentiles = []

for _ in range(500):
    bootstrap_sample = df.sample(n=150, replace=True)
    bootstrap_means.append(bootstrap_sample['BloodPressure'].mean())
    bootstrap_stds.append(bootstrap_sample['BloodPressure'].std())
    bootstrap_percentiles.append(np.percentile(bootstrap_sample['BloodPressure'], 50))

population_mean = df['BloodPressure'].mean()
population_std = df['BloodPressure'].std()
population_percentile = np.percentile(df['BloodPressure'], 50)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Mean
axes[0].hist(bootstrap_means, bins=30, color='skyblue', alpha=0.7, label='Bootstrap Means')
axes[0].axvline(population_mean, color='red', linestyle='dashed', linewidth=2, label='Population Mean')
axes[0].set_title('Distribution of Bootstrap Means')
axes[0].set_xlabel('Blood Pressure Mean')
axes[0].set_ylabel('Frequency')
axes[0].legend()

# Standard Deviation
axes[1].hist(bootstrap_stds, bins=30, color='lightgreen', alpha=0.7, label='Bootstrap Stds')
axes[1].axvline(population_std, color='red', linestyle='dashed', linewidth=2, label='Population Std Dev')
axes[1].set_title('Distribution of Bootstrap Standard Deviations')
axes[1].set_xlabel('Blood Pressure Std Dev')
axes[1].set_ylabel('Frequency')
axes[1].legend()

# Percentile
axes[2].hist(bootstrap_percentiles, bins=30, color='salmon', alpha=0.7, label='Bootstrap 50th Percentiles')
axes[2].axvline(population_percentile, color='red', linestyle='dashed', linewidth=2, label='Population 50th Percentile')
axes[2].set_title('Distribution of Bootstrap 50th Percentiles')
axes[2].set_xlabel('Blood Pressure 50th Percentile')
axes[2].set_ylabel('Frequency')
axes[2].legend()

plt.tight_layout()
plt.show()