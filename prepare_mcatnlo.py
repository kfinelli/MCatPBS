#!/usr/bin/env python

import random
import os
import common

random.seed(42)


def CreateScript(script_file,input_file,log_file,command,working_dir,subdir):

  str='#!/bin/bash\n'
  str+='export LD_LIBRARY_PATH='+LHAPDF_lib_dir+':$LD_LIBRARY_PATH\n'
  str+='export LHAPATH='+LHAPATH+'\n'
  str+='cd '+working_dir+'\n'
  str+='mkdir -p '+subdir+'\n'
  str+='cd '+subdir+'\n'
  str+=command+' < '+input_file +' >'+log_file+'\n'

  f = open(script_file,'w')
  f.write(str)
  f.close()

def CreateZtautauGenInputScale(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed,fren,ffact):


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
  CreateZtautauGenInputScale(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed,'1','1')

def CreateWWGenInputScale(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed,decay,fren,ffact):
  out=" \'"+fnamebases+"\'                ! prefix for BASES files\n"
  out +=" \'"+prefix_eventfname+"\'               ! prefix for event files\n"
  out +=" 7000 "+fren+" "+ffact+" 1 1 ! energy, fren, ffact, frenmc, ffactmc\n"
  out +="  -12850                          ! -2850/60/70/80=WW/ZZ/ZW+/ZW-\n"
  out +=" "+str(hppdecay[decay][0])+" "+ str(hppdecay[decay][1])+"               ! 0..6 -> t dec, 7 -> t undec\n"
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
  out +="  10 10                 ! itmx1,itmx2\n"

  f = open(input_fname,"w")
  f.write(out)

  f.close()

def CreateWWGenInput(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed,decay):
  CreateWWGenInputScale(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed,decay,'1','1')


def CreateTtbarGenInputScale(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed,fren,ffact):
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
  str +=" 10 10                 ! itmx1,itmx2\n"

  f = open(input_fname,"w")
  f.write(str)

  f.close()




def CreateTtbarGenInput(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed):
  CreateTtbarGenInputScale(input_fname,fnamebases,prefix_eventfname,pdf_number,nevents,randomseed,'1','1')


def DoSubmission_Ztautau(pdfname,pdfnumber,workingdir):

  nsubmissions =1

  command = '../../ztautau.mcatnlo.7TeV.CT10nlotNLO_EXE_LHAPDF'
  fname = 'ztautau.mcatnlo.7TeV.'+pdfname
  subdir = 'ztautau'
  fnamebase = fname + '.bases'
  event_fname = fname + '.events'
  input_fname = fname + '.input'
  log_fname = fname + '.log'
  bsub_fname = fname + '.bsub'

  sub_fname = fname+'.suball.sh'
  fout = open(sub_fname,'w')

  for i in xrange(nsubmissions):

    randomnumber = random.randint(0,100000)
    CreateZtautauGenInput(workingdir+'/'+subdir+'/'+input_fname+'.'+str(i),fnamebase+'.'+str(i),event_fname+'.'+str(i),pdfnumber,str(200000),str(randomnumber))
    CreateScript(bsub_fname+'.'+str(i)+'.sh',input_fname+'.'+str(i),log_fname+'.'+str(i)+'.txt',command,workingdir, subdir)
#    os.chmod(bsub_fname+'.'+str(i)+'.sh',0755)
    #fout.write('qsub -q long -l walltime=100:00:00,cput=100:00:00 '+bsub_fname+'.'+str(i)+'.sh\n')
    fout.write('qsub -q short '+bsub_fname+'.'+str(i)+'.sh\n')
    fout.write('sleep 1\n')

  fout.close()

def DoSubmission_ZtautauScale(pdfname,pdfnumber,workingdir):

  nsubmissions =1

  command = '../../ztautau.mcatnlo.7TeV.CT10nlotNLO_EXE_LHAPDF'
  fname = 'ztautau.mcatnlo.7TeV.'+pdfname
  subdir = 'ztautau'
  fnamebase = fname + '.bases'
  event_fname = fname + '.events'
  input_fname = fname + '.input'
  log_fname = fname + '.log'
  bsub_fname = fname + '.bsub'

  sub_fname = fname+'.scale.suball.sh'
  fout = open(sub_fname,'w')

  fren=[0.5,1,2]
  ffac=[0.5,1,2]

  for f1 in fren:
    for f2 in ffac:
      tag = 'fr'+str(f1).replace('0.5','5')+'ff'+str(f2).replace('0.5','5')
      randomnumber = random.randint(0,100000)
      CreateZtautauGenInputScale(workingdir+'/'+subdir+'/'+input_fname+'.'+tag,fnamebase+tag,event_fname+'.'+tag,pdfnumber,str(200000),str(randomnumber),str(f1),str(f2))
      CreateScript(bsub_fname+'.'+tag+'.sh',input_fname+'.'+tag,log_fname+'.'+tag+'.txt',command,workingdir, subdir)
#    os.chmod(bsub_fname+'.'+str(i)+'.sh',0755)
    #fout.write('qsub -q long -l walltime=100:00:00,cput=100:00:00 '+bsub_fname+'.'+str(i)+'.sh\n')
      fout.write('qsub -q short '+bsub_fname+'.'+tag+'.sh\n')
      fout.write('sleep 1\n')

  fout.close()

