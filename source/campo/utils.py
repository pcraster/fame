import math
import pandas as pd
from osgeo import gdal
from osgeo import osr
import os
import subprocess
import tempfile
import numpy
import shutil

import lue.data_model as ldm

from .dataframe import *

def to_csv(frame, filename):

  phen_name = frame.keys()

  dfObj = pd.DataFrame()

  for phen_name in frame.keys():
    phen = frame[phen_name]
    for pset_name in phen.keys():
      propset = frame[phen_name][pset_name]

      for prop_name in propset.keys():
        dfObj['x'] = frame[phen_name][pset_name][prop_name]['coordinates'].data[:, 0]
        dfObj['y'] = frame[phen_name][pset_name][prop_name]['coordinates'].data[:, 1]


      for prop_name in propset.keys():
        prop = frame[phen_name][pset_name][prop_name]

        dfObj[prop_name] = prop['values'].data

  dfObj.to_csv(filename, index=False)




def create_pdf(frame, filename):

  phen_name = frame.keys()

  wdir = os.getcwd()
  data_dir = os.path.join(wdir,'data')

  tmpdir = 'tmp'
  if os.path.exists(tmpdir):
    shutil.rmtree(tmpdir)

  os.mkdir(tmpdir)


  #with tempfile.TemporaryDirectory() as tmpdir:
  fnames = []
  lnames = []

  for phen_name in frame.keys():
    phen = frame[phen_name]
    for pset_name in phen.keys():
      propset = frame[phen_name][pset_name]

      for prop_name in propset.keys():

        objects = frame[phen_name][pset_name][prop_name]

        for obj_id in objects:
          obj = objects[obj_id]

          rows = obj.values.shape[0]
          cols = obj.values.shape[1]
          cellsize = math.fabs(obj.xcoord[1].values - obj.xcoord[0].values)

          data = obj.data
          data = data/(data.max()/250.0)
          xmin = obj.xcoord[0].values.item()
          ymax = obj.ycoord[-1].values.item()
          geotransform = (xmin, cellsize, 0, ymax, 0, -cellsize)

          fname = os.path.join(tmpdir, '{:03d}'.format(obj_id))
          #fname = os.path.join('{:03d}'.format(obj_id))
          fnames.append(fname)
          lnames.append('shop{:03d}'.format(obj_id))


          dst_ds = gdal.GetDriverByName('GTiff').Create(fname, cols, rows, 1, gdal.GDT_Byte)
          dst_ds.SetGeoTransform(geotransform)
          srs = osr.SpatialReference()
          srs.ImportFromEPSG(28992)
          dst_ds.SetProjection(srs.ExportToWkt())
          dst_ds.GetRasterBand(1).WriteArray(data)
          dst_ds = None


  outfile = os.path.join(wdir, filename)
  clone = os.path.join(data_dir, 'clone.tiff')
  roads = os.path.join(data_dir, 'roads.gpkg')

  rasters = ','.join(fnames)
  names = ','.join(lnames)


  cmd = 'gdal_translate -q -of PDF -a_srs EPSG:28992 {} {} -co OGR_DATASOURCE={} -co OGR_DISPLAY_FIELD="roads" -co EXTRA_RASTERS={} -co EXTRA_RASTERS_LAYER_NAME={} -co OFF_LAYERS={}'.format(clone, outfile,roads,rasters,names,names )
  cmd = 'gdal_translate -q -of PDF -a_srs EPSG:28992 {} {} -co OGR_DATASOURCE={} -co OGR_DISPLAY_FIELD="roads" -co EXTRA_RASTERS={} -co EXTRA_RASTERS_LAYER_NAME={}'.format(clone, outfile,roads,rasters,names)

  subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL)
  shutil.rmtree(tmpdir)
  print(cmd, len(cmd))
