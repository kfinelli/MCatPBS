#!/usr/bin/env python

import random
import os, sys
import mcatpbs_common as common

random.seed()

def parseCmdLine(args):
  """ Parse input command line to optdict. """

  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option("--process", dest="process", help="Name of physics process.  Currently supported: ttbar, ww, ztautau", default='ttbar')
  parser.add_option("--pdf", dest="pdf", help="Name of PDF set to use, named as at http://lhapdf.hepforge.org/pdfsets", default='CT10nlo') 
  parser.add_option("--doScale", dest="doScale", help="Create scale variation output scripts", action='store_true', default=False)
  (config, args) = parser.parse_args(args)
  return config



def CreateScript(script_file, input_file, log_file, command, working_dir, subdir):
  """
  Write out bash script with filename 'script_file' which will run the
  MC@NLO executable 'command' from input card 'input_file' with stdout
  directed to 'log_file'.  MC@NLO is run in 'working_dir'/'subdir'.
  """
  str='#!/bin/bash\n'
  str+='export LD_LIBRARY_PATH='+common.LHAPDF_lib_dir+':$LD_LIBRARY_PATH\n'
  str+='export LHAPATH='+common.LHAPATH+'\n'
  str+='cd '+working_dir+'\n'
  str+='mkdir -p '+subdir+'\n'
  str+='cd '+subdir+'\n'
  str+=command+' < '+input_file +' >'+log_file+'\n'

  f = open(script_file,'w')
  f.write(str)
  f.close()

def CreateZtautauGenInputScale(input_fname, fnamebases, prefix_eventfname, pdf_number, nevents, randomseed, fren, ffact):
  """
  Create an input card 'input_fname' for MC@NLO running that generates
  Z->tau+tau events.  MC@NLO needs to have BASES file 'fnamebases' and
  will write event files with prefix 'prefix_eventfname'.  Events will
  be generated with PDF given by 'pdf_number' according to the LHAPDF
  numbering scheme.
  """

  str=" \'"+fnamebases+"\'                ! prefix for BASES files\n"
  str +=" \'"+prefix_eventfname+"\'               ! prefix for event files\n"
  str +=" 7000 "+fren+" "+ffact+" 1 1 ! energy, fren, ffact, frenmc, ffactmc\n"
  str +=" -1355                          ! -135#/136#/137#/146#/147#=Zg/Z/g/W+/W-\n"
  str +=" 91.1876 2.4952                  ! M_V, Ga_V\n"
  str +=" -1 40 2400 ! GammaX, M_V(min), M_V(max)\n"
  str +=" 0.32 0.32 0.5 1.29 4.2 0.75 ! quark and gluon masses\n"
  str +=" \'P\'  \'P\'               ! hadron types\n"
  str +=" \'LHAPDF\' "+pdf_number+"   ! PDF group and id number\n"
  str +=" -1                     ! Lambda_5, <0 for default\n"
  str +=" \'MS\'                   ! scheme\n"
  str +=" "+nevents+"              ! number of events\n"
  str +=" 1                        ! 0 => wgt=+1/-1, 1 => wgt=+w/-w\n"
  str +=" "+randomseed+"           ! seed for rnd numbers\n"
  str +=" 0                        ! 0=running, 1=fixed alpha_EM\n"
  str +=" 1                        ! 0 => MC@@NLO format, 1 => LHEF\n"
  str +=" 10 10                 ! itmx1,itmx2\n"

  f = open(input_fname,"w")
  f.write(str)

  f.close()

def CreateZtautauGenInput(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed):
  """Create gen input in the case of nominal ren/fac scales"""
  CreateZtautauGenInputScale(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed,'1','1')

