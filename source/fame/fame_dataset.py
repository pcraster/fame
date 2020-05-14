import os
import numpy as np

try:
  import lue
except ModuleNotFoundError as e:
  print(e)
  msg = 'You can try to install the current development version like:\n'
  msg += 'conda install -c conda-forge -c http://pcraster.geo.uu.nl/pcraster/pcraster/ lue'
  raise SystemExit(msg)

import fame.lue_phenomenon as fame_phen







class LueMemory(object):

    def __init__(self, last_timestep, first_timestep=1):
      """ some text """

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
          # daily time steps
          self._lue_clock = lue.Clock(epoch, lue.Unit.day, 1)

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



    def add_framework(self):
      """ Adding a phenomenon holding framwork relevant information
          in a good case this can be shared between phenomena
      """

      # LUE
      self.lue_dataset.add_phenomenon('framework')
      tmp = self.lue_dataset.phenomena['framework']

      self.lue_time_extent = tmp.add_property_set(
              "fame_time_cell",
              lue.TimeConfiguration(lue.TimeDomainItemType.cell), self.lue_clock)

      # just a number, TODO sampleNumber?
      simulation_id = 1

      # dynamic...
      time_cell = tmp.property_sets["fame_time_cell"]

      # add one timstep, 0=inital, 1...T=timesteps
      timesteps = self._nr_timesteps + 1

      time_cell.object_tracker.active_set_index.expand(timesteps) \
        [-timesteps:] = np.arange(0, timesteps, dtype=np.dtype(np.uint64))

      time_cell.object_tracker.active_object_id.expand(timesteps) \
        [-timesteps:] = np.full(timesteps, simulation_id, dtype=lue.dtype.ID)

      time_cell.time_domain.value.count.expand(1)[-1] = timesteps
      time_cell.time_domain.value.expand(1)[-1] = np.array([0, timesteps], dtype=lue.dtype.TickPeriodCount).reshape(1, 2)


      # We create one time cell with nr of timesteps (dynamic)
#      self.lue_time_extent = tmp.add_property_set(
#              "fame_time_extent",
#              lue.TimeConfiguration(lue.TimeDomainItemType.cell), self.lue_clock)

      #self.lue_time_extent = tmp.add_property_set(
              #"fame_time_cell",
              #lue.TimeConfiguration(lue.TimeDomainItemType.cell), self.lue_clock)

      # We create one time box (static)
#      self.lue_time_extent = tmp.add_property_set(
#              "fame_time_box",
#              lue.TimeConfiguration(lue.TimeDomainItemType.box), lue.Clock(lue.Epoch(lue.Epoch.Kind.common_era), lue.Unit.day, self._nr_timesteps))

      # Discretisation



      # static...

#      time_cell = tmp.property_sets["fame_time_box"]
#      time_cell.object_tracker.active_set_index.expand(1)[-1:] = 0
#      time_cell.object_tracker.active_object_id.expand(1)[-1:] = simulation_id
#      time_cell.time_domain.value.expand(1)[-1] = np.array([0, self._nr_timesteps], dtype=lue.dtype.TickPeriodCount).reshape(1, 2)

      lue.assert_is_valid(self.lue_filename)


    def add_phenomenon(self, phen_name, nr_objects):
      """ Adding a phenomenon """

      # FAME
      if not isinstance(phen_name, str):
        raise NotImplementedError

      p = fame_phen.Phenomenon(nr_objects)
      p.__name__ = phen_name
      p._lue_dataset = self.lue_dataset
      p._lue_dataset_name = self.lue_filename
      p._nr_timesteps = self._nr_timesteps
      self._phenomena.add(p)

      # LUE
      self.lue_dataset.add_phenomenon(phen_name)
      tmp = self.lue_dataset.phenomena[phen_name]
      tmp.object_id.expand(p.nr_objects)[:] = p.object_ids


      lue.assert_is_valid(self.lue_filename)

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


      self.add_framework()

      lue.assert_is_valid(self.lue_filename)




