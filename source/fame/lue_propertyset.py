import numpy

import lue


import fame.lue_points as lue_points
import fame.lue_areas as lue_areas
import fame.lue_property as lue_property
import fame.lue_phenomenon as fame_phen

from .fame_utils import TimeDiscretization



class PropertySet(object):

    def __init__(self, phen, space_domain=None, time_domain=None):

      self._lue_dataset_name = None
      self._lue_phenomenon_name = None
      self._phen = phen

      self._properties = set()

      self.__name__ = None

      self._domain = None

      self._space_domain = space_domain
      self._time_domain = time_domain


    @property
    def space_domain(self):
      return self.space_domain


    @property
    def time_domain(self):
      return self.time_domain

    @property
    def domain(self):
      return self._domain


    def nr_objects(self):
      return self._phen



    def __len__(self):
      return len(self._properties)





    def __getattr__(self, property_name):
      result = None
      for p in self._properties:
        if p.name == property_name:
          result = p

      return result



    def set_space_domain(self, variable, values):
      assert isinstance(variable, str)
      if isinstance(values, lue_points.Points):

        self._domain = values


      elif isinstance(values, lue_areas.Areas):

        self._domain = values


      else:
        raise NotImplementedError

      for p in self._properties:
        p.pset_domain = self._domain


    def add_property(self, property_name, dtype=numpy.float64, time_discretisation=TimeDiscretization.dynamic):

      assert isinstance(property_name, str)
      assert self._lue_dataset_name is not None

      # FAME
      p = lue_property.Property(self._phen)
      p.name = property_name
      p.pset_domain = self._domain

      p._lue_pset_name = self.__name__

      self._properties.add(p)

      # LUE

      nr_timesteps = self._lue_dataset.phenomena['framework'].property_sets['fame_time_cell'].time_domain.value[0][1]

      pset = self._lue_dataset.phenomena[self._lue_phenomenon_name].property_sets[self.__name__]
      prop = pset.add_property(property_name, dtype=numpy.dtype(dtype), shape=(1,nr_timesteps), value_variability=lue.ValueVariability.variable)
# nr_timesteps,1
      prop.value.expand(self.nr_objects())


      lue.assert_is_valid(self._lue_dataset_name)



    def write(self, timestep=None):

        if timestep is not None:
          timestep -= 1
          lue_pset = self._lue_dataset.phenomena[self._lue_phenomenon_name].property_sets[self.__name__]

          for prop in self._properties:
            if prop.name != 'neighboured_houses' and prop.name != 'neighboured_foodstores':

                lue_prop = lue_pset.properties[prop.name]
#                raise SystemExit



        else:
          # in initial...
          pass

        lue.assert_is_valid(self._lue_dataset_name)



