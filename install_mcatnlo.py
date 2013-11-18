#!/usr/bin/env python

import mcatpbs_common as common
import urllib
import os, sys
import tarfile
import glob

def parseCmdLine(args):
  """ Parse input command line to optdict. """

  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option("--process", dest="process", help="Name of physics process.  Currently supported: ttbar, ww, ztautau", default='ttbar')
  (config, args) = parser.parse_args(args)
  return config

def WriteBuildScript(process):
  '''Write a minimal build script to compile MC@NLO for running
  'process' (currently ttbar, ww, or ztautau)'''
  lhalibpath=common.LHAPDF_lib_dir
  if ('lib' in common.LHAPDF_lib_dir[-3:]):
    lhalibpath=common.LHAPDF_lib_dir[0:-3]
  if ('lib/' in common.LHAPDF_lib_dir[-4:]):
    lhalibpath=common.LHAPDF_lib_dir[0:-4]

  if process=='ttbar':
    iproc='-11706'
  if process=='ww':
    iproc='-12850'
  if process=='ztautau':
    iproc='-1355'
  outstr = '#!/bin/bash\n'
  outstr += 'IPROC='+iproc + '\n'
  outstr += 'FPREFIX='+process + '\n'
  outstr += 'EVPREFIX='+process + '\n'
  outstr += 'EXEPREFIX='+process + '\n'
  outstr += 'LHALIBPATH="'+lhalibpath+'"\n'

  outstr+='''
  PDFLIBRARY=LHAPDF
  LHALINK=DYNAMIC
  MCMODE=HWPP
  HWUTI="mcatnlo_hwantop.o mcatnlo_hbook.o"
  INCDIRMK="INCDIR="`pwd`"/include"
  SRCDIRMK="SRCDIR="`pwd`"/srcHerwigpp"
  COMSRCMK="COMSRC="`pwd`"/srcCommon"
  IL1CODE=1
  IL2CODE=1


  thisdir=`pwd`
  if [ $MCMODE = "HWPP" ] ; then
  . $thisdir/MCatNLO_pp.Script
  elif [ $MCMODE = "HW6" ] ; then
  . $thisdir/MCatNLO.Script
  else
  echo "Wrong MCMODE, can only be HW6 or HWPP"
  exit 
  fi

  compileNLO
  '''
  f=open(process+'mcnlo.input','w')
  f.write(outstr)
  f.close()

if __name__=="__main__":
  config = parseCmdLine(sys.argv[1:])

  common.checkAndMkdir(common.MCNLO_workdir)

  os.chdir(common.MCNLO_workdir)
  if not os.access(os.path.basename(common.MCNLO_url), os.F_OK):
    urllib.urlretrieve(common.MCNLO_url, os.path.basename(common.MCNLO_url))
  tar = tarfile.open(os.path.basename(common.MCNLO_url))
  tar.extractall()
  tar.close()
  WriteBuildScript(config.process)
  
  prepend=''
  if not (common.LHAPDF_lib_dir in os.getenv('LD_LIBRARY_PATH')):
    print 'fixing ld_library_path'
    prepend='LD_LIBRARY_PATH='+ common.LHAPDF_lib_dir+':' + os.getenv('LD_LIBRARY_PATH')+'; '

  os.system('bash '+config.process+'mcnlo.input')
