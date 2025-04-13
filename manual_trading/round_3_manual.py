import numpy as np
import matplotlib.pyplot as plt

DISTRIBUTION_PROBABILITY = 1/110

def find_proportion(value):
    if value < 250:
        return DISTRIBUTION_PROBABILITY* (min(value, 200)-160)
    else:
        return 4/11 + DISTRIBUTION_PROBABILITY * (value-250)

def find_value(value, proportion):
    return (320-value) * proportion


array = np.arange(160, 320, 0.1)  # Include 320 by setting the stop value slightly higher
print(array)

# Compute 320 - each value in array
new_array = 320 - array
print(new_array)

# Apply find_proportion to every value in the array
proportions = np.array([find_proportion(value) for value in array])
print(proportions)

result = new_array * proportions
print(result)

# Plot the graph
plt.plot(array, result, label="Result vs Array")
plt.xlabel("Array (x-axis)")
plt.ylabel("Result (y-axis)")
plt.title("Graph of Result vs Array")
plt.legend()
plt.grid(True)
plt.show()