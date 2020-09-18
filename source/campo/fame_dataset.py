import os
import numpy as np
import datetime

try:
  import lue
  import lue.data_model as ldm
  import campo.lue_points as lue_points
  import campo.lue_areas as lue_areas
except ModuleNotFoundError as e:
  print(e)
  msg = 'You can try to install the current development version like:\n'
  msg += 'conda install -c conda-forge -c http://pcraster.geo.uu.nl/pcraster/pcraster/ lue'
  raise SystemExit(msg)

import campo.lue_phenomenon as fame_phen







class LueMemory(object):

    def __init__(self):
      """ some text """

      self._phenomena = {}
      self._nr_timesteps = None
      self._lue_clock = None
      self._lue_time_configuration = None


      #self.lue_filename = None
      #self.lue_dataset = None
      ##self.lue_epoch = None
      #self._lue_clock = None
      #self.lue_time_extent = None
      #self.timeset = False




      #self._phenomena = set()



      #self._first_timestep = None
      #self._last_timestep = None
      #self._nr_timesteps = None

      ###self._set_timesteps(first_timestep, last_timestep)

      ###start_timestep = start_timestep.isoformat()

      ###if self._nr_timesteps > 1:
          ###epoch = ldm.Epoch(ldm.Epoch.Kind.common_era, start_timestep, ldm.Calendar.gregorian)
          ###self._lue_clock = ldm.Clock(epoch, unit.value, stepsize)
      ###else:
        ###raise NotImplementedError


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



    def add_framework(self, nr_objects):
      """ Adding a phenomenon holding framwork relevant information
          in a good case this can be shared between phenomena
      """

      # LUE
      self.lue_dataset.add_phenomenon('framework')
      tmp = self.lue_dataset.phenomena['framework']

      self.lue_time_extent = tmp.add_property_set(
              "fame_time_cell",
              ldm.TimeConfiguration(ldm.TimeDomainItemType.box), self.lue_clock)

      # just a number, TODO sampleNumber?
      simulation_id = 1

      # dynamic...
      time_cell = tmp.property_sets["fame_time_cell"]

      time_boxes = 1

      #time_cell.object_tracker.active_object_id.expand(time_boxes * nr_objects)[:] = np.arange(0, nr_objects, dtype=np.dtype(np.uint64))

      #time_cell.object_tracker.active_object_index.expand(time_boxes * nr_objects)[:] = list(np.zeros(nr_objects, dtype=np.dtype(np.uint64)))

      time_cell.object_tracker.active_set_index.expand(time_boxes)[:] = 0

      #time_domain = point_pset.time_domain
      time_cell.time_domain.value.expand(time_boxes)[:] = [0, self._nr_timesteps]


      ###### add one timstep, 0=inital, 1...T=timesteps
      #####timesteps = self._nr_timesteps + 1

      #####time_cell.object_tracker.active_set_index.expand(timesteps) \
        #####[-timesteps:] = np.arange(0, timesteps, dtype=np.dtype(np.uint64))

      #####time_cell.object_tracker.active_object_id.expand(timesteps) \
        #####[-timesteps:] = np.full(timesteps, simulation_id, dtype=ldm.dtype.ID)

      #####time_cell.time_domain.value.count.expand(1)[-1] = timesteps
      #####time_cell.time_domain.value.expand(1)[-1] = np.array([0, timesteps], dtype=ldm.dtype.TickPeriodCount).reshape(1, 2)




      # We create one time cell with nr of timesteps (dynamic)
#      self.lue_time_extent = tmp.add_property_set(
#              "fame_time_extent",
#              ldm.TimeConfiguration(ldm.TimeDomainItemType.cell), self.lue_clock)

      #self.lue_time_extent = tmp.add_property_set(
              #"fame_time_cell",
              #ldm.TimeConfiguration(ldm.TimeDomainItemType.cell), self.lue_clock)

      # We create one time box (static)
#      self.lue_time_extent = tmp.add_property_set(
#              "fame_time_box",
#              ldm.TimeConfiguration(ldm.TimeDomainItemType.box), ldm.Clock(ldm.Epoch(ldm.Epoch.Kind.common_era), ldm.Unit.day, self._nr_timesteps))

      # Discretisation



      # static...

