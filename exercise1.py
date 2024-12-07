import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import t

# Dataset
data = pd.DataFrame({
    'Loss(%)': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Average_Goodput(Mbps)': [94.8, 93.05, 89.20, 66.85, 42.25, 23.55, 13.58, 10.1, 7.15, 5, 3.9],
    'Std_Dev(Mbps)': [0, 0.22, 1.17, 5.15, 5.10, 4.30, 2.43, 1.79, 1.46, 0, 0.7]
})

# Number of runs and confidence interval
n_runs = 20
confidence_level = 0.95
data['CI'] = t.ppf((1 + confidence_level) / 2, n_runs - 1) * data['Std_Dev(Mbps)'] / np.sqrt(n_runs)

# Calculate second derivative for curvature approximation
goodput = data['Average_Goodput(Mbps)'].values
loss = data['Loss(%)'].values

# Approximate the second derivative
second_derivative = np.gradient(np.gradient(goodput, loss), loss)

# Find the index of the largest (most negative) second derivative
biggest_knee_index = np.argmin(second_derivative)
biggest_knee = loss[biggest_knee_index]
knee_goodput = goodput[biggest_knee_index]

# Plotting the results
plt.figure(figsize=(10, 6))
plt.errorbar(
    data['Loss(%)'],
    data['Average_Goodput(Mbps)'],
    yerr=data['CI'],
    fmt='-o',
    capsize=5,
    label='Average Goodput with 95% CI'
)
plt.scatter(biggest_knee, knee_goodput, color='red', zorder=5, label=f'Biggest Knee: Loss={biggest_knee}%, Goodput={knee_goodput:.2f} Mbps')
plt.title('Average Goodput vs Loss Percentage with 95% Confidence Interval')
plt.xlabel('Loss (%)')
plt.ylabel('Average Goodput (Mbps)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()
