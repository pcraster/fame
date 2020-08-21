import numbers
import os
import numpy as np
#import copy

#from .luemem_values import *

import fame.luemem_values as fame_values

class Property(object):
    def __init__(self, pset, shapes, pset_uuid, pset_domain, time_discretisation):

        self._pset = pset

        self._name = None

        self._is_agent = None

        self.pset_domain = pset_domain

        #self._values = None
        self._shape = shapes
        self._dtype = None

        self.nr_objects = self._pset

        self._lue_dataset  = None
        self._lue_phen_name = None
        self._lue_pset_name = None

        self._pset_uuid = pset_uuid
        self._values = fame_values.Values2(self._pset, self._shape, np.nan)


        self.time_discretisation = time_discretisation


    @property
    def pset_uuid(self):
      return self._pset_uuid

    @property
    def name(self):
      return self._name

    @name.setter
    def name(self, value):
      self._name = value

    @property
    def shapes(self):
      return self._shapes



    #@property
    def values(self):
      return self._values

    #@values.setter
    def set_values(self, values):

      #values = None

      #if isinstance(value, numbers.Number):
        #shape = (self._pset,)
        #values = numpy.full(shape, value)

      #elif isinstance(value, numpy.ndarray):
        #values = numpy.full(value.shape, value)
      #else:
        #raise NotImplementedError

      #assert values is not None
      #self._values = fame_values.Values(self._pset, values)
      self._values = fame_values.Values2(self._pset, self._shape, values)
      #raise SystemExit


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



    #def __repr__(self):
      ##print(self._values)
      #return ''


    #def __setattr__(self, name, value):
      #print('set property',name,value, type(value))
      #try:
        #getattr(self, name)
        #print('set property try ok',name,value, type(value))
        #super().__setattr__(name, value)
      #except AttributeError as e:
        #super().__setattr__(name, value)
      ##raise  SystemExit
      #print(self.__dict__)