def CreateWWGenInputScale(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed,decay,fren,ffact):
  """
  Create an input card 'input_fname' for MC@NLO running that generates
  WW events.  MC@NLO needs to have BASES file 'fnamebases' and will
  write event files with prefix 'prefix_eventfname'.  Events will be
  generated with PDF given by 'pdf_number' according to the LHAPDF
  numbering scheme.  The decay mode of the WW pair is specified by
  'decay' as 'em', 'et', 'ee', etc.
  """
  out=" \'"+fnamebases+"\'                ! prefix for BASES files\n"
  out +=" \'"+prefix_eventfname+"\'               ! prefix for event files\n"
  out +=" 7000 "+fren+" "+ffact+" 1 1 ! energy, fren, ffact, frenmc, ffactmc\n"
  out +="  -12850                          ! -2850/60/70/80=WW/ZZ/ZW+/ZW-\n"
  out +=" "+str(common.hppdecay[decay][0])+" "+ str(common.hppdecay[decay][1])+"               ! 0..6 -> t dec, 7 -> t undec\n"
  out +=" 80.42 2.124                  ! M_W, Gamma_W\n"
  out +=" 91.19  2.495                          ! Z Mass and Width\n"
  out +=" 30 0 0 ! GammaX, M_V1(min), M_V1(max)\n"
  out +=" 30 0 0 ! GammaX, M_V2(min), M_V2(max)\n"
  out +=" 0.1111                     ! t -> leptons branching ratio\n"
  out +=" 0.3333                     ! t -> hadrons branching ratio\n"
  out +=" 0 0 0        ! Dg_1(Z), Dk(Z), lambda(Z)\n"
  out +=" 0 0 0  ! Dg_1(ph), Dk(ph), lambda(ph)\n"
  out +=" 0                        ! Lambda of FF\n"
  out +="  1                        ! 0=an cpl weights, 1=no weights\n"
  out +="  0.32 0.32 0.5 1.55 4.95 0.75 ! quark and gluon masses\n"
  out +=" \'P\'  \'P\'               ! hadron types\n"
  out +=" \'LHAPDF\'   "+pdf_number+"            ! PDF group and id number\n"
  out +="  -1                     ! Lambda_5, <0 for default\n"
  out +=" \'MS\'                   ! scheme\n"
  out +=" "+nevents+"                        ! number of events\n"
  out +="  1                        ! 0 => wgt=+1/-1, 1 => wgt=+w/-w\n"
  out +=" "+randomseed+"                      ! seed for rnd numbers\n"
  out +="  0.2                             ! zi\n"
  out +="  0                        ! 0=running, 1=fixed alpha_EM\n"
  out +="  1                        ! 0 => MC@@NLO format, 1 => LHEF\n"
  out +="  10 10                 ! itmx1,itmx2\n"

  f = open(input_fname,"w")
  f.write(out)

  f.close()

def CreateWWGenInput(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed,decay):
  """Create gen input in the case of nominal ren/fac scales"""
  CreateWWGenInputScale(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed,decay,'1','1')


def CreateTtbarGenInputScale(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed,fren,ffact):
  """
  Create an input card 'input_fname' for MC@NLO running that generates
  ttbar events.  MC@NLO needs to have BASES file 'fnamebases' and will
  write event files with prefix 'prefix_eventfname'.  Events will be
  generated with PDF given by 'pdf_number' according to the LHAPDF
  numbering scheme.
  """
  str=" \'"+fnamebases+"\'                ! prefix for BASES files\n"
  str +=" \'"+prefix_eventfname+"\'               ! prefix for event files\n"
  str +=" 7000 "+fren+" "+ffact+" 1 1 ! energy, fren, ffact, frenmc, ffactmc\n"
  str +="  -11706                          ! -1705/1706=bb/tt\n"
  str +=" 172.5                        ! M_Q\n"
  str +=" 0 0               ! 0..6 -> t dec, 7 -> t undec\n"
  str +=" 1.4                         ! top width\n"
  str +=" 80.42 2.124                  ! M_W, Gamma_W\n"
  str +=" 30 0 0 ! GammaX, M_T(min), M_T(max)\n"
  str +=" 30 0 0 ! GammaX, M_Tb(min), M_Tb(max)\n"
  str +=" 30 0 0 ! GammaX, M_V1(min), M_V1(max)\n"
  str +=" 30 0 0 ! GammaX, M_V2(min), M_V2(max)\n"
  str +=" 0.9748 0.2225 0.0036                  ! |V_ud|,|V_us|,|V_ub|\n"
  str +=" 0.2225 0.9740 0.041                  ! |V_cd|,|V_cs|,|V_cb|\n"
  str +=" 0.009 0.0405 0.9992                  ! |V_td|,|V_ts|,|V_tb|\n"
  str +=" 0                       ! 0=t->Wb, 1=t->W+any d\n"
  str +=" 0.1111                     ! t -> leptons branching ratio\n"
  str +=" 0.3333                     ! t -> hadrons branching ratio\n"
  str +=" 0.32 0.32 0.5 1.55 4.95 0.75 ! quark and gluon masses\n"
  str +=" \'P\'  \'P\'               ! hadron types\n"
  str +=" \'LHAPDF\'   "+pdf_number+"            ! PDF group and id number\n"
  str +=" -1                     ! Lambda_5, <0 for default\n"
  str +=" \'MS\'                   ! scheme\n"
  str +=" "+nevents+"                        ! number of events\n"
  str +=" 1                        ! 0 => wgt=+1/-1, 1 => wgt=+w/-w\n"
  str +=" "+randomseed+"                      ! seed for rnd numbers\n"
  str +=" 0.3                             ! zi\n"
  str +=" 1                        ! 0 => MC@@NLO format, 1 => LHEF\n"
  str +=" 10 10                 ! itmx1,itmx2\n"

  f = open(input_fname,"w")
  f.write(str)

  f.close()


