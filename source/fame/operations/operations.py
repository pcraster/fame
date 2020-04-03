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
  tmp_prop = copy.deepcopy(self)

  for idx,i in enumerate(self.values.values):
    tmp_prop.values[idx,...] = numpy.abs(tmp_prop.values[idx])

  return tmp_prop


def lue_mul(self, something):


  tmp_prop = copy.deepcopy(self)


  if isinstance(something, lue_property.Property ):
    v = something.values
  else:
    raise NotImplementedError
    v = something

  for idx,i in enumerate(self.values.values):
    tmp_prop.values[idx,...] = tmp_prop.values[idx] * v[idx]


  return tmp_prop



def lue_rmul(self, number):
  tmp_prop = copy.deepcopy(self)


  for idx,i in enumerate(self.values.values):
    tmp_prop.values[idx,...] = tmp_prop.values[idx] * number

  return tmp_prop



def lue_sub(self, something):

  tmp_prop = copy.deepcopy(self)

  for idx,i in enumerate(self.values.values):
    tmp_prop.values[idx,...] = self.values[idx] - something.values[idx]

  return tmp_prop



def lue_rsub(self, number):

  tmp_prop = copy.deepcopy(self)


  for idx,i in enumerate(self.values.values):
    tmp_prop.values[idx,...] = number - tmp_prop.values[idx]

  return tmp_prop



def lue_add(self, something):


  tmp_prop = copy.deepcopy(self)

  if isinstance(something, lue_property.Property ):
    v =something.values
  else:
    raise NotImplementedError
    v = something

  for idx,i in enumerate(self.values.values):
    tmp_prop.values[idx,...] = self.values[idx] + v.values[idx]

  return tmp_prop


def lue_radd(self, number):

  return lue_add(self, number)

def lue_iadd(self, prop):

  if isinstance(prop, lue_property.Property ):
    v =prop.values
  else:
    raise NotImplementedError
    v = prop

  for idx,i in enumerate(self.values.values):
    self.values[idx,...] = self.values[idx] + v.values[idx]

  return self





def lue_neg(self):
  if not isinstance(prop, lue_property.Property):
    raise NotImplementedError




def average(prop):
  if not isinstance(prop, lue_property.Property):
    raise NotImplementedError

  tmp_prop = copy.deepcopy(prop)

  for idx,i in enumerate(prop.values.values):
    tmp_prop.values[idx,...] = numpy.average(i)

  return tmp_prop

lue_property.Property.__add__      = lue_add
lue_property.Property.__radd__      = lue_radd
#lue_property.Property.__iadd__      = lue_iadd



lue_property.Property.__sub__ = lue_sub
lue_property.Property.__rsub__ = lue_rsub


lue_property.Property.__mul__ = lue_mul
lue_property.Property.__rmul__  = lue_rmul



lue_property.Property.__neg__ = lue_neg
