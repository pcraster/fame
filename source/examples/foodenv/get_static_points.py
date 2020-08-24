import lue.data_model as ldm

import dataframe as df




dataset = ldm.open_dataset("1/food_consumption_1.lue")

frame = df.select(dataset.household, property_names=['default_propensity', 'alpha', 'beta', 'gamma', 'buffersize'])

pp = frame['household']['frontdoor']['default_propensity']

obj_values = pp['values']

print(obj_values)
