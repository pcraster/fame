import numpy
import os

import lue


import fame.lue_points as lue_points
import fame.lue_propertyset as fame_pset
from .lue_points import Points

from .fame_utils import TimeDomain





class Phenomenon(object):

    def __init__(self, nr_objects, working_dir=os.getcwd()):

        self._property_sets = set()

        self.working_dir = working_dir
        self._nr_objects = nr_objects

        # Plain list of object IDs
        self._object_ids = numpy.arange(self._nr_objects, dtype=lue.dtype.ID)

        self._lue_dataset = None
        self._lue_dataset_name = None
        self._nr_timesteps = None






    def __len__(self):
      return len(self._property_sets)


    def __getattr__(self, property_set_name):
      result = None

      for pset in self._property_sets:
        if pset.__name__ == property_set_name:
          result = pset

      return result





    def add_property_set(self, pset_name, space_domain=None, time_domain=None):
      """ Adding a property set """
      assert isinstance(time_domain, TimeDomain)

      assert isinstance(pset_name, str)

      rank = None
      space_type = None

      if space_domain is not None:
        if isinstance(space_domain, lue_points.Points):
          space_type = lue.SpaceDomainItemType.point
          rank = 2
        else:
          space_type = lue.SpaceDomainItemType.box
          rank = 2

        if not space_domain.mobile:
          space_configuration = lue.SpaceConfiguration(
          lue.Mobility.stationary,
          space_type
          )
        else:
          raise NotImplementedError



      # FAME
      self._space_domain = space_domain
      self._time_domain = time_domain

      p = fame_pset.PropertySet(self._nr_objects)
      p.__name__ = pset_name
      p._lue_dataset_name = self._lue_dataset_name
      p._lue_dataset = self._lue_dataset
      p._lue_phenomenon_name = self.__name__
      p.set_space_domain('locationdfg', space_domain)
      self._property_sets.add(p)

      # LUE

      lue_time_domain = self._lue_dataset.phenomena['framework'].property_sets['fame_time_cell'].time_domain

      #self._lue_dataset.phenomena[self.__name__].add_property_set(pset_name, time_domain.configuration, time_domain.clock)

      tmp_pset = self._lue_dataset.phenomena[self.__name__].add_property_set(pset_name, lue_time_domain, space_configuration, numpy.dtype(numpy.float64), rank=rank)

      #ids = self._lue_dataset.phenomena[self.__name__].object_id
      nr_timesteps = lue_time_domain.value[0][1]


      # Assign coordinates
      if space_type == lue.SpaceDomainItemType.point:

        tmp_location = self._lue_dataset.phenomena[self.__name__].property_sets[pset_name]

        # Index of active set (we only use one...)
        tmp_location.object_tracker.active_set_index.expand(nr_timesteps)[-1] = 0

        # IDs of the active objects of current time cell.
        tmp_location.object_tracker.active_object_id.expand(self._nr_objects)[-self._nr_objects:] = self._object_ids
        #tmp_location.object_tracker.active_object_id.expand(nr_timesteps)[-nr_timesteps:] = self._object_ids

        space_coordinate_dtype = tmp_location.space_domain.value.dtype

        tmp_values = numpy.ones((self._nr_objects, 2), dtype=tmp_location.space_domain.value.dtype)

        for idx, item in enumerate(space_domain):
          tmp_values[idx, 0] = item[0]
          tmp_values[idx, 1] = item[1]

        tmp_location.space_domain.value.expand(self._nr_objects)[-self._nr_objects:] = tmp_values


      elif space_type == lue.SpaceDomainItemType.box:

        tmp_location = self._lue_dataset.phenomena[self.__name__].property_sets[pset_name]

        # Index of active set (we only use one...)
        tmp_location.object_tracker.active_set_index.expand(1)[-1] = 0

        # IDs of the active objects of current time cell.
        tmp_location.object_tracker.active_object_id.expand(self._nr_objects)[-self._nr_objects:] = self._object_ids

        space_coordinate_dtype = tmp_location.space_domain.value.dtype

        tmp_values = numpy.zeros((self._nr_objects, 4), dtype=tmp_location.space_domain.value.dtype)

        for idx, item in enumerate(space_domain):
          tmp_values[idx, 0] = item[0]
          tmp_values[idx, 1] = item[1]
          tmp_values[idx, 2] = item[2]
          tmp_values[idx, 3] = item[3]

        tmp_location.space_domain.value.expand(self._nr_objects)[-self._nr_objects:] = tmp_values

      else:
        raise NotImplementedError

      lue.assert_is_valid(self._lue_dataset_name)



    @property
    def nr_objects(self):
      return self._nr_objects

    @property
    def time_domain(self):
      return self._time_domain

    @property
    def object_ids(self):
      return self._object_ids

