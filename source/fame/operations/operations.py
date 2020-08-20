import copy
import numpy
import os
import subprocess

import fame.lue_property as lue_property
import fame.lue_points as points
import fame.lue_areas as areas

#import pcraster


def pset_report(prop, filename, path, ts,name):

  csvname = os.path.join(path, 'tmp_{}_{:03d}.csv'.format(name, ts))

  with open(csvname, 'w') as content:
    for idx, p in enumerate(prop.pset_domain):
      row = '{},{},{}\n'.format(p[0],p[1], prop.values[idx])
      content.write(row)


  map_path = os.path.join(path, filename)
  cmd = 'col2map --nothing --clone houses.map {} {}'.format(csvname, map_path)
  subprocess.check_call(cmd, shell=True)









def agents_average(prop):
  """returns average value of property values """
  if not isinstance(prop, lue_property.Property):
    raise NotImplementedError

  if not isinstance(prop.pset_domain, points.Points):
    raise NotImplementedError

  tmp_prop = copy.deepcopy(prop)
  nr_objects = tmp_prop.nr_objects

  tmp = numpy.zeros(nr_objects)

  for i in range(0, nr_objects):
    tmp[i] = tmp_prop.values()[i]

  tmp_values = numpy.average(tmp)

  for i in range(0, nr_objects):
    tmp_prop.values()[i] = tmp_values

  return tmp_prop







def average(prop):
  if not isinstance(prop, lue_property.Property):
    raise NotImplementedError

  tmp_prop = copy.deepcopy(prop)

  for idx,i in enumerate(prop.values.values):
    tmp_prop.values[idx,...] = numpy.average(i)

  return tmp_prop

