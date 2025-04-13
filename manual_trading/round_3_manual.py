
import numpy as np


DISTRIBUTION_PROBABILITY = 1/110

def find_proportion(value):
    if value < 250:
        return DISTRIBUTION_PROBABILITY* (min(value, 200)-160)
    else:
        return 4/11 + DISTRIBUTION_PROBABILITY * (value-250)

def find_value(value, proportion):
    return value * proportion


