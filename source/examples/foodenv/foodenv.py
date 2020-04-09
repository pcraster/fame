import numpy
import datetime

from pcraster.framework import *

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
    #

  def premcloop(self):
    pass

  def postmcloop(self):
    pass




  def initial(self):

    self.luemem = LueMemory(self.nrTimeSteps())

    dataset_name = os.path.join(str(self.currentSampleNumber()), 'food_consumption_{}'.format(self.currentSampleNumber()))
    self.luemem.open(dataset_name)

    locations = Points()
    # locations.read('house_locs_utr.csv')
    locations.read('h.csv')



    # Houses, 1d agents fttb
    self.household = self.luemem.add_phenomenon('household', locations.nr_items)

    self.household.add_property_set('frontdoor', locations, fame.TimeDomain.dynamic)

    self.household.frontdoor.add_property('propensity')
    self.household.frontdoor.add_property('default_propensity')
    self.household.frontdoor.add_property('alpha')
    self.household.frontdoor.add_property('beta')
    self.household.frontdoor.add_property('gamma')
    self.household.frontdoor.add_property('buffersize')
    self.household.frontdoor.add_property('social_neighbours')

    # Temporary way to decreaser runtime.
    # Calculate once as we assume no changes over time
    self.household.frontdoor.add_property('neighboured_foodstores')

    nr_objects = self.household.nr_objects
    self.household.frontdoor.alpha.values = 0.15
    self.household.frontdoor.beta.values = 0.5
    self.household.frontdoor.gamma.values = 0.0
    self.household.frontdoor.buffersize.values = 500
    self.household.frontdoor.default_propensity.values = 0.4

    lower = -0.18344355629253628
    upper = -0.16344355629253626
    self.household.frontdoor.propensity.values = uniform(self.household.frontdoor, lower, upper)

    self.household.frontdoor.social_neighbours.values = neighbour_network(nr_objects, 40, 0.1, seed)




    # Food stores, 1d agents fttb
    locations = Points()
    locations.read('shops_locs.csv')

    self.foodstore = self.luemem.add_phenomenon('foodstore', locations.nr_items)


    nr_objects = locations.nr_items

    self.foodstore.add_property_set('frontdoor', locations, fame.TimeDomain.dynamic)

    self.foodstore.frontdoor.add_property('propensity')
    self.foodstore.frontdoor.add_property('buffersize')
    self.foodstore.frontdoor.add_property('delta')




    self.foodstore.frontdoor.propensity.values = uniform(self.foodstore.frontdoor, lower, upper)
    self.foodstore.frontdoor.buffersize.values = 500
    self.foodstore.frontdoor.delta = 0.2


    areas = Areas()
    # areas.read('shops_areas.csv')
    self.foodstore.add_property_set('surrounding', locations, fame.TimeDomain.dynamic)

    self.foodstore.surrounding.add_property('randomfield')
    self.foodstore.surrounding.randomfield.values = numpy.random.uniform(-1, 1, (nr_objects, 2, 2))


    # Temporary way to decreaser runtime.
    # Calculate once as we assume no changes over time
    self.foodstore.frontdoor.add_property('neighboured_houses')

    # Assign spatial neighbours
    self.household.frontdoor.neighboured_foodstores.values = get_others(self.household.frontdoor.domain, self.foodstore.frontdoor.domain, self.household.frontdoor.buffersize)
    self.foodstore.frontdoor.neighboured_houses.values = get_others(self.foodstore.frontdoor.domain, self.household.frontdoor.domain, self.foodstore.frontdoor.buffersize)

    self.timestep = 0.5


  def dynamic(self):
    print('dynamic {}'.format(self.currentTimeStep()))
    # Houses
    term1 = self.household.frontdoor.alpha * (self.household.frontdoor.default_propensity - self.household.frontdoor.propensity)

    # Second term

    # Calculate the potential default value for households in case no food is in buffer
    # Averages per object, holds items * (shape)
    tmp_averages = average(self.foodstore.frontdoor.propensity)
    total_average = property_average(tmp_averages)

    # Averages of neighbours in buffer
    #neighboured_store_prop = focal_average_others(self.household.frontdoor.domain, self.foodstore.frontdoor.domain, self.foodstore.frontdoor.propensity, self.household.frontdoor.buffersize, total_average, self.household.frontdoor.propensity)

    neighboured_store_prop = network_average_def(self.household.frontdoor.neighboured_foodstores, self.foodstore.frontdoor.propensity, total_average)



    term2 =  self.household.frontdoor.beta * (neighboured_store_prop * (1.0 - abs(self.household.frontdoor.propensity)))

    # Social network
    social_neighbours_prop = network_average(self.household.frontdoor.social_neighbours, self.household.frontdoor.propensity, os.path.join(str(self.currentSampleNumber()), 'nw_{}.txt'.format(self.currentTimeStep())))
    term3 =  self.household.frontdoor.gamma * (social_neighbours_prop * (1.0 - abs(self.household.frontdoor.propensity)))


    self.household.frontdoor.propensity += self.timestep * (term1 + term2 + term3)


    # Foodstores
    total_average = property_average(average(self.household.frontdoor.propensity))

    #neighboured_houses_prop = focal_average_others(self.foodstore.frontdoor.domain, self.household.frontdoor.domain, self.household.frontdoor.propensity, self.foodstore.frontdoor.buffersize, total_average, self.foodstore.frontdoor.propensity)

    neighboured_houses_prop = network_average_def(self.foodstore.frontdoor.neighboured_houses, self.household.frontdoor.propensity, total_average)


    self.foodstore.frontdoor.propensity += self.foodstore.frontdoor.delta * self.timestep * (neighboured_houses_prop - self.foodstore.frontdoor.propensity)







    # We plainly write to PCRaster maps for simplicity of (timeseries) display
    sample_dir = str(self.currentSampleNumber())

    fname = 'houses_{}.map'.format(self.currentTimeStep())
    pset_report(self.household.frontdoor.propensity, fname, sample_dir, self.currentTimeStep(), 'h')

    fname = 'shops_{}.map'.format(self.currentTimeStep())
    pset_report(self.foodstore.frontdoor.propensity, fname, sample_dir, self.currentTimeStep(), 's')






timesteps = 20
samples = 2

myModel = FoodConsumption()
dynFrw = DynamicFramework(myModel, timesteps)
mcFrw = MonteCarloFramework(dynFrw, samples)
#mcFrw.setForkSamples(True)
mcFrw.run()

print()
