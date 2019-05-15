import fame.lue_points as lue_points
import fame.lue_areas as lue_areas
import fame.lue_property as lue_property





class PropertySet(object):

    def __init__(self):

      self._properties = set()

      self.__name__ = None

      self.__dict__['domain'] = None


    def __len__(self):
      return len(self._properties)



    def __setattr__(self, name, value):



        if name == '__name__':
          self.__dict__[name] = value

        elif name == 'domain':
          assert isinstance(value, lue_points.Points) or isinstance(value, lue_areas.Areas)

          self.__dict__[name] = value

        elif isinstance(value, lue_property.Property):

          if hasattr(self, 'domain'):
            value.pset_domain = self.domain

          value.name = name
          self.__dict__[name] = value


    def __getattr__(self, property_set_name):
      pass



    def __repr__(self):
      msg = 'Property set "{}" with domain "{}" and properties "{}"'.format(self.__name__, self.domain, self._properties)
      return msg
