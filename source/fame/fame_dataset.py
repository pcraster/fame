import os

try:
  import lue
except ModuleNotFoundError as e:
  print(e)
  msg = 'You can try to install the current development version like:\n'
  msg += 'conda install -c conda-forge -c http://pcraster.geo.uu.nl/pcraster/pcraster/ lue'
  raise SystemExit(msg)

from .lue_phenomenon import *


class LueMemory(object):

    def __init__(self, last_timestep, first_timestep=1):

      self.lue_filname = None
      self.lue_dataset = None



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


    def open(self, filename, working_dir=os.getcwd()):
      fpath = os.path.join(working_dir, filename)

      root, ext = os.path.splitext(fpath)
      if ext == '':
        fpath += '.lue'

      if os.path.exists(filename):
        raise NotImplementedError('opening existing not yet supported')

      self.lue_filename = fpath
      self.lue_dataset = lue.create_dataset(self.lue_filename)

      assert lue.validate(self.lue_filename)
