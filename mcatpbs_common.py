#path to libLHAPDF.so
LHAPDF_lib_dir='/data/saavedra/hepsoftware/lhapdf/lib/'

#lhapath - path to .LHgrid files
LHAPATH='/data/saavedra/hepsoftware/lhapdf/share/lhapdf/PDFsets/'

#working directory for running MC@NLO here the executables should be found
#(e.g. under the LinuxPP directory).  I need write access to this directory
MCNLO_workdir='/data/finelli/analysisStandalone/hepsoftware/NLOGen/'

#working directory for PBS scripts
PBS_workdir='/data/finelli/test/'

#download URL for mcatnlo tgz
MCNLO_url='http://www.hep.phy.cam.ac.uk/theory/webber/MCatNLO/Package4.10_dist.tar.gz'


#herwig decay paths for WW
hppdecay = {'ee':[1, 1],
            'em':[1, 2],
            'et':[1, 3],
            'me':[2, 1],
            'mm':[2, 2],
            'mt':[2, 3],
            'te':[3, 1],
            'tm':[3, 2],
            'tt':[3, 3]}

processes=['ttbar','ww','ztautau']

pdfs=['CT10nlo',
      'MSTW2008nlo68cl',
      'MSTW2008CPdeutnlo68cl',
      'abm11_5n_nlo',
      'HERAPDF15NLO_EIG',
      'HERAPDF15NLO_VAR',
      'NNPDF23_nlo_as_0118']

limit={}
limit['CT10nlo']=53
limit['MSTW2008nlo68cl']=42
limit['MSTW2008CPdeutnlo68cl']=48
limit['abm11_5n_nlo']=29
limit['HERAPDF15NLO_EIG']=21
limit['HERAPDF15NLO_VAR']=13
limit['NNPDF23_nlo_as_0118']=101


number={}
number['CT10nlo']=11000
number['MSTW2008nlo68cl']=21100
number['MSTW2008CPdeutnlo68cl']=23800
number['abm11_5n_nlo']=42060
number['HERAPDF15NLO_EIG']=60700
number['HERAPDF15NLO_VAR']=60730
number['NNPDF23_nlo_as_0118']=229800

def checkAndMkdir(dirname):
    import os, errno
    """check that the necessary directories are in place, make if necessary"""
    if not os.path.exists(dirname):
        print 'making '+dirname
    try:
        os.makedirs(dirname)
    except OSError as exc: 
        if exc.errno == errno.EEXIST and os.path.isdir(dirname):
            pass