#      time_cell = tmp.property_sets["fame_time_box"]
#      time_cell.object_tracker.active_set_index.expand(1)[-1:] = 0
#      time_cell.object_tracker.active_object_id.expand(1)[-1:] = simulation_id
#      time_cell.time_domain.valdm.expand(1)[-1] = np.array([0, self._nr_timesteps], dtype=ldm.dtype.TickPeriodCount).reshape(1, 2)

      ldm.assert_is_valid(self.lue_filename)



    def add_phenomenon(self, phen_name):

      if phen_name in self._phenomena:
        msg = "'{}' is already present as phenomenon name".format(phen_name)
        raise ValueError(msg)

      phen = fame_phen.Phenomenon(phen_name)
      self._phenomena[phen_name] = phen

      return phen


    def add_phenomenon2(self, phen_name, nr_objects):
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


      if self.timeset == False:
        self.add_framework(p.nr_objects)
        self.timeset = True

      ldm.assert_is_valid(self.lue_filename)



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
      self.lue_dataset = ldm.create_dataset(self.lue_filename)



      ldm.assert_is_valid(self.lue_filename)



    def create_dataset(self, filename, working_dir=os.getcwd()):
      fpath = os.path.join(working_dir, filename)

      root, ext = os.path.splitext(fpath)
      if ext == '':
        fpath += '.lue'

      if os.path.exists(filename):
        os.remove(filename)
        #raise FileExistsError("'{}' already exists".format(filename))

      self.lue_filename = fpath

      self.lue_dataset = ldm.create_dataset(self.lue_filename)
      ldm.assert_is_valid(self.lue_filename)



    def _generate_lue_property(self, phen_name, property_set, prop):

      pset = self.lue_dataset.phenomena[phen_name].property_sets[property_set.name]

      dtype = prop.values().values[0].dtype

      nr_objects = prop.nr_objects

      if isinstance(property_set.space_domain, lue_points.Points):

        if prop.is_dynamic:
          time_boxes = 1
          p_shape = (self._nr_timesteps,)
          lue_prop = pset.add_property(prop.name, dtype=np.dtype(dtype), shape=p_shape, value_variability=ldm.ValueVariability.variable)
          lue_prop.value.expand(nr_objects)


          pset.object_tracker.active_object_id.expand(time_boxes * nr_objects)[:] = self.lue_dataset.phenomena[phen_name].object_id[:]
          pset.object_tracker.active_set_index.expand(time_boxes)[:] = 0
