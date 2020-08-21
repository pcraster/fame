import numpy as np
import uuid

import lue.data_model as ldm


import fame.lue_points as lue_points
import fame.lue_areas as lue_areas
import fame.lue_property as lue_property
import fame.lue_phenomenon as fame_phen
import fame.luemem_values as fame_values

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

      self._uuid = uuid.uuid4()
      self.shapes = None

      self.time_discretisation = None


    @property
    def uuid(self):
      return self._uuid

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
      try:
        for p in self._properties:
          if p.name == property_name:
            result = p

        return result
      except Exception:
        pass



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


    def add_property(self, property_name, dtype=np.float64, time_discretisation=TimeDiscretization.dynamic, rank=None, shape=None):

      assert isinstance(property_name, str)
      assert self._lue_dataset_name is not None

      self.time_discretisation = time_discretisation


      # FAME
      self.shapes = None
      if isinstance(self._domain, lue_points.Points):
        if rank == None:
          self.shapes = [()] * self._phen
        elif rank != None and shape != None:
          self.shapes = [shape] * self._phen
        else:
          raise NotImplementedError
      elif isinstance(self._domain, lue_areas.Areas):
        self.shapes = [(int(self._domain.row_discr[i]), int(self._domain.col_discr[i])) for i in range(len(self._domain.row_discr))]
      else:
        raise NotImplementedError


      p = lue_property.Property(self._phen, self.shapes, self._uuid, self._domain, self.time_discretisation)
      p.name = property_name

      p._lue_pset_name = self.__name__

      self._properties.add(p)

      # LUE

      nr_timesteps = int(self._lue_dataset.phenomena['framework'].property_sets['fame_time_cell'].time_domain.value[0][1])

      pset = self._lue_dataset.phenomena[self._lue_phenomenon_name].property_sets[self.__name__]

      if isinstance(p.pset_domain, lue_points.Points):

        if self.time_discretisation == TimeDiscretization.dynamic:
          p_shape = ()
          prop = pset.add_property(property_name, dtype=np.dtype(dtype), shape=p_shape, value_variability=ldm.ValueVariability.variable)
          prop.value.expand(self.nr_objects() * nr_timesteps)
        else:
          prop = pset.add_property(property_name, dtype=np.dtype(dtype))
          prop.value.expand(self.nr_objects())

      elif isinstance(p.pset_domain, lue_areas.Areas):

        # all same shape...
        #p_shape = (p.pset_domain.row_discr[0], p.pset_domain.col_discr[0])
        #p_shape = (2,1)
        #prop = pset.add_property(property_name, dtype=np.dtype(dtype), shape=p_shape, value_variability=lue.ValueVariability.variable)
        prop = pset.add_property(property_name, dtype=np.dtype(dtype), rank=2,
            shape_per_object=ldm.ShapePerObject.different,
            shape_variability=ldm.ShapeVariability.constant)
         #                        )#shape=p_shape, value_variability=lue.ValueVariability.variable)
        #prop.value.expand(self.nr_objects() * nr_timesteps)

        space_discr = pset.fame_discretization

        for idx, item in enumerate(p.pset_domain):
          space_discr.value[idx]= [item[4], item[5]]
          #prop.value.expand(idx, item, nr_timesteps)


        prop.set_space_discretization(
            ldm.SpaceDiscretization.regular_grid,
            space_discr)
        #prop.value.expand(self.nr_objects())


        for idx, item in enumerate(p.pset_domain):
          #space_discr.value[idx]= [item[0], item[1]]
          #print(idx, item, nr_timesteps)
          prop.value.expand(idx, tuple([nr_timesteps, item[4], item[5]]), self.nr_objects())#nr_timesteps)#self.nr_objects())#nr_timesteps)

        # all different shape
        #space_rank = 2
        #prop = pset.add_property(property_name, dtype=np.dtype(dtype), rank=space_rank,
            #shape_per_object=lue.ShapePerObject.different,
            #shape_variability=lue.ShapeVariability.constant)


      else:
        raise NotImplementedError

      ldm.assert_is_valid(self._lue_dataset_name)



    def write(self, timestep):
        # write ts 0 initial
        # 1..T dynamic


        lue_pset = self._lue_dataset.phenomena[self._lue_phenomenon_name].property_sets[self.__name__]
        nr_objects = len(self._lue_dataset.phenomena[self._lue_phenomenon_name].object_id[:])

        # Static data...
        if timestep == 0:

          for prop in self._properties:
            if prop.time_discretisation == TimeDiscretization.static:
              lue_prop = lue_pset.properties[prop.name]
              for idx, val in enumerate(prop.values().values):
                lue_prop.value[idx] = prop.values().values[idx]
            if prop.time_discretisation == TimeDiscretization.dynamic:
              if prop.name != 'neighboured_houses' and prop.name != 'neighboured_foodstores' and prop.name != 'social_neighbours':
                lue_prop = lue_pset.properties[prop.name]
                for idx, val in enumerate(prop.values().values):
                  lue_prop.value[idx] = prop.values().values[idx]


        #if timestep is not None:
        # Dynamic data...
        else:
          # Determine current time slice to write
          sidx = int(lue_pset.object_tracker.active_set_index[timestep])
          eidx = sidx + nr_objects

          for prop in self._properties:
            # TODO
            if prop.name != 'neighboured_houses' and prop.name != 'neighboured_foodstores' and prop.name != 'social_neighbours':
                lue_prop = lue_pset.properties[prop.name]
                #lue_prop.value[sidx:eidx] = prop.values.values
                #lue_prop.value[sidx:eidx] = prop.values().values[0]
                for idx, val in enumerate(prop.values().values):
                  lue_prop.value[sidx + idx] = prop.values().values[idx]

        #else:
          # in initial...
        #  raise NotImplementedError

        #lue.assert_is_valid(self._lue_dataset_name)


    def __setattr__(self, name, value):
      try:
        attr = getattr(self, name)
        if not isinstance(attr, lue_property.Property):
          super().__setattr__(name, value)
        else:
          if not isinstance(value, lue_property.Property):
            attr.set_values(value)
          else:
            #super().__setattr__(name, value)
            attr.set_values(value)
      except AttributeError as e:
        super().__setattr__(name, value)


