import pandas as pd
import numpy as np

# Creating the exchange rate table as a pandas DataFrame

initial_values = [(0,1.34,['snowballs']), (1,1.98,['pizza']), (2,0.64,['silicon']), (3,1,['seashells'])]

"""
0: snowballs
1: pizza
2: silicon
3: seashells
"""
index_to_currency = {
    0: 'snowballs',
    1: 'pizza',
    2: 'silicon',
    3: 'seashells'
}
exchange_array = np.array([
    [1.00, 1.45, 0.52, 0.72],
    [0.70, 1.00, 0.31, 0.48],
    [1.95, 3.10, 1.00, 1.49],
    [1.34, 1.98, 0.64, 1.00]
])

"""
If you run the code it spits out a list of every sequence of five trades, sorted by how much money you have at the end.

The first element of the tuple is the index of the currency you end with, the second is how much money you have, and the third is the sequence of trades you made.

I didn't include the first element as seashells because that's obvious
"""

# print(exchange_array)

# array_transpose = np.transpose(exchange_array)
# print(array_transpose)

# multiplied_array = np.multiply(exchange_array
#                                , array_transpose)

# print(multiplied_array)



def exchange(curr_index, curr_value, sequence, next_index):
    curr_value *= exchange_array[curr_index][next_index]
    new_sequence = sequence.copy()
    new_sequence.append(index_to_currency[next_index])
    return (next_index, curr_value, new_sequence)

final_list = initial_values.copy()
for iteration in range(3):
    final_values = []
    c = 0
    while c < len(initial_values):
        curr_index, curr_value, sequence = initial_values[c]
        
        # if len(sequence) == 4:
        #     c += 1
        #     continue  # Do not expand further
        
#        print(f"Expanding from {index_to_currency[curr_index]} with value {curr_value:.2f}")
        
        for i in range(len(exchange_array)):
            if i != curr_index:
                next_index, new_value, next_sequence = exchange(curr_index, curr_value, sequence, i)
                final_values.append((next_index, new_value, next_sequence))
                
        c += 1
    initial_values = final_values.copy()
    print("finished index", iteration)
    final_list += initial_values

last_exchange = []
for tup in final_list:
    last_exchange.append(exchange(tup[0],tup[1],tup[2],3))


last_exchange.sort(key=lambda x: x[1])
print(last_exchange)


# final_list.sort(key=lambda x: x[1])
# print(final_list)

