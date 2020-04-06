import enum
import os

from .lue_propertyset import *



class TimeDomain(enum.Enum):
  """ Class to indicate time domain of a property set """
  static = 1
  dynamic = 2




class Phenomenon(object):

    def __init__(self, nr_objects, working_dir=os.getcwd()):

        self._property_sets = set()

        self.working_dir = working_dir
        self._nr_objects = nr_objects




    def __len__(self):
      return len(self._property_sets)


    def __getattr__(self, property_set_name):
      result = None

      for pset in self._property_sets:
        if pset.__name__ == property_set_name:
          result = pset

      return result





    def add_property_set(self, value, space_domain=None, time_domain=None):
      assert isinstance(time_domain, TimeDomain)

      assert isinstance(value, str)

      self._space_domain = space_domain
      self._time_domain = time_domain

      p = PropertySet(self._nr_objects)
      p.__name__ = value
      p.set_space_domain('locationdfg', space_domain)
      self._property_sets.add(p)




    @property
    def nr_objects(self):
      return self._nr_objects

    @property
    def time_domain(self):
      return self._time_domain
