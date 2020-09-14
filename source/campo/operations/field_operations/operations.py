import os
import numpy


import pcraster

import campo.lue_property as lue_property

import campo


def _spatial_operation(area_property, spatial_operation):


      for item_idx, item in enumerate(area_property.values):

        west = area_property.pset_domain.p1.xcoord[item_idx]
        north = area_property.pset_domain.p1.ycoord[item_idx]

        rows = int(area_property.pset_domain.row_discr[item_idx])
        cols = int(area_property.pset_domain.col_discr[item_idx])


        cellsize = (area_property.pset_domain.p2.xcoord[item_idx] - west ) / cols

        pcraster.setclone(rows, cols, cellsize, west, north)

        raster = pcraster.numpy2pcr( pcraster.Scalar, item,numpy.nan)















def report(area_property, output_dir=os.getcwd(), timestep=None, pcr_type=None):
      print ('report {} '.format( output_dir))

      print('pset domain #items {}'.format(area_property.pset_domain.nr_items))


      if not os.path.exists(output_dir):
        os.mkdir(output_dir)


      for item_idx, item in enumerate(area_property.values):

        out_dir =  os.path.join(output_dir, str(item_idx))

        if not os.path.exists(out_dir):
          os.mkdir(out_dir)
        os.makedirs(out_dir, exist_ok=True)

        if timestep is None:
          fname = '{}.map'.format(area_property.name)
        else:
          fname = '{}_{}.map'.format(area_property.name, timestep)

        fname = '{}'.format(os.path.join(out_dir, fname))

        west = area_property.pset_domain.p1.xcoord[item_idx]
        north = area_property.pset_domain.p1.ycoord[item_idx]

        rows = int(area_property.pset_domain.row_discr[item_idx])
        cols = int(area_property.pset_domain.col_discr[item_idx])


        cellsize = (area_property.pset_domain.p2.xcoord[item_idx] - west ) / cols #rows #cols #000 #self.pset_domain.


        print(rows, cols, cellsize, west, north)


        pcraster.setclone(rows, cols, cellsize, west, north)

        # fttb set the origin the same to be sure that aguila dislays properly...
        # pcraster.setclone(rows, cols, cellsize, 0, 0)

        rasternp = item

        if pcr_type is None:
          pcr_type = pcraster.Scalar



        raster = pcraster.numpy2pcr(pcr_type, item,numpy.nan)



        pcraster.report(raster, fname)









def spread(start_locations, frictiondist, friction):
  """ """


  result_prop = campo.lue_property.Property('emptyspreadname', start_locations.pset_uuid, start_locations.space_domain, start_locations.shapes)


  for idx in start_locations.values().values.keys():
    values = start_locations.values().values[idx]
    _set_current_clone(start_locations, idx)

    frictiondistvalues = frictiondist.values().values[idx]
    frictionvalues = friction.values().values[idx]

    arg1_raster = pcraster.numpy2pcr(pcraster.Nominal, values, -999) #numpy.nan)
    frictiondist_raster = pcraster.numpy2pcr(pcraster.Scalar, frictiondistvalues, numpy.nan)
    friction_raster = pcraster.numpy2pcr(pcraster.Scalar, frictionvalues, numpy.nan)

    result_raster = pcraster.spread(arg1_raster, frictiondist_raster, friction_raster)
    result_item = pcraster.pcr2numpy(result_raster, numpy.nan)
    result_prop.values().values[idx] = result_item

  return result_prop








def spread2(property_set, start_locations, frictiondist, friction):
  """ """

  # generate a property to store the result

  result_prop = lue_property.Property(property_set._phen, property_set.shapes, property_set.uuid, property_set._domain, property_set.time_discretization)


  for item_idx, item in enumerate(start_locations.values().values):
        _set_current_clone(start_locations, item_idx)

        arg1_raster = pcraster.numpy2pcr(pcraster.Nominal, start_locations.values().values[item_idx], numpy.nan)

        result_raster = pcraster.spread(arg1_raster, frictiondist, friction)

        result_item = pcraster.pcr2numpy(result_raster, numpy.nan)

        result_prop.values().values[item_idx] = result_item

  return result_prop





