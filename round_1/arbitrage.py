import pandas as pd
import numpy as np

# Creating the exchange rate table as a pandas DataFrame
exchange_rates = pd.DataFrame({
    'Snowballs':   [1,    0.7,   1.95,  1.34],
    'Pizza\'s':    [1.45, 1,     3.1,   1.98],
    'Silicon Nuggets': [0.52, 0.31,  1,     0.64],
    'SeaShells':   [0.72, 0.48,  1.49,  1]
}, index=['Snowballs', 'Pizza\'s', 'Silicon Nuggets', 'SeaShells'])

exchange_array = exchange_rates.to_numpy()

print(exchange_array)

array_transpose = np.transpose(exchange_array)

multiplied_array = np.multiply(exchange_array, array_transpose)

print(multiplied_array)