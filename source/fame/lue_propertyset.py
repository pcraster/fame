import fame.lue_points as lue_points
import fame.lue_areas as lue_areas
import fame.lue_property as lue_property




class PropertySet(object):

    def __init__(self, phen, space_domain=None, time_domain=None):

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


    def _nr_objects(self):
      return self._phen



    def __len__(self):
      return len(self._properties)





    def __getattr__(self, property_name):
      result = None
      for p in self._properties:
        if p.__name__ == property_name:
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


    def add_property(self, value):

      assert isinstance(value, str)

      p = lue_property.Property(self._phen)
      p.__name__ = value
      p.pset_domain = self._domain

      self._properties.add(p)
