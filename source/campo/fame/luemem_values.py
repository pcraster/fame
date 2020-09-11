import numpy as np
from collections import OrderedDict

import campo.lue_property as lue_property




class Values(object):
  def __init__(self, nr_objects, values):

    self.iter_idx = 0

    self.values = values
    self.nr_objects = nr_objects



  def __iter__(self):
        return self

  def __next__(self):
        if self.iter_idx == self.nr_objects:
            raise StopIteration

        values = self.values[self.iter_idx]
        self.iter_idx += 1

        return values


  def __getitem__(self, index):
    try:
      idx = index[0]
    except Exception as e:
      idx = index
    if idx < 0 or idx > self.nr_objects:
      raise IndexError

    return self.values[index]


  def __setitem__(self, index, value):
    try:
      idx = index[0]
    except Exception as e:
      idx = index

    if idx < 0 or idx > self.nr_objects:
      raise IndexError

    self.values[index] = value



  def __repr__(self):
    for v in self.values:
      print(v)
    return ''






class Values2(object):

  def __init__(self, nr_objects, shapes, values):

    self.iter_idx = 0
    self.nr_objects = nr_objects

    self.values = OrderedDict()

    if isinstance(values, (int, float)):
      self._init_numbers(shapes, values)

    elif isinstance(values, np.ndarray):
      self._init_array(shapes, values)

    elif isinstance(values, lue_property.Property):
      self._init_prop(shapes, values)
    else:
      raise NotImplementedError


  def _init_array(self, shapes, values):

    for idx, shape in enumerate(shapes):
      self.values[idx] = values[idx]


  def _init_numbers(self, shapes, values):

    dim = len(shapes[0])


    for idx, shape in enumerate(shapes):
      tmp = None
      if dim == 0:
        tmp = np.array(values)
      elif dim == 1 or dim == 2:
        tmp = np.full(shape, values)
      else:
        raise NotImplementedError

      self.values[idx] = tmp


  def _init_prop(self, shapes, values):

    for idx, shape in enumerate(shapes):
      self.values[idx] = values.values().values[idx]





  def __setitem__(self, index, value):
    #try:
      #idx = index[0]
    #except Exception as e:
      #idx = index

    if index < 0 or index > self.nr_objects:
      raise IndexError

    self.values[index] = value


  def __getitem__(self, index):
    #try:
      #idx = index[0]
    #except Exception as e:
      #idx = index
    #if idx < 0 or idx > self.nr_objects:
      #raise IndexError

    return self.values[index]


  def __iter__(self):
        return self

  def __next__(self):
        if self.iter_idx == self.nr_objects:
            raise StopIteration

        values = self.values[self.iter_idx]
        self.iter_idx += 1

        return values
