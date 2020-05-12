import copy
import numpy
import os
import subprocess

import fame.lue_property as lue_property

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









def property_average(prop):
  if not isinstance(prop, lue_property.Property):
    raise NotImplementedError


  tmp_prop = copy.deepcopy(prop)

  tmp_values = numpy.average(prop.values.values)

  for idx,i in enumerate(prop.values.values):
    tmp_prop.values[idx,...] = tmp_values

  return tmp_prop



def abs(self):
  """ """
  tmp_prop = copy.deepcopy(self)

  for idx,i in enumerate(self.values.values):
    tmp_prop.values[idx,...] = numpy.abs(tmp_prop.values[idx])

  return tmp_prop





def average(prop):
  if not isinstance(prop, lue_property.Property):
    raise NotImplementedError

  tmp_prop = copy.deepcopy(prop)

  for idx,i in enumerate(prop.values.values):
    tmp_prop.values[idx,...] = numpy.average(i)

  return tmp_prop

