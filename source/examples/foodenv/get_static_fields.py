import lue.data_model as ldm

import dataframe as df




dataset = ldm.open_dataset("1/food_consumption_1.lue")


frame = df.select(dataset.foodstore, property_names=['spreadvalues', 'centre', 'randomfield'])

prop = frame['foodstore']['surrounding']['spreadvalues']



obj = prop[2]

print(obj.values)
