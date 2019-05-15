import os

from .lue_propertyset import *






class Phenomenon(object):

    def __init__(self, working_dir=os.getcwd()):

      self._property_sets = set()

      self.working_dir = working_dir

      self.current_timestep = None


    @property
    def current_timestep(self):
      return self._current_timestep

    @current_timestep.setter
    def current_timestep(self, value):
      self._current_timestep = value



    def __len__(self):
      return len(self._property_sets)


    def __getattr__(self, property_set_name):
      result = None
      for pset in self._property_sets:
        if pset.__name__ == property_set_name:
          result = pset

      return result




    def __setattr__(self, name, value):

      if isinstance(value, Phenomenon):
        raise NotImplementedError


      elif isinstance(value, PropertySet):
        value.__name__ = name
        self._property_sets.add(value)

      else:
        self.__dict__[name] = value
