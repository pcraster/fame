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
numpy.random.seed(seed)



class FoodConsumption(DynamicModel, MonteCarloModel):
  def __init__(self):
    DynamicModel.__init__(self)
    MonteCarloModel.__init__(self)

    # Framework requires a clone
    # set a dummy clone fttb
    setclone('houses.map')
    setclone(6, 10, 1234.5, -987.6, 543.2)
    #

  def premcloop(self):
    pass

  def postmcloop(self):
    pass




  def initial(self):

    self.luemem = LueMemory(self.nrTimeSteps())

    dataset_name = os.path.join(str(self.currentSampleNumber()), 'food_consumption_{}'.format(self.currentSampleNumber()))
    self.luemem.open(dataset_name)

    locations = Points(mobile=False)
    # locations.read('house_locs_utr.csv')
    #locations.read('h.csv')
    locations.read('h5.csv')



    ## Houses, 1d agents fttb
    #self.household = self.luemem.add_phenomenon('household', locations.nr_items)

    #self.household.add_property_set('frontdoor', locations, fame.TimeDomain.dynamic)

    ## Propensity will be changed and written per time step (default situation)
    #self.household.frontdoor.add_property('propensity')
    ## These properties will be constant over time and stored once
    #self.household.frontdoor.add_property('default_propensity', time_discretisation=fame.TimeDiscretization.static)
    #self.household.frontdoor.add_property('alpha', time_discretisation=fame.TimeDiscretization.static)
    #self.household.frontdoor.add_property('beta', time_discretisation=fame.TimeDiscretization.static)
    #self.household.frontdoor.add_property('gamma', time_discretisation=fame.TimeDiscretization.static)
    #self.household.frontdoor.add_property('buffersize', time_discretisation=fame.TimeDiscretization.static)
    #self.household.frontdoor.add_property('social_neighbours', dtype=numpy.int64)


    ##
    #self.household.frontdoor.alpha = 0.15
    #raise SystemExit
    #self.household.frontdoor.beta = 0.5
    #self.household.frontdoor.gamma = 0.0
    #self.household.frontdoor.buffersize = 500
    #self.household.frontdoor.default_propensity = 0.4

    #lower = -0.18344355629253628
    #upper = -0.16344355629253626
    ##self.household.frontdoor.propensity = fame.uniform(self.household.frontdoor, lower, upper)

    #self.household.frontdoor.social_neighbours = neighbour_network(self.household.nr_objects, 2, 0.1, seed)


    ## Food stores, 1d agents fttb
    #shop_locations = Points(mobile=False)
    ##locations.read('shops_locs.csv')
    #shop_locations.read('s8.csv')

    #self.foodstore = self.luemem.add_phenomenon('foodstore', shop_locations.nr_items)

    #nr_objects = shop_locations.nr_items

    #self.foodstore.add_property_set('frontdoor', shop_locations, fame.TimeDomain.dynamic)

    #self.foodstore.frontdoor.add_property('fpropensity')
    #self.foodstore.frontdoor.add_property('buffersize')
    #self.foodstore.frontdoor.add_property('delta')
    #self.foodstore.frontdoor.add_property('upper')

    #self.foodstore.frontdoor.upper = -0.16344355629253626
    #self.foodstore.frontdoor.fpropensity = fame.uniform(self.foodstore.frontdoor, lower, self.foodstore.frontdoor.upper)
    #self.foodstore.frontdoor.buffersize = 500
    #self.foodstore.frontdoor.delta = 0.2

    #areas = Areas()
    #areas.read('shops_extent.csv')
    #self.foodstore.add_property_set('surrounding', areas, fame.TimeDomain.static)

    #self.foodstore.surrounding.add_property('randomfield')
    ##self.foodstore.surrounding.add_property('upper')

    ##self.foodstore.surrounding.randomfield = fame.uniform(self.foodstore.surrounding, 0, 1)


    ## Temporary way to decrease runtime.
    ## Calculate once as we assume no changes over time
    #self.foodstore.frontdoor.add_property('neighboured_houses', rank=1, shape=(self.household.nr_objects,))

    ## Temporary way to decrease runtime.
    ## Calculate once as we assume no changes over time
    #self.household.frontdoor.add_property('neighboured_foodstores', dtype=numpy.int16, rank=1, shape=(self.foodstore.nr_objects,))

    ## Assign spatial neighbours
    ##self.household.frontdoor.neighboured_foodstores = get_others(self.household.frontdoor.domain, self.foodstore.frontdoor.domain, self.household.frontdoor.buffersize)
    ##self.foodstore.frontdoor.neighboured_houses = get_others(self.foodstore.frontdoor.domain, self.household.frontdoor.domain, self.foodstore.frontdoor.buffersize)

    #self.timestep = 0.5


    ## Read the Utrecht map

    ## for testing we use a dummy raster
    ##self.raster = 1000 + pcr.uniqueid(1)
    ##self.report(self.raster, 'tmp_raster')

    ### One raster object with house locations
    ##self.aoi = self.luemem.add_phenomenon('extent', 1)

    ### Also add one raster holding the entire modelling area (municipality Utrecht) to the dataset
    ##area = Areas()
    ##area.read('utrecht.csv')

    ##self.aoi.add_property_set('utrecht', area, fame.TimeDomain.static)
    ##self.aoi.utrecht.add_property('houses')

    ## self.raster = pcr.readmap('houses.map')
    ## raster_np = pcr.pcr2numpy(self.raster, numpy.nan)
    ## self.aoi.utrecht.houses.values = raster_np

    ##self.aoi.utrecht.write()





  def dynamic(self):
    print('dynamic {}'.format(self.currentTimeStep()))

    #self.household.frontdoor.propensity = fame.uniform(self.household.frontdoor, 0, 1)

    #self.household.frontdoor.write(self.currentTimeStep())

    ## Houses
    #term1 = self.household.frontdoor.alpha * (self.household.frontdoor.default_propensity - self.household.frontdoor.propensity)

    ## Second term

    ## Calculate the potential default value for households in case no food store is within buffer
    ## Averages per object, holds items * (shape)
    ##tmp_averages = fame.average(self.foodstore.frontdoor.propensity)
    ##total_average = property_average(tmp_averages)
    #total_average = fame.agents_average(self.foodstore.frontdoor.fpropensity)

    ####### Averages of neighbours in buffer
    #######neighboured_store_prop = focal_average_others(self.household.frontdoor.domain, self.foodstore.frontdoor.domain, self.foodstore.frontdoor.propensity, self.household.frontdoor.buffersize, total_average, self.household.frontdoor.propensity)

    #neighboured_store_prop = network_average_def(self.household.frontdoor.neighboured_foodstores, self.foodstore.frontdoor.fpropensity, total_average)


    #term2 =  self.household.frontdoor.beta * (neighboured_store_prop * (1.0 - fame.abs(self.household.frontdoor.propensity)))


    ## Social network
    #social_neighbours_prop = network_average(self.household.frontdoor.social_neighbours, self.household.frontdoor.propensity, os.path.join(str(self.currentSampleNumber()), 'nw_{}.txt'.format(self.currentTimeStep())))
    #term3 =  self.household.frontdoor.gamma * (social_neighbours_prop * (1.0 - fame.abs(self.household.frontdoor.propensity)))


    #self.household.frontdoor.propensity = self.timestep #* (term1 + term2 + term3)
    ##self.household.frontdoor.propensity = 5#self.household.frontdoor.propensity + self.timestep * (term1 + term2 + term3)


    ## Foodstores
    #total_average = fame.agents_average(self.household.frontdoor.propensity)

    ##neighboured_houses_prop = focal_average_others(self.foodstore.frontdoor.domain, self.household.frontdoor.domain, self.household.frontdoor.propensity, self.foodstore.frontdoor.buffersize, total_average, self.foodstore.frontdoor.propensity)

    #neighboured_houses_prop = network_average_def(self.foodstore.frontdoor.neighboured_houses, self.household.frontdoor.propensity, total_average)


    #self.foodstore.frontdoor.fpropensity += self.timestep * self.foodstore.frontdoor.delta  * (neighboured_houses_prop - self.foodstore.frontdoor.fpropensity)


    ## Some processes irrelevant for food environment
    ## just for demonstration purpose of field operations

    #self.foodstore.surrounding.randomfield += fame.uniform(self.foodstore.surrounding, 0, 1)
    ## Binding to PCRaster
    #self.foodstore.surrounding.randomfield = fame.slope(self.foodstore.surrounding.randomfield)


    #self.household.frontdoor.write(self.currentTimeStep())

    ##self.foodstore.frontdoor.write(self.currentTimeStep())

    ##self.foodstore.surrounding.write(self.currentTimeStep())





timesteps = 37
samples = 1

myModel = FoodConsumption()
dynFrw = DynamicFramework(myModel, timesteps)
mcFrw = MonteCarloFramework(dynFrw, samples)
#mcFrw.setForkSamples(True)
mcFrw.run()

print()
