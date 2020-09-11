import enum

import lue.data_model as ldm

class TimeDomain(enum.Enum):
  """ Class to indicate time domain of a property set """
  static = 1
  dynamic = 2



class TimeDiscretization(enum.Enum):
  """ Class to indicate temporal discretisation of a property set """
  static = 1
  dynamic = 2


class TimeUnit(enum.Enum):
  """ Class to indicate time step unit """

  day = ldm.Unit.day
  year = ldm.Unit.year
