import copy
import numpy

import fame

import fame.lue_points as points
import fame.lue_areas as areas


def uniform(property_set, lower=0.0, upper=1.0):
  """ Returns uniform value for each object. Can be applied to fields and objects.

  :param property_set: Property set
  :type arg1: PropertySet
  :param lower: lower boundary
  :type arg2: number
  :param upper: upper boundary
  :type arg2: number
  :returns: a property with summed values
  :rtype: Property
  """
  if not isinstance(property_set, fame.lue_propertyset.PropertySet):
    raise NotImplementedError

  if isinstance(property_set._space_domain, points.Points):
    values = numpy.random.uniform(lower, upper, (property_set.nr_objects(),))
  elif isinstance(property_set._space_domain, areas.Areas):
    p_shape = (property_set._space_domain.row_discr[0], property_set._space_domain.col_discr[0])
    values = numpy.random.uniform(lower, upper, (property_set.nr_objects(), int(property_set._space_domain.row_discr[0]), int(property_set._space_domain.col_discr[0])))

  tmp_prop = fame.lue_property.Property(property_set._phen)
  tmp_prop.values = values

  return values
