import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import t

# Assuming your dataset is structured as follows:
# Loss(%) | Average Goodput (Mbps) | Std Dev (Mbps)
data = pd.DataFrame({
    'Loss(%)': [5, 20,50],  # Replace with your loss percentage data
    'Average_Goodput(Mbps)': [92.9, 92.45, 86.45],  # Replace with your goodput data
    'Std_Dev(Mbps)': [0.44, .92, 8.66]  # Replace with your standard deviation data
})

# Number of runs (samples per loss percentage)
n_runs = 20

# Calculate 95% confidence intervals
confidence_level = 0.95
data['CI'] = t.ppf((1 + confidence_level) / 2, n_runs - 1) * data['Std_Dev(Mbps)'] / np.sqrt(n_runs)

# Plotting
plt.figure(figsize=(10, 6))
plt.errorbar(
    data['Loss(%)'],
    data['Average_Goodput(Mbps)'],
    yerr=data['CI'],
    fmt='-o',
    capsize=5,
    label='Average Goodput with 95% CI'
)
plt.title('Average Goodput vs Loss Percentage with 95% Confidence Interval')
plt.xlabel('Loss (%)')
plt.ylabel('Average Goodput (Mbps)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()
