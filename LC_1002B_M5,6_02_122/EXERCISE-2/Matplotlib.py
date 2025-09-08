import pandas as pd
import matplotlib.pyplot as plt

def visualize_data(filepath):

    try:
        # Load the dataset
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return

    # --- Line Plot: Average Ejection Fraction over Time ---
    # The 'time' variable indicates follow-up duration. Let's see how the average
    # ejection fraction changes over this time.
    avg_ejection_by_time = df.groupby('time')['ejection_fraction'].mean()

    plt.figure(figsize=(10, 6))
    plt.plot(avg_ejection_by_time.index, avg_ejection_by_time.values, color='skyblue', marker='o')
    plt.title('Average Ejection Fraction Over Follow-up Time')
    plt.xlabel('Follow-up Time (days)')
    plt.ylabel('Average Ejection Fraction (%)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

    # --- Bar Plot: Death Events by Sex ---
    # This plot compares the number of death events between male and female patients.
    # 0 = Female, 1 = Male
    df['sex_label'] = df['sex'].map({0: 'Female', 1: 'Male'})
    death_events_by_sex = df.groupby('sex_label')['DEATH_EVENT'].sum()

    plt.figure(figsize=(8, 6))
    death_events_by_sex.plot(kind='bar', color=['lightcoral', 'teal'])
    plt.title('Number of Death Events by Sex')
    plt.xlabel('Sex')
    plt.ylabel('Number of Death Events')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

    # --- Scatter Plot: Serum Creatinine vs. Ejection Fraction ---
    # This plot visualizes the relationship between these two continuous variables.

    plt.figure(figsize=(10, 6))

    df_alive = df[df['DEATH_EVENT'] == 0]
    df_dead = df[df['DEATH_EVENT'] == 1]

    plt.scatter(
        df_alive['serum_creatinine'],
        df_alive['ejection_fraction'],
        alpha=0.6,
        color='mediumseagreen',
        label='No Death Event'
    )
    plt.scatter(
        df_dead['serum_creatinine'],
        df_dead['ejection_fraction'],
        alpha=0.8,
        color='firebrick',
        label='Death Event'
    )

    plt.title('Serum Creatinine vs. Ejection Fraction')
    plt.xlabel('Serum Creatinine (mg/dL)')
    plt.ylabel('Ejection Fraction (%)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


# Run the visualization function with the provided dataset filename
if __name__ == '__main__':
    visualize_data('heart_failure_clinical_records_dataset.csv')
