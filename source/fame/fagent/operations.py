import copy
import numpy as np

import pcraster as pcr

import fame.lue_property as property
import fame.lue_points as points
import fame.lue_areas as areas




def slope(prop):
  """ slope for each object """
  if not isinstance(prop, property.Property):
    raise NotImplementedError

  if not isinstance(prop.pset_domain, areas.Areas):
    raise NotImplementedError



  tmp_prop = copy.deepcopy(prop)

  for idx,p in enumerate(prop.pset_domain):
    ulx = p[0]
    uly = p[1]
    rows = int(p[4])
    cols = int(p[5])
    cellsize = (p[2] - p[0]) / cols
    values = prop.values()[0]
    in_dtype = np.dtype(values.dtype)

    pcr.setclone(rows, cols, cellsize, ulx, uly)

    raster = pcr.numpy2pcr(pcr.VALUESCALE.Scalar, values, np.nan)

    result = pcr.slope(raster)

    np_result = pcr.pcr2numpy(result, np.nan)

    np_result_type = np_result.astype(in_dtype)

    tmp_prop.values()[idx] = np_result_type

    return tmp_prop