def CreateTtbarGenInput(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed):
  """Create gen input in the case of nominal ren/fac scales"""
  CreateTtbarGenInputScale(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed,'1','1')


def DoSubmission_Ztautau(pdfname,pdfnumber,workingdir):
  """
  Create MC@NLO input cards and batch submission scripts to generate
  Z->tau+tau events with nominal ren/fac scale using PDF
  'pdfname','pdfnumber' which will run under 'workingdir'.
  """
  nsubmissions =1

  command = common.MCNLO_workdir+'/LinuxPP/ztautauNLO_EXE_LHAPDF'
  fname = 'ztautau.mcatnlo.7TeV.'+pdfname
  subdir = 'ztautau'
  fnamebase = fname + '.bases'
  event_fname = fname + '.events'
  input_fname = fname + '.input'
  log_fname = fname + '.log'
  bsub_fname = fname + '.bsub'

  sub_fname = common.PBS_workdir+fname+'.suball.sh'
  fout = open(sub_fname,'w')

  for i in xrange(nsubmissions):

    randomnumber = random.randint(0,100000)
    CreateZtautauGenInput(workingdir+'/'+subdir+'/'+input_fname+'.'+str(i), fnamebase+'.'+str(i), event_fname+'.'+str(i), pdfnumber,str(200000), str(randomnumber))
    CreateScript(common.PBS_workdir+bsub_fname+'.'+str(i)+'.sh',input_fname+'.'+str(i),log_fname+'.'+str(i)+'.txt',command,workingdir, subdir)
    fout.write('qsub -q short '+bsub_fname+'.'+str(i)+'.sh\n')
    fout.write('sleep 1\n')

  fout.close()

def DoSubmission_ZtautauScale(pdfname,pdfnumber,workingdir):
  """
  Create MC@NLO input cards and batch submission scripts to generate
  Z->tau+tau events with 2x and 0.5x ren/fac scale variations using PDF
  'pdfname','pdfnumber' which will run under 'workingdir'.
  """

  command = common.MCNLO_workdir+'/LinuxPP/ztautauNLO_EXE_LHAPDF'
  fname = 'ztautau.mcatnlo.7TeV.'+pdfname
  subdir = 'ztautau'
  fnamebase = fname + '.bases'
  event_fname = fname + '.events'
  input_fname = fname + '.input'
  log_fname = fname + '.log'
  bsub_fname = fname + '.bsub'

  sub_fname = common.PBS_workdir+fname+'.scale.suball.sh'
  fout = open(sub_fname,'w')

  fren=[0.5,1,2]
  ffac=[0.5,1,2]

  for f1 in fren:
    for f2 in ffac:
      tag = 'fr'+str(f1).replace('0.5','5')+'ff'+str(f2).replace('0.5','5')
      randomnumber = random.randint(0,100000)
      CreateZtautauGenInputScale(workingdir+'/'+subdir+'/'+input_fname+'.'+tag,fnamebase+tag,event_fname+'.'+tag,pdfnumber,str(200000),str(randomnumber),str(f1),str(f2))
      CreateScript(common.PBS_workdir+bsub_fname+'.'+tag+'.sh', input_fname+'.'+tag, log_fname+'.'+tag+'.txt', command, workingdir, subdir)
      fout.write('qsub -q short '+bsub_fname+'.'+tag+'.sh\n')
      fout.write('sleep 1\n')

  fout.close()