######          pset.object_tracker.active_object_index.expand(time_boxes * nr_objects)[:] = [0] * nr_objects


          time_domain = pset.time_domain
          time_domain.value.expand(time_boxes)[:] = [0, self._nr_timesteps]

        else:
          lue_prop = pset.add_property(prop.name, dtype=np.dtype(dtype))
          lue_prop.value.expand(nr_objects)


      elif isinstance(property_set.space_domain, lue_areas.Areas):

        if prop.is_dynamic:
          lue_prop = pset.add_property(prop.name, dtype=np.dtype(dtype), rank=2,
            shape_per_object=ldm.ShapePerObject.different,
            shape_variability=ldm.ShapeVariability.constant)
        else:
          # Same shape
          # prop = pset.add_property(property_name, dtype=np.dtype(dtype), shape=shape)

          # Different shape
          lue_prop = pset.add_property(prop.name, dtype=np.dtype(dtype), rank=2)
            #shape_per_object=ldm.ShapePerObject.different,
            #shape_variability=ldm.ShapeVariability.constant)


        space_discr = pset.fame_discretization

        for idx, item in enumerate(property_set.space_domain):
          space_discr.value[idx]= [item[4], item[5]]


        lue_prop.set_space_discretization(
            ldm.SpaceDiscretization.regular_grid,
            space_discr)

        rank = 2
        if prop.is_dynamic:
          for idx, item in enumerate(property_set.space_domain):
            prop.value.expand(idx, tuple([item[4], item[5]]), nr_timesteps)
        else:
          shapes = np.zeros(nr_objects * rank, dtype=ldm.dtype.Count).reshape(nr_objects, rank)

          for idx, item in enumerate(property_set.space_domain):
            shapes[idx][0] = item[4]
            shapes[idx][1] = item[5]

          lue_prop.value.expand(self.lue_dataset.phenomena[phen_name].object_id[:], shapes)

      else:
        raise NotImplementedError


      ldm.assert_is_valid(self.lue_filename)


    def _generate_lue_property_set(self, phen_name, property_set):

      rank = -1
      space_type = None
      space_configuration = None
      static = False
      if self._lue_time_configuration is None:
        static = True

      if isinstance(property_set.space_domain, lue_points.Points):
          space_type = ldm.SpaceDomainItemType.point
          rank = 2
      else:
          space_type = ldm.SpaceDomainItemType.box
          rank = 2

        #if not space_domain.mobile:
      space_configuration = ldm.SpaceConfiguration(
          ldm.Mobility.stationary,
          space_type
          )
        #else:
        #  raise NotImplementedError

      if static:
        tmp_pset = self.lue_dataset.phenomena[phen_name].add_property_set(property_set.name, space_configuration, np.dtype(np.float64), rank=rank)
      else:
        tmp_pset = self.lue_dataset.phenomena[phen_name].add_property_set(property_set.name, self._lue_time_configuration, self._lue_clock, space_configuration, np.dtype(np.float64), rank=rank)

      tmp_pset = self.lue_dataset.phenomena[phen_name].property_sets[property_set.name]


      # Assign coordinates
      if space_type == ldm.SpaceDomainItemType.point:

        space_coordinate_dtype = tmp_pset.space_domain.value.dtype

        tmp_values = np.ones((property_set.nr_objects, 2), dtype=tmp_pset.space_domain.value.dtype)

        for idx, item in enumerate(property_set.space_domain):
          tmp_values[idx, 0] = item[0]
          tmp_values[idx, 1] = item[1]
        tmp_pset.space_domain.value.expand(property_set.nr_objects)[-property_set.nr_objects:] = tmp_values


      elif space_type == ldm.SpaceDomainItemType.box:

        space_coordinate_dtype = tmp_pset.space_domain.value.dtype

        tmp_values = np.zeros((property_set.nr_objects, 4), dtype=tmp_pset.space_domain.value.dtype)

        for idx, item in enumerate(property_set.space_domain):
          tmp_values[idx, 0] = item[0]
          tmp_values[idx, 1] = item[1]
          tmp_values[idx, 2] = item[2]
          tmp_values[idx, 3] = item[3]

        tmp_pset.space_domain.value.expand(property_set.nr_objects)[-property_set.nr_objects:] = tmp_values

        # For fields we also add a discretisation property
       # tmp_prop = tmp_location.add_property('fame_discretization', dtype=np.dtype(np.int64), shape=(1,2), value_variability=lue.ValueVariability.constant)
       # tmp_prop.value.expand(self._nr_objects)
       # for idx, item in enumerate(space_domain):
       #   tmp_prop.value[idx]= [item[4], item[5]]

        tmp_prop = tmp_pset.add_property('fame_discretization', dtype=ldm.dtype.Count, shape=(2,))
        tmp_prop.value.expand(property_set.nr_objects)



      else:
        raise NotImplementedError




      ## static fttb
      #if static:
      for prop in property_set.properties.values():
        self._generate_lue_property(phen_name, property_set, prop)
      #else:



      ldm.assert_is_valid(self.lue_filename)


    def _generate_lue_phenomenon(self,  phenomenon):
      pset = next(iter(phenomenon.property_sets.values()))

      nr_objects = pset.nr_objects


      self.lue_dataset.add_phenomenon(phenomenon.name)
      tmp = self.lue_dataset.phenomena[phenomenon.name]
      tmp.object_id.expand(nr_objects)[:] = np.arange(nr_objects, dtype=ldm.dtype.ID)

      for p in phenomenon.property_sets.values():
        self._generate_lue_property_set(phenomenon.name, p)



      ldm.assert_is_valid(self.lue_filename)



    def _lue_write_property(self, phen_name, pset, prop, timestep):

      lue_pset = self.lue_dataset.phenomena[phen_name].property_sets[pset.name]
      object_ids = self.lue_dataset.phenomena[phen_name].object_id[:]

      if not prop.is_dynamic:
              lue_prop = lue_pset.properties[prop.name]
              if isinstance(prop.space_domain, lue_points.Points):
                for idx, val in enumerate(prop.values().values):
                  lue_prop.value[idx] = prop.values().values[idx]
              elif isinstance(prop.space_domain, lue_areas.Areas):
                for idx, val in enumerate(prop.values().values):
                  lue_prop.value[object_ids[idx]][:] = prop.values().values[idx]
              else:
                raise NotImplementedError

      else:
        if timestep is not None:
                lue_prop = lue_pset.properties[prop.name]
                if isinstance(prop.space_domain, lue_points.Points):
                  for idx, val in enumerate(prop.values().values):
                    #lue_prop.value[:][idx, timestep - 1] = prop.values().values[idx]
                    tmp = lue_prop.value[idx]
                    tmp[timestep - 1] = prop.values().values[idx]
                    lue_prop.value[idx] = tmp
                else:
                  for idx, val in enumerate(prop.values().values):
                    lue_prop.value[object_ids[idx]][timestep - 1] = prop.values().values[idx]


      ldm.assert_is_valid(self.lue_filename)


    def write(self, timestep=None):

      for p in self._phenomena:
        if not p in self.lue_dataset.phenomena:
          self._generate_lue_phenomenon(self._phenomena[p])

        for pset in self._phenomena[p].property_sets.values():
          for prop in pset.properties.values():
            self._lue_write_property(p, pset, prop, timestep)


    def set_time(self, start, unit, stepsize, nrTimeSteps):
      start_timestep = start.isoformat()
      self._nr_timesteps = nrTimeSteps

      epoch = ldm.Epoch(ldm.Epoch.Kind.common_era, start_timestep, ldm.Calendar.gregorian)
      self._lue_clock = ldm.Clock(epoch, unit.value, stepsize)

      self._lue_time_configuration = ldm.TimeConfiguration(ldm.TimeDomainItemType.box)

      self.lue_dataset.add_phenomenon('framework')
      tmp = self.lue_dataset.phenomena['framework']

      self.lue_time_extent = tmp.add_property_set(
              "campo_time_cell",
              self._lue_time_configuration, self._lue_clock)

      # just a number, TODO sampleNumber?
      simulation_id = 1

      # dynamic...
      time_cell = tmp.property_sets["campo_time_cell"]

      time_boxes = 1

      time_cell.object_tracker.active_set_index.expand(time_boxes)[:] = 0
      time_cell.time_domain.value.expand(time_boxes)[:] = [0, self._nr_timesteps]

      ldm.assert_is_valid(self.lue_filename)
