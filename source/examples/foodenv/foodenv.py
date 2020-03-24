import numpy
import datetime

from pcraster.framework import *

import sys
sys.path.insert(0, os.path.abspath('../../'))
from fame import *


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

    dataset_name = os.path.join(str(self.currentSampleNumber()), 'food_consumption_{}'.format(self.currentSampleNumber()))

    self.luemem = LueMemory(dataset_name, self.nrTimeSteps())


    locations = Points()
    locations.read('houses_locs_utr.csv')



    # Houses, 1d agents fttb
    self.household = self.luemem.add_phenomenon('household', locations.nr_items)


    self.household.add_property_set('frontdoor')
    self.household.frontdoor.set_space_domain('location', locations)

    self.household.frontdoor.add_property('propensity')
    self.household.frontdoor.add_property('default_propensity')
    self.household.frontdoor.add_property('alpha')
    self.household.frontdoor.add_property('beta')
    self.household.frontdoor.add_property('gamma')
    self.household.frontdoor.add_property('buffersize')
    self.household.frontdoor.add_property('neighbours')

    nr_objects = self.household.nr_objects
    self.household.frontdoor.alpha.values = 0.15
    self.household.frontdoor.beta.values = 0.6
    self.household.frontdoor.gamma.values = 0.5
    self.household.frontdoor.buffersize.values = 500
    self.household.frontdoor.propensity.values = -0.17
    self.household.frontdoor.default_propensity.values = numpy.random.uniform(-1, 1, (nr_objects))

    self.household.frontdoor.neighbours.values = neighbour_network(nr_objects, 40, 0.1, seed)



    # Food stores, 1d agents fttb
    locations = Points()
    locations.read('shops_locs.csv')

    self.foodstore = self.luemem.add_phenomenon('foodstore', locations.nr_items)


    nr_objects = locations.nr_items

    self.foodstore.add_property_set('frontdoor')
    self.foodstore.frontdoor.set_space_domain('location', locations)

    self.foodstore.frontdoor.add_property('propensity')
    self.foodstore.frontdoor.add_property('buffersize')
    self.foodstore.frontdoor.add_property('delta')


    self.foodstore.frontdoor.propensity.values = numpy.random.uniform(-1, 1, (nr_objects))
    self.foodstore.frontdoor.buffersize.values = 500
    self.foodstore.frontdoor.delta = 0.2

    self.foodstore.add_property_set('surrounding')
    areas = Areas()
    # areas.read('shops_areas.csv')

    self.foodstore.surrounding.set_space_domain('areas', areas)
    self.foodstore.surrounding.add_property('randomfield')
    self.foodstore.surrounding.randomfield.values = numpy.random.uniform(-1, 1, (nr_objects, 2, 2))


    self.timestep = 0.5


  def dynamic(self):
    print('dynamic {}'.format(self.currentTimeStep()))
    # Houses
    # First term
    tmp1 = self.household.frontdoor.alpha * (self.household.frontdoor.default_propensity - self.household.frontdoor.propensity)

    # Second term

    # Calculate the potential default value for households in case no food is in buffer
    # Averages per object, holds items * (shape)
    tmp_averages = average(self.foodstore.frontdoor.propensity)
    total_average = property_average(tmp_averages)

    # Averages of neighbours in buffer
    neighboured_store_prop = focal_average_others(self.household.frontdoor.domain, self.foodstore.frontdoor.domain, self.foodstore.frontdoor.propensity, self.household.frontdoor.buffersize, total_average, self.household.frontdoor.propensity)


    tmp2 =  self.household.frontdoor.beta * (neighboured_store_prop * (1.0 - abs(self.household.frontdoor.propensity)))

    # Social network
    social_neighbours_prop = network_average(self.household.frontdoor.neighbours, self.household.frontdoor.propensity, os.path.join(str(self.currentSampleNumber()), 'nw_{}.txt'.format(self.currentTimeStep())))
    tmp3 =  self.household.frontdoor.gamma * (social_neighbours_prop * (1.0 - abs(self.household.frontdoor.propensity)))


    self.household.frontdoor.propensity += self.timestep * (tmp1 + tmp2 + tmp3)


    # Foodstores
    total_average = property_average(average(self.household.frontdoor.propensity))

    neighboured_houses_prop = focal_average_others(self.foodstore.frontdoor.domain, self.household.frontdoor.domain, self.household.frontdoor.propensity, self.foodstore.frontdoor.buffersize, total_average, self.foodstore.frontdoor.propensity)

    self.foodstore.frontdoor.propensity += self.foodstore.frontdoor.delta * self.timestep * (neighboured_houses_prop - self.foodstore.frontdoor.propensity)







    # We plainly write to PCRaster maps for simplicity of (timeseries) display
    sample_dir = str(self.currentSampleNumber())

    fname = 'houses_{}.map'.format(self.currentTimeStep())
    pset_report(self.household.frontdoor.propensity, fname, sample_dir,'h')

    fname = 'shops_{}.map'.format(self.currentTimeStep())
    pset_report(self.foodstore.frontdoor.propensity, fname, sample_dir,'s')






timesteps = 200
samples = 2

myModel = FoodConsumption()
dynFrw = DynamicFramework(myModel, timesteps)
mcFrw = MonteCarloFramework(dynFrw, samples)
#mcFrw.setForkSamples(True)
mcFrw.run()

print()