def _new_property_from_property(area_property, multiplier):

  # make empty property
  new_prop = lue_property.Property()

  fame.lue_property.Property(property_set._phen, property_set.shapes, property_set.uuid, property_set._domain, property_set.time_discretization)

  # attach propertyset domain if available
  new_prop.pset_domain = area_property.pset_domain

  # obtain number, datatype and shape of value
  #nr_items = area_property
  #shape = area_property.values.shape
  #dtype = area_property.values.dtype



  new_prop.shape = area_property.shape
  new_prop.dtype = area_property.dtype

  #None
  nr_items = area_property.shape[0]

  # create and attach new value to property
  values = numpy.ones(area_property.shape, area_property.dtype)

  #
  new_prop.values = values



  return new_prop





def _set_current_clone(area_property, item_idx):

    west = area_property.space_domain.p1.xcoord[item_idx]
    north = area_property.space_domain.p1.ycoord[item_idx]

    rows = int(area_property.space_domain.row_discr[item_idx])
    cols = int(area_property.space_domain.col_discr[item_idx])


    cellsize = (area_property.space_domain.p2.xcoord[item_idx] - west ) / cols

    pcraster.setclone(rows, cols, cellsize, west, north)




def _spatial_operation_one_argument(area_property, spatial_operation, pcr_type):


  # generate a property to store the result
  result_prop = _new_property_from_property(area_property, 0.0)



  for item_idx, item in enumerate(area_property.values):


        _set_current_clone(area_property, item_idx)


        arg_raster = pcraster.numpy2pcr(pcr_type, item, numpy.nan)

        result_raster = spatial_operation(arg_raster)
        result_item = pcraster.pcr2numpy(result_raster, numpy.nan)

        result_prop.values[item_idx] = result_item



  return result_prop





def _spatial_operation_two_arguments(arg1_property, arg2_property, spatial_operation, pcr_type):



  # generate a property to store the result
  result_prop = _new_property_from_property(arg1_property, 0.0)



  for item_idx, item in enumerate(arg1_property.values):

        _set_current_clone(arg1_property, item_idx)


        arg1_raster = pcraster.numpy2pcr(pcr_type, arg1_property.values[item_idx], numpy.nan)
        arg2_raster = pcraster.numpy2pcr(pcr_type, arg2_property.values[item_idx], numpy.nan)


        result_raster = spatial_operation(arg1_raster, arg2_raster)

        result_item = pcraster.pcr2numpy(result_raster, numpy.nan)

        result_prop.values[item_idx] = result_item



  return result_prop













def uniform(area_property):
  return _spatial_operation_one_argument(area_property, pcraster.uniform, pcraster.Boolean)



def window4total(area_property):
  return _spatial_operation_one_argument(area_property, pcraster.window4total, pcraster.Scalar)


def windowtotal(area_property, window_size):

  if not isinstance(window_size, lue_property.Property):
    window_size =_new_property_from_property(area_property, window_size)

  return _spatial_operation_two_arguments(area_property, window_size, pcraster.windowtotal, pcraster.Scalar)



def field_add(arg1_property, arg2_property):
  pass


def field_sub(arg1_property, arg2_property):


  return _spatial_operation_two_arguments(arg1_property, arg2_property, pcraster.operators.pcrSub, pcraster.Scalar)



def field_and(arg1_property, arg2_property):
  return _spatial_operation_two_arguments(arg1_property, arg2_property, pcraster.operators.pcrAnd, pcraster.Boolean)


def field_or(arg1_property, arg2_property):

  return _spatial_operation_two_arguments(arg1_property, arg2_property, pcraster.operators.pcrOr, pcraster.Boolean)


def field_not(arg1_property):
  return _spatial_operation_one_argument(arg1_property, pcraster.operators.pcrNot, pcraster.Boolean)



def field_less_than(arg1_property, arg2_property):

  if not isinstance(arg2_property, lue_property.Property):
    assert(isinstance(arg2_property, float))
    arg2_property =_new_property_from_property(arg1_property, arg2_property)


  return _spatial_operation_two_arguments(arg1_property, arg2_property, pcraster.operators.pcrLT, pcraster.Scalar)




def field_equals(arg1_property, arg2_property):

  if not isinstance(arg2_property, lue_property.Property):
    arg2_property =_new_property_from_property(arg1_property, arg2_property)
  return _spatial_operation_two_arguments(arg1_property, arg2_property, pcraster.operators.pcrEQ, pcraster.Scalar)





#lue_property.Property.__lt__      = field_less_than
#lue_property.Property.__sub__     = field_sub

#lue_property.Property.__eq__      = field_equals
#lue_property.Property.__and__     = field_and
#lue_property.Property.__or__      = field_or
#lue_property.Property.__invert__  = field_not