def DoSubmission_Ttbar(pdfname,pdfnumber,workingdir):
  """
  Create MC@NLO input cards and batch submission scripts to generate
  ttbar events with nominal ren/fac scale using PDF
  'pdfname','pdfnumber' which will run under 'workingdir'.
  """

  nsubmissions =1

  command = common.MCNLO_workdir+'/LinuxPP/ttbarNLO_EXE_LHAPDF'
  fname = 'ttbar.mcatnlo.7TeV.'+pdfname
  subdir = 'ttbar'
  fnamebase = fname + '.bases'
  event_fname = fname + '.events'
  input_fname = fname + '.input'
  log_fname = fname + '.log'
  bsub_fname = fname + '.bsub'

  sub_fname = common.PBS_workdir+fname+'.suball.sh'
  fout = open(sub_fname,'w')

  for i in xrange(nsubmissions):

    randomnumber = random.randint(0,100000)
    CreateTtbarGenInput(workingdir+'/'+subdir+'/'+input_fname+'.'+str(i),fnamebase+'.'+str(i),event_fname+'.'+str(i),pdfnumber,str(200000),str(randomnumber))
    CreateScript(common.PBS_workdir+bsub_fname+'.'+str(i)+'.sh',input_fname+'.'+str(i),log_fname+'.'+str(i)+'.txt',command,workingdir,subdir)
    fout.write('qsub -q long '+bsub_fname+'.'+str(i)+'.sh\n')
    fout.write('sleep 1\n')

  fout.close()


def DoSubmission_TtbarScale(pdfname,pdfnumber,workingdir):
  """
  Create MC@NLO input cards and batch submission scripts to generate
  ttbar events with varied ren/fac scale using PDF
  'pdfname','pdfnumber' which will run under 'workingdir'.
  """

  command = common.MCNLO_workdir+'/LinuxPP/ttbarNLO_EXE_LHAPDF'
  fname = 'ttbar.mcatnlo.7TeV.'+pdfname
  subdir = 'ttbar'
  fnamebase = fname + '.bases'
  event_fname = fname + '.events'
  input_fname = fname + '.input'
  log_fname = fname + '.log'
  bsub_fname = fname + '.bsub'

  sub_fname = common.PBS_workdir+fname+'.scale.suball.sh'
  fout = open(sub_fname,'w')

  fren=[0.5,1,2]
  ffac=[0.5,1,2]

  for f1 in fren:
    for f2 in ffac:
      tag = 'fr'+str(f1).replace('0.5','5')+'ff'+str(f2).replace('0.5','5')
      randomnumber = random.randint(0,100000)
      CreateTtbarGenInputScale(workingdir+'/'+subdir+'/'+input_fname+'.'+tag, fnamebase+tag, event_fname+'.'+tag,pdfnumber,str(200000),str(randomnumber),str(f1),str(f2))
      CreateScript(common.PBS_workdir+bsub_fname+'.'+tag+'.sh', input_fname+'.'+tag, log_fname+'.'+tag+'.txt', command, workingdir, subdir)
      fout.write('qsub -q short '+bsub_fname+'.'+tag+'.sh\n')
      fout.write('sleep 1\n')

  fout.close()



def DoSubmission_WW(pdfname,pdfnumber,workingdir):
  """
  Create MC@NLO input cards and batch submission scripts to generate
  WW events with nominal ren/fac scale using PDF 'pdfname','pdfnumber'
  which will run under 'workingdir'.
  """

  nsubmissions =1

  command = common.MCNLO_workdir+'/LinuxPP/wwNLO_EXE_LHAPDF'
  for idecay in ['em','et','me','mt','te','tm','tt']:
    fname = 'ww'+idecay+'.mcatnlo.7TeV.'+pdfname
    subdir = 'ww'+idecay
    fnamebase = fname + '.bases'
    event_fname = fname + '.events'
    input_fname = fname + '.input'
    log_fname = fname + '.log'
    bsub_fname = fname + '.bsub'

    sub_fname = common.PBS_workdir+fname+'.suball.sh'
    fout = open(sub_fname,'w')

    for i in xrange(nsubmissions):

      randomnumber = random.randint(0,100000)
      CreateWWGenInput(workingdir+'/'+subdir+'/'+input_fname+'.'+str(i),fnamebase+'.'+str(i),event_fname+'.'+str(i),pdfnumber,str(50000),str(randomnumber),idecay)
      CreateScript(common.PBS_workdir+bsub_fname+'.'+str(i)+'.sh',input_fname+'.'+str(i),log_fname+'.'+str(i)+'.txt',command,workingdir, subdir)
      fout.write('qsub -q short '+bsub_fname+'.'+str(i)+'.sh\n')
      fout.write('sleep 1\n')

    fout.close()


