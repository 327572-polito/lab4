import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import t
import numpy as np

# Define the dataset
data = pd.DataFrame({
    'RTT(ms)': [10, 10, 10, 100, 100, 100, 300, 300, 300],
    'Loss(%)': [1, 3, 5, 1, 3, 5, 1, 3, 5],
    'Average_Goodput(Mbps)': [17.9, 7.72, 5.06, 2.9, 0.433, 0.615, 0.9932, 0.437, 0.4069],
    'Std_Dev(Mbps)': [3.6, 0.73, 0.7, 1.26, 0.458, 0.289, 0.232, 0.307, 0.221]
})

# Number of runs (samples per condition)
n_runs = 20

# Calculate 95% confidence intervals
confidence_level = 0.95
data['CI'] = t.ppf((1 + confidence_level) / 2, n_runs - 1) * data['Std_Dev(Mbps)'] / np.sqrt(n_runs)

# Plotting
plt.figure(figsize=(10, 6))

# Group by 'Delay(ms)' and plot each group
for RTT, group in data.groupby('RTT(ms)'):
    plt.errorbar(
        group['Loss(%)'],
        group['Average_Goodput(Mbps)'],
        yerr=group['CI'],
        fmt='-o',
        capsize=5,
        label=f'RTT {RTT} ms'
    )

plt.title('Average Goodput vs Loss Probability for Different Delays with 95% Confidence Interval')
plt.xlabel('Loss (%)')
plt.ylabel('Average Goodput (Mbps)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()