def DoSubmission_Ttbar(pdfname,pdfnumber,workingdir):

  nsubmissions =1

  command = '../../ttbar.mcatnlo.7TeV.CT10nlotNLO_EXE_LHAPDF'
  fname = 'ttbar.mcatnlo.7TeV.'+pdfname
  subdir = 'ttbar'
  fnamebase = fname + '.bases'
  event_fname = fname + '.events'
  input_fname = fname + '.input'
  log_fname = fname + '.log'
  bsub_fname = fname + '.bsub'

  sub_fname = fname+'.suball.sh'
  fout = open(sub_fname,'w')

  for i in xrange(nsubmissions):

    randomnumber = random.randint(0,100000)
    CreateTtbarGenInput(workingdir+'/'+subdir+'/'+input_fname+'.'+str(i),fnamebase+'.'+str(i),event_fname+'.'+str(i),pdfnumber,str(200000),str(randomnumber))
    CreateScript(bsub_fname+'.'+str(i)+'.sh',input_fname+'.'+str(i),log_fname+'.'+str(i)+'.txt',command,workingdir,subdir)
#    os.chmod(bsub_fname+'.'+str(i)+'.sh',0755)
    #fout.write('qsub -q long -l walltime=100:00:00,cput=100:00:00 '+bsub_fname+'.'+str(i)+'.sh\n')
    fout.write('qsub -q long '+bsub_fname+'.'+str(i)+'.sh\n')
    fout.write('sleep 1\n')

  fout.close()


def DoSubmission_WW(pdfname,pdfnumber,workingdir):

  nsubmissions =1

  command = '../../ww.mcatnlo.7TeV.CT10nlotNLO_EXE_LHAPDF'
  for idecay in ['em','et','me','mt','te','tm','tt']:
    fname = 'ww'+idecay+'.mcatnlo.7TeV.'+pdfname
    subdir = 'ww'+idecay
    fnamebase = fname + '.bases'
    event_fname = fname + '.events'
    input_fname = fname + '.input'
    log_fname = fname + '.log'
    bsub_fname = fname + '.bsub'

    sub_fname = fname+'.suball.sh'
    fout = open(sub_fname,'w')

    for i in xrange(nsubmissions):

      randomnumber = random.randint(0,100000)
      CreateWWGenInput(workingdir+'/'+subdir+'/'+input_fname+'.'+str(i),fnamebase+'.'+str(i),event_fname+'.'+str(i),pdfnumber,str(50000),str(randomnumber),idecay)
      CreateScript(bsub_fname+'.'+str(i)+'.sh',input_fname+'.'+str(i),log_fname+'.'+str(i)+'.txt',command,workingdir, subdir)
  #    os.chmod(bsub_fname+'.'+str(i)+'.sh',0755)
      #fout.write('qsub -q long -l walltime=100:00:00,cput=100:00:00 '+bsub_fname+'.'+str(i)+'.sh\n')
      fout.write('qsub -q short '+bsub_fname+'.'+str(i)+'.sh\n')
      fout.write('sleep 1\n')

    fout.close()


path={}
path['CT10nlo']='ct10nlo'
path['MSTW2008nlo']='mstw2008nlo'
path['MSTW2008CP']='mstw2008cp'
path['HERAPDF15']='herapdf15nlo'
path['HERAPDF15V']='herapdf15varnlo'
path['NNPDF23']='nnpdf23nlo'
path['ABM11']='abm11nlo'

limit={}
limit['CT10nlo']=53
limit['MSTW2008nlo']=42
limit['MSTW2008CP']=48
limit['HERAPDF15']=21
limit['HERAPDF15V']=14
limit['NNPDF23']=101
limit['ABM11']=29


number={}
number['CT10nlo']=11000
number['MSTW2008nlo']=21100
number['MSTW2008CP']=23800
number['HERAPDF15']=60700
number['HERAPDF15V']=60730
number['NNPDF23']=229800
number['ABM11']=42060

#which = 'CT10nlo'
#which = 'MSTW2008nlo'
#which = 'HERAPDF15'
#which = 'HERAPDF15V'
#which = 'MSTW2008CP'
#which = 'NNPDF23'
#which = 'ABM11'

#DoSubmission_Ttbar(which+str(0),str(number[which]),'/data/finelli/hepsoftware/MC@NLO/LinuxPP/'+path[which]+'/')
#DoSubmission_ZtautauScale(which+str(0),str(number[which]),'/data/saavedra/hepsoftware/MC@NLO/LinuxPP/'+path[which]+'/')
for which in ['CT10nlo',
              'HERAPDF15',
              'HERAPDF15V',
              'MSTW2008CP',
              'NNPDF23',
              'ABM11']:
  for k in xrange(limit[which]):
    DoSubmission_WW(which+str(k),str(number[which]+k),'/data/finelli/hepsoftware/MC@NLO/LinuxPP/'+path[which]+'/')
    DoSubmission_Ttbar(which+str(k),str(number[which]+k),'/data/finelli/hepsoftware/MC@NLO/LinuxPP/'+path[which]+'/')
#  DoSubmission_Ztautau(which+str(k),str(number[which]+k),'/data/saavedra/hepsoftware/MC@NLO/LinuxPP/'+path[which]+'/')

'''
f=open("list_200926.txt")

outf2=open("submit_data12.sh","w")
count=0
for l in f.readlines():
  input_file = l.strip()
  outstr = CreateScript(input_file)
  outf=open("script_data12_"+str(count)+".sh","w")
  outf.write(outstr)
  outf.close()
  outf2.write("qsub -q long script_data12_"+str(count)+".sh\nsleep 30\n")
  count+=1
'''
