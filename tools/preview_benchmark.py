import json 
import numpy as np
import matplotlib.pyplot as plt 

# --- load data 
print("Loading benchmark data.")
results_a = json.load(open("./data/benchmarks/5k/nearest.benchmark-1000-500-100.json"))
results_a = np.array(results_a)
results_b = json.load(open("./data/benchmarks/10k/nearest.benchmark-1000-500-100.json"))
results_b = np.array(results_b)

# --- distribution of 100% accuracy
final_a = results_a[:,-1]
final_b = results_b[:,-1]

# --- show histogram
plt.hist(final_a, bins=20, alpha=0.5, label="5k")
plt.hist(final_b, bins=20, alpha=0.5, label="10k")
plt.legend()

plt.show()