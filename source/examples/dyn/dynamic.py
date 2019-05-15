# Using the PCRaster modelling framework to model changes in time
import numpy
from pcraster.framework import *

from fame import *


class LueDynamic(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)
    # Framework requires a clone
    # set a dummy clone fttb
    setclone(1, 1, 1, 0, 0)


    self.tmp_out = os.path.join(os.getcwd(), 'tmp')

    self.countries = Phenomenon()
    self.countries.catchments = PropertySet()

    # prepare domain
    areas = Areas()
    areas.read('areas.csv')

    # 'clone map' extents
    self.countries.catchments.domain = areas
    # workaround to generate the areas on the fly...
    ones = numpy.ones((self.countries.catchments.domain.nr_items, 21, 27), dtype=numpy.int32)

    self.countries.catchments.clones = Property()
    self.countries.catchments.clones.values = ones


  def initial(self):

    self.countries.catchments.alives = uniform(self.countries.catchments.clones) < 0.15

    report(self.countries.catchments.alives, self.tmp_out, self.currentTimeStep(), Boolean)


  def dynamic(self):

    numberOfAliveNeighbours = windowtotal(self.countries.catchments.alives, 15)  - self.countries.catchments.alives

    threeAliveNeighbours = numberOfAliveNeighbours == 3

    birth = threeAliveNeighbours &  ~self.countries.catchments.alives

    survivalA = (numberOfAliveNeighbours == 2) & self.countries.catchments.alives
    survivalB = (numberOfAliveNeighbours == 3) & self.countries.catchments.alives
    survival = survivalA | survivalB

    self.countries.catchments.alives = birth | survival

    report(self.countries.catchments.alives, self.tmp_out, self.currentTimeStep(), Boolean)


myModel = LueDynamic()
dynModel = DynamicFramework(myModel, 150)
dynModel.run()





















