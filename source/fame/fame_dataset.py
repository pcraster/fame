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

      self.lue_filename = None
      self.lue_dataset = None
      #self.lue_epoch = None
      self._lue_clock = None
      self.lue_time_extent = None



      self._phenomena = set()



      self._first_timestep = None
      self._last_timestep = None
      self._nr_timesteps = None

      self._set_timesteps(first_timestep, last_timestep)



      if self._nr_timesteps > 1:
          epoch = lue.Epoch(lue.Epoch.Kind.common_era)

          self._lue_clock = lue.Clock(epoch, lue.Unit.day, self._nr_timesteps)
      else:
        raise NotImplementedError

    @property
    def lue_clock(self):
      return self._lue_clock

    def _set_timesteps(self, first_timestep, last_timestep):
      assert first_timestep > 0
      assert last_timestep > 0
      assert last_timestep >= first_timestep

      self._first_timestep = first_timestep
      self._last_timestep = last_timestep
      self._nr_timesteps = last_timestep - first_timestep + 1





    def add_phenomenon(self, phen_name, nr_objects):

      # FAME
      if not isinstance(phen_name, str):
        raise NotImplementedError

      p = Phenomenon(nr_objects)
      p.__name__ = phen_name
      p._lue_dataset = self.lue_dataset
      p._lue_dataset_name = self.lue_filename
      p._nr_timesteps = self._nr_timesteps
      self._phenomena.add(p)

      # LUE
      self.lue_dataset.add_phenomenon(phen_name)
      tmp = self.lue_dataset.phenomena[phen_name]
      tmp.object_id.expand(p.nr_objects)[:] = p.object_ids

      self.lue_time_extent = tmp.add_property_set(
              "fame_time_extent",
              lue.TimeConfiguration(lue.TimeDomainItemType.cell), self.lue_clock)


      assert lue.validate(self.lue_filename)

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




