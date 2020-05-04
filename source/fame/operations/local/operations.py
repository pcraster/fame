import copy
import numpy

import fame


def uniform(pset, lower=0.0, upper=1.0):
  """ Returns uniform value for each object """
  if not isinstance(pset, fame.lue_propertyset.PropertySet):
    raise NotImplementedError

  tmp_prop = fame.lue_property.Property(pset._phen)
  tmp_prop.values = numpy.random.uniform(lower, upper, (pset.nr_objects(),))

  return numpy.random.uniform(lower, upper, (pset.nr_objects(),))
