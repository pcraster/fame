import numbers
import os
import numpy

from .luemem_values import *


class Property(object):
    def __init__(self, pset):

        self._pset = pset

        self._name = None

        self._is_agent = None

        self.pset_domain = None

        self._values = None
        self._shape = None
        self._dtype = None

        self.nr_objects = self._pset



    @property
    def name(self):
      return self._name

    @name.setter
    def name(self, value):
      self._name = value




    @property
    def values(self):
      return self._values

    @values.setter
    def values(self, value):


      values = None

      if isinstance(value, numbers.Number):
        shape = (self._pset,) #._nr_objects(),)
        values = numpy.full(shape, value)

      elif isinstance(value, numpy.ndarray):
        values = numpy.full(value.shape, value)
      else:
        raise NotImplementedError

      assert values is not None
      self._values = Values(self._pset, values)


    @property
    def shape(self):
      return self._shape

    @shape.setter
    def shape(self, value):
      self._shape = value

    @property
    def dtype(self):
      return self._dtype

    @dtype.setter
    def dtype(self, value):
      self._dtype = value





    def assign(self, value):

      nr_objects = len(self.pset_domain)

      if isinstance(value, numbers.Number):

        self.values = numpy.full((nr_objects), value)
        self._dtype = self._values.dtype
      else:


        self.values = value

      self._dtype = self._values.dtype



    def __repr__(self):
      #print(self._values)
      return ''

