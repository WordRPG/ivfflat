import json 
import numpy as np
import matplotlib.pyplot as plt 

# --- load data 
print("Loading benchmark data.")
results = json.load(open("./data/benchmarks/farthest.benchmark-1000-500-100.json"))
results = np.array(results)

# --- distribution of 100% accuracy
final = results[:,-1]

# --- show histogram
plt.hist(final, bins=20)
plt.show()