def DoSubmission_WWScale(pdfname,pdfnumber,workingdir):
  """
  Create MC@NLO input cards and batch submission scripts to generate
  WW events with nominal ren/fac scale using PDF 'pdfname','pdfnumber'
  which will run under 'workingdir'.
  """

  nsubmissions =1

  command = common.MCNLO_workdir+'/LinuxPP/wwNLO_EXE_LHAPDF'
  for idecay in ['em','et','me','mt','te','tm','tt']:
    fname = 'ww'+idecay+'.mcatnlo.7TeV.'+pdfname
    subdir = 'ww'+idecay
    fnamebase = fname + '.bases'
    event_fname = fname + '.events'
    input_fname = fname + '.input'
    log_fname = fname + '.log'
    bsub_fname = fname + '.bsub'

    sub_fname = common.PBS_workdir+fname+'.suball.sh'
    fout = open(sub_fname,'w')

    fren=[0.5,1,2]
    ffac=[0.5,1,2]

    for f1 in fren:
      for f2 in ffac:
        tag = 'fr'+str(f1).replace('0.5','5')+'ff'+str(f2).replace('0.5','5')
        randomnumber = random.randint(0,100000)
        CreateWWGenInputScale(workingdir+'/'+subdir+'/'+input_fname+'.'+tag, fnamebase+tag, event_fname+'.'+tag,pdfnumber,str(200000),str(randomnumber), idecay, str(f1),str(f2))
        CreateScript(common.PBS_workdir+bsub_fname+'.'+tag+'.sh', input_fname+'.'+tag, log_fname+'.'+tag+'.txt', command, workingdir, subdir)
        fout.write('qsub -q short '+bsub_fname+'.'+tag+'.sh\n')
        fout.write('sleep 0.3\n')

    fout.close()


if __name__=="__main__":
  config = parseCmdLine(sys.argv[1:])

  if not (config.pdf in common.pdfs):
    print 'Invalid PDF name, abort'
    sys.exit(1)

  if not (config.process in common.processes):
    print 'Invalid process name, abort'
    sys.exit(1)

  directory_name=common.MCNLO_workdir+config.pdf+'/'+config.process
  """check that the necessary directories are in place"""
  if not os.path.exists(directory_name):
    print 'making '+directory_name
    try:
      os.makedirs(directory_name)
    except OSError as exc: 
      if exc.errno == errno.EEXIST and os.path.isdir(directory_name):
        pass

  for k in xrange(common.limit[config.pdf]):
    if config.process=='ww':
      if config.doScale:        
        DoSubmission_WWScale(config.pdf+str(k), str(common.number[config.pdf]+k), common.MCNLO_workdir+config.pdf+'/')
      else:
        DoSubmission_WW(config.pdf+str(k), str(common.number[config.pdf]+k), common.MCNLO_workdir+config.pdf+'/')
    if config.process=='ttbar':
      if config.doScale:        
        DoSubmission_TtbarScale(config.pdf+str(k), str(common.number[config.pdf]+k), common.MCNLO_workdir+config.pdf+'/')
      else:
        DoSubmission_Ttbar(config.pdf+str(k), str(common.number[config.pdf]+k), common.MCNLO_workdir+config.pdf+'/')
    if config.process=='ztautau':
      if config.doScale:        
        DoSubmission_ZtautauScale(config.pdf+str(k), str(common.number[config.pdf]+k), common.MCNLO_workdir+config.pdf+'/')
      else:
        DoSubmission_Ztautau(config.pdf+str(k), str(common.number[config.pdf]+k), common.MCNLO_workdir+config.pdf+'/')
