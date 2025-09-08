import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load the data from the provided CSV file
try:
    data = pd.read_csv('growth_rate_20220907.csv')
except FileNotFoundError:
    print("Error: 'growth_rate_20220907.csv' not found. Please make sure the file is in the same directory.")
    exit()

data_clean = data.dropna(subset=['doubling_time_hours'])

# --- 1. Bar Plot: Average Doubling Time for Selected Models ---
# This plot compares the average doubling time of different models.
doubling_times = data_clean.groupby('model_name')['doubling_time_hours'].mean().head(10)

plt.figure(figsize=(12, 7))
bars = plt.bar(doubling_times.index, doubling_times.values, color='lightgreen')

plt.title('Average Doubling Time of Cell Models', fontsize=16)
plt.xlabel('Cell Model Name', fontsize=12)
plt.ylabel('Doubling Time (Hours)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adding labels on top of the bars for clarity
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout() # Adjust layout to prevent labels from being cut off
plt.show()


# --- 2. Scatter Plot: Seeding Density vs. Doubling Time ---
# This plot visualizes the relationship between the initial seeding density
plt.figure(figsize=(10, 6))
plt.scatter(data_clean['seeding_density'], data_clean['doubling_time_hours'], color='darkorange', alpha=0.7, edgecolors='k')

plt.title('Seeding Density vs. Doubling Time', fontsize=16)
plt.xlabel('Seeding Density', fontsize=12)
plt.ylabel('Doubling Time (Hours)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()


# --- 3. Histogram: Distribution of Doubling Times ---
# This plot shows the frequency distribution of the doubling times across all models.
plt.figure(figsize=(10, 6))
plt.hist(data_clean['doubling_time_hours'], bins=15, color='royalblue', edgecolor='black', alpha=0.8)

plt.title('Distribution of Cell Doubling Times', fontsize=16)
plt.xlabel('Doubling Time (Hours)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
