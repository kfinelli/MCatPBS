#!/usr/bin/env python

import mcatpbs_common as common
import urllib
import os, sys
import tarfile
import glob

if __name__=="__main__":
  config = parseCmdLine(sys.argv[1:])

  common.checkAndMkdir(common.MCNLO_workdir)

  os.chdir(common.MCNLO_workdir)
  urllib.urlretrieve(common.MCNLO_url, os.path.basename(common.MCNLO_url))
  tar = tarfile.open(os.path.basename(common.MCNLO_url))
  tar.extractall()
  tar.close()

