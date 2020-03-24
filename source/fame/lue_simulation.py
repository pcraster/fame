import os


from .lue_phenomenon import *


class LueMemory(object):

    def __init__(self, filename, last_timestep, first_timestep=1, working_dir=os.getcwd()):

      self.filename = filename


      self.working_dir = working_dir

      self._phenomena = set()



      self._first_timestep = None
      self._last_timestep = None
      self._nr_timesteps = None

      self._set_timesteps(first_timestep, last_timestep)

    def _set_timesteps(self, first_timestep, last_timestep):
      assert first_timestep > 0
      assert last_timestep > 0
      assert last_timestep >= first_timestep

      self._first_timestep = first_timestep
      self._last_timestep = last_timestep
      self._nr_timesteps = last_timestep - first_timestep + 1





    def add_phenomenon(self, value, nr_objects):

      if not isinstance(value, str):
        raise NotImplementedError

      p = Phenomenon(nr_objects)
      p.__name__ = value
      self._phenomena.add(p)

      return p



    def __repr__(self):
      msg = 'Simulation with phenomena "{}"'.format(self._phenomena)
      return msg
