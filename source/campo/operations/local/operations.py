import copy
import numpy

import campo

import campo.lue_points as points
import campo.lue_areas as areas



def uniform(lower, upper, seed=0):
  """ Returns uniform value for each object. Can be applied to fields and objects.

  :param lower: lower boundary
  :type Property: number or Property from the same property set
  :param upper: upper boundary
  :type Property: number or Property from the same property set
  :param seed: random seed (default 0)
  :type int
  :returns: a property with summed values
  :rtype: Property
  """
  if not isinstance(lower, campo.lue_property.Property):
    raise ValueError

  if not isinstance(upper, campo.lue_property.Property):
    raise ValueError

  if lower.pset_uuid != upper.pset_uuid:
      msg = 'Property "{}" and property "{}" are not from the same PropertySet '.format(lower.name, upper.name)
      raise ValueError(msg)

  tmp_prop = campo.lue_property.Property('emptyuniformname', lower.pset_uuid, lower.space_domain, lower.shapes)


  for idx in range(lower.nr_objects):
    values = None
    if isinstance(lower.space_domain, points.Points):
      if seed != 0:
        numpy.random.seed(seed + idx)
      values = numpy.random.uniform(lower.values()[idx], upper.values()[idx])
    elif isinstance(lower.space_domain, areas.Areas):
      if seed != 0:
        numpy.random.seed(seed + idx)
      values = numpy.random.uniform(lower.values()[idx], upper.values()[idx], (int(lower.space_domain.row_discr[idx]), int(lower.space_domain.col_discr[idx])))
    else:
      raise NotImplementedError

    tmp_prop.values()[idx] = values


  return tmp_prop









def uniform2(property_set, lower=0.0, upper=1.0, seed=0):
  """ Returns uniform value for each object. Can be applied to fields and objects.

  :param property_set: Property set
  :type arg1: PropertySet
  :param lower: lower boundary
  :type arg2: number or Property from the same property set
  :param upper: upper boundary
  :type arg2: number or Property from the same property set
  :returns: a property with summed values
  :rtype: Property
  """
  if not isinstance(property_set, campo.lue_propertyset.PropertySet):
    raise NotImplementedError

  nr_objects = property_set.nr_objects()

  lower_values = None
  upper_values = None

  if isinstance(lower, campo.lue_property.Property):
    if property_set.uuid != lower.pset_uuid:
      msg = 'Property "{}" is not part of the PropertySet "{}"'.format(lower.name, property_set.__name__)
      raise TypeError(msg)

    lower_values = lower.values()

  if isinstance(lower, (int, float)):
    lower_values = numpy.full(nr_objects, lower)


  if isinstance(upper, campo.lue_property.Property):
    if property_set.uuid != upper.pset_uuid:
      msg = 'Property "{}" is not part of the PropertySet "{}"'.format(upper.name, property_set.__name__)
      raise TypeError(msg)

    upper_values = upper.values()

  if isinstance(upper, (int, float)):
    upper_values = numpy.full(nr_objects, upper)

  #if isinstance(property_set._space_domain, points.Points):
    #values = numpy.random.uniform(lower, upper, (property_set.nr_objects(),))
  #elif isinstance(property_set._space_domain, areas.Areas):
    #p_shape = (property_set._space_domain.row_discr[0], property_set._space_domain.col_discr[0])
    #values = numpy.random.uniform(lower, upper, (property_set.nr_objects(), int(property_set._space_domain.row_discr[0]), int(property_set._space_domain.col_discr[0])))


  tmp_prop = campo.lue_property.Property(property_set._phen, property_set.shapes, property_set.uuid, property_set._domain, property_set.time_discretization)


  for idx in range(nr_objects): #self.values()):
    values = None
    if isinstance(property_set._space_domain, points.Points):
      if seed != 0:
        numpy.random.seed(seed + idx)
      values = numpy.random.uniform(lower_values[idx], upper_values[idx])
    elif isinstance(property_set._space_domain, areas.Areas):
      #values = numpy.random.uniform(lower_values[idx], upper_values[idx], (property_set.nr_objects(), int(property_set._space_domain.row_discr[idx]), int(property_set._space_domain.col_discr[idx])))
      if seed != 0:
        numpy.random.seed(seed + idx)
      values = numpy.random.uniform(lower_values[idx], upper_values[idx], (int(property_set._space_domain.row_discr[idx]), int(property_set._space_domain.col_discr[idx])))
    else:
      raise NotImplementedError

    tmp_prop.values()[idx] = values

  return tmp_prop
