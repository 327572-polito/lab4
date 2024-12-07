import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import t
import numpy as np

# Define the dataset
data = pd.DataFrame({
    'Congestion_Control': ['bic', 'bic', 'bic', 'cubic', 'cubic', 'cubic', 'reno', 'reno', 'reno', 'vegas', 'vegas', 'vegas'],
    'Loss(%)': [1, 3, 5, 1, 3, 5, 1, 3, 5, 1, 3, 5],
    'Average_Goodput(Mbps)': [93.00, 92.70, 87.15, 92.85, 63.80, 24.05, 92.95, 87.95, 67.85, 85.35, 59.95, 38.68],
    'Std_Dev(Mbps)': [0.00, 0.71, 4.17, 0.48, 5.90, 5.69, 0.22, 2.85, 3.72, 1.24, 4.88, 3.61]
})

# Number of runs (samples per condition)
n_runs = 20

# Calculate 95% confidence intervals
confidence_level = 0.95
data['CI'] = t.ppf((1 + confidence_level) / 2, n_runs - 1) * data['Std_Dev(Mbps)'] / np.sqrt(n_runs)

# Plotting
plt.figure(figsize=(12, 8))

# Group by 'Congestion_Control' and plot each group
for cc, group in data.groupby('Congestion_Control'):
    plt.errorbar(
        group['Loss(%)'],
        group['Average_Goodput(Mbps)'],
        yerr=group['CI'],
        fmt='-o',
        capsize=5,
        label=f'{cc.capitalize()}'
    )

plt.title('Average Goodput vs Loss Percentage for Different Congestion Controls with 95% Confidence Interval')
plt.xlabel('Loss (%)')
plt.ylabel('Average Goodput (Mbps)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()
