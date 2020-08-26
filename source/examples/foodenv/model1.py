import numpy
import datetime

from pcraster.framework import *
import pcraster as pcr

import sys
sys.path.insert(0, os.path.abspath('../../'))
from fame import *

import fame

seed = 1
setrandomseed(seed)



class FoodConsumption(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)

    # Framework requires a clone
    # set a dummy clone fttb
    setclone(10,20,10,0,0)
    #



  def initial(self):

    date = datetime.date(2000, 1, 2)
    time = datetime.time(12, 34)
    start = datetime.datetime.combine(date, time)
    unit = fame.TimeUnit.year
    stepsize = 2
    self.luemem = LueMemory(start, unit, stepsize, self.nrTimeSteps())

    fname = 'food_consumption.lue'
    if os.path.exists(fname):
      os.remove(fname)
    self.luemem.open(fname)

    locations = Points(mobile=False)
    # locations.read('house_locs_utr.csv')
    #locations.read('h.csv')
    locations.read('h5.csv')



    ## Houses, 1d agents fttb
    self.household = self.luemem.add_phenomenon('household', locations.nr_items)

    self.household.add_property_set('frontdoor', locations, fame.TimeDomain.dynamic)

    # Propensity will be changed and written per time step (default situation, time_discretisation keyword omitted)
    self.household.frontdoor.add_property('propensity')

    # These properties will be constant over time and stored once
    self.household.frontdoor.add_property('buffersize', time_discretisation=fame.TimeDiscretization.static)

    self.household.frontdoor.add_property('xInitial', time_discretisation=fame.TimeDiscretization.static)
    self.household.frontdoor.add_property('x')
    self.household.frontdoor.add_property('a', time_discretisation=fame.TimeDiscretization.static)
    self.household.frontdoor.add_property('betaH', time_discretisation=fame.TimeDiscretization.static)
    self.household.frontdoor.add_property('gammaH', time_discretisation=fame.TimeDiscretization.static)
    self.household.frontdoor.add_property('betaO', time_discretisation=fame.TimeDiscretization.static)
    self.household.frontdoor.add_property('gammaO', time_discretisation=fame.TimeDiscretization.static)
    self.household.frontdoor.add_property('resultingSlopeAtZero', time_discretisation=fame.TimeDiscretization.static)

    self.household.frontdoor.buffersize = 500


    self.household.frontdoor.a = fame.uniform(self.household.frontdoor, -0.0001, 0.0001, seed)
    self.household.frontdoor.betaH = 0.8
    self.household.frontdoor.gammaH = 0.8
    self.household.frontdoor.resultingSlopeAtZero = (self.household.frontdoor.gammaH * self.household.frontdoor.betaH) / 0.4

    proportionOne = 0.5
    self.household.frontdoor.betaO = proportionOne * self.household.frontdoor.betaH

    proportionTwo = 4.0
    self.household.frontdoor.gammaO = ((4 * self.household.frontdoor.resultingSlopeAtZero) / self.household.frontdoor.betaO) * proportionTwo

    self.household.frontdoor.xInitial = fame.uniform(self.household.frontdoor, -2, 2, seed)
    self.household.frontdoor.x = self.household.frontdoor.xInitial

    self.household.frontdoor.social_neighbours = neighbour_network(self.household.nr_objects, 2, 0.1, seed)


    # Food stores, 1d properties
    shop_locations = Points(mobile=False)
    #locations.read('shops_locs.csv')
    shop_locations.read('s8.csv')

    self.foodstore = self.luemem.add_phenomenon('foodstore', shop_locations.nr_items)

    nr_objects = shop_locations.nr_items

    self.foodstore.add_property_set('frontdoor', shop_locations, fame.TimeDomain.dynamic)

    self.foodstore.frontdoor.add_property('buffersize')

    self.foodstore.frontdoor.add_property('y')

    self.foodstore.frontdoor.buffersize = 500


    # Foodstore, 2d properties
    areas = Areas()
    areas.read('shops_extent.csv')
    self.foodstore.add_property_set('surrounding', areas, fame.TimeDomain.static)

    # Add one dynamic property
    self.foodstore.surrounding.add_property('dynamicfield', time_discretisation=fame.TimeDiscretization.dynamic)
    self.foodstore.surrounding.dynamicfield = -1 + fame.uniform(self.foodstore.surrounding, 0, 1, seed)

    # Add static properties
    self.foodstore.surrounding.add_property('randomfield', time_discretisation=fame.TimeDiscretization.static)
    self.foodstore.surrounding.add_property('centre', time_discretisation=fame.TimeDiscretization.static)
    self.foodstore.surrounding.add_property('spreadvalues', time_discretisation=fame.TimeDiscretization.static)

    # 'same' uniform as for point agents
    self.foodstore.surrounding.randomfield = fame.uniform(self.foodstore.surrounding, 0, 1, seed)

    # map algebra operation
    self.foodstore.surrounding.randomfield += 0.3

    # Workaround, create raster with 1 in centre (starting location)
    for idx,f in enumerate(self.foodstore.surrounding.centre.values()):
      r_centre = f.shape[0] // 2
      c_centre = f.shape[1] // 2
      a = numpy.zeros(f.shape)
      a[r_centre][c_centre] = 1
      self.foodstore.surrounding.centre.values().values[idx] = a

    # Executing PCRaster spread on each agent
    self.foodstore.surrounding.spreadvalues = fame.spread(self.foodstore.surrounding, self.foodstore.surrounding.centre, 0, 1)


    # Temporary way to decrease runtime.
    # Calculate once as we assume no changes over time
    self.foodstore.frontdoor.add_property('neighboured_houses', rank=1, shape=(self.household.nr_objects,))

    # Temporary way to decrease runtime.
    # Calculate once as we assume no changes over time
    self.household.frontdoor.add_property('neighboured_foodstores', dtype=numpy.int16, rank=1, shape=(self.foodstore.nr_objects,))

    # Assign spatial neighbours
    self.household.frontdoor.neighboured_foodstores = get_others(self.household.frontdoor.domain, self.foodstore.frontdoor.domain, self.household.frontdoor.buffersize)
    self.foodstore.frontdoor.neighboured_houses = get_others(self.foodstore.frontdoor.domain, self.household.frontdoor.domain, self.foodstore.frontdoor.buffersize)


    # Write to LUE
    self.household.frontdoor.write(self.currentTimeStep())
    self.foodstore.frontdoor.write(self.currentTimeStep())
    self.foodstore.surrounding.write(self.currentTimeStep())

    self.timestep = 0.01

    # initialize store propensity
    total_average = fame.agents_average(self.household.frontdoor.x)
    neighboured_houses_prop = network_average_def(self.foodstore.frontdoor.neighboured_houses, self.household.frontdoor.x, total_average)

    self.foodstore.frontdoor.y = neighboured_houses_prop

  # household
  def diffEqTermOne(self, x, a, betaH, gammaH):
    return -((betaH / (1.0 + fame.exp(-gammaH*(x-a)))) - (betaH/2.0))

  # food environment of household
  def diffEqTermTwo(self, y, a, betaO, gammaO):
    return ((betaO / (1.0 + fame.exp(-gammaO*(y-a)))) - (betaO/2.0))

  def dynamic(self):

    # Calculate average store propensity in neighbourhood of houses
    total_average = fame.agents_average(self.foodstore.frontdoor.y)
    neighboured_store_prop = network_average_def(self.household.frontdoor.neighboured_foodstores, self.foodstore.frontdoor.y, total_average)

    # New household propensity
    self.household.frontdoor.x = self.household.frontdoor.x + self.timestep * (self.diffEqTermOne(self.household.frontdoor.x, self.household.frontdoor.a, self.household.frontdoor.betaH, self.household.frontdoor.gammaH) + self.diffEqTermTwo(neighboured_store_prop, self.household.frontdoor.a, self.household.frontdoor.betaO, self.household.frontdoor.gammaO))


    # Calculate average house propensity in neighbourhood of stores
    total_average = fame.agents_average(self.household.frontdoor.x)
    neighboured_houses_prop = network_average_def(self.foodstore.frontdoor.neighboured_houses, self.household.frontdoor.x, total_average)

    # New store propensity
    self.foodstore.frontdoor.y = neighboured_houses_prop


    # just a dynamic map algebra operation...
    self.foodstore.surrounding.dynamicfield += 1


    self.household.frontdoor.write(self.currentTimeStep())
    self.foodstore.surrounding.write(self.currentTimeStep())


timesteps = 6

myModel = FoodConsumption()
dynFrw = DynamicFramework(myModel, timesteps)
dynFrw.run()
print()
