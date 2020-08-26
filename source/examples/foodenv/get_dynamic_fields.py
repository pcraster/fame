import lue.data_model as ldm

import dataframe as df




dataset = ldm.open_dataset("food_consumption.lue")

frame = df.select(dataset.foodstore, property_names=['dynamicfield'])

pp = frame['foodstore']['surrounding']['dynamicfield']

obj_values = pp[1]

print(obj_values)
