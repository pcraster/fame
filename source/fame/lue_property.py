import numpy
import os





class Property(object):
    def __init__(self):

        self._name = None

        self._is_agent = None

        self.pset_domain = None



    @property
    def name(self):
      return self._name

    @name.setter
    def name(self, value):
      self._name = value






