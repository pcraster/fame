import os

from .lue_propertyset import *






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





    def add_property_set(self, value):
      assert isinstance(value, str)

      p = PropertySet(self._nr_objects) #self)
      p.__name__ = value
      self._property_sets.add(p)


    @property
    def nr_objects(self):
      return self._nr_objects

