import sys, getopt , adnod,pdh_files,os,subprocess

#def frend(argv):        # arguments passed to frend , user name and frend file
                                # need to think security measures here to limit user and access to instance of PDH
                                # probbly have a master file which sets up PDH on a system provides access and
				# allows for setting of system path globals below they are hardcoded.
				#
drpath=r'C:/PDH/Data/'
urpath=r'C:/PDH/User/'
srpath=r'C:/PDH/System/'

                                # with username and frend file read master user name file establish file name node
unum='4'                    # NAF Usernm2UserNum
                                # with UserNumber now I can get user frend global file 
				# need usr globablfile name #uns2path

                        # convert frend file name to sf.# ,sf.1 is default file uffn2usfn(uffn)
uns="2:"+ unum              # User Node String set to user 4 this would be done via system list   
#upath=adnod.uns2path(uns,urpath)    # all Paths may be set by globals from FREND this will interface with system security
upath="needtoinput"
usfn="s.10"                 # NAF - search s.0 for SF name ? and return SF#- need to set up User 4 s.0
ugpath=upath+usfn
ugnvals=[]
ugfvals=[]
#stuff= pdh_files.rduglobf(ugpath,ugnvals,ugfvals)#open frend global file for read     
#curnode=str(ugnvals[0])        # globals returned from frend file per oder of function
                                  # strip off /n
                                  # look for values
                                  #   globals are GL.Name Value
                                  # Read until EOF find all GL.Name if name matches Global Name assign value
                                  # Global $CURMENU,$CURNODE,$HELPLEV,$LASTMLEV,$MODE,$NOABORT,$NODECRIT,$NOPROMPT,$RFCON,$TERMID
                                  #,$ZONE,$NODECRIT
                                  # Get user input - This will be done via a GUI twinker
                                  # Front End Commands
                                   # ! executes a program - programs are found insystem tree
                                  # + executes a user command file
                                  # - execute a global command file User 0
                                  # : executes a front end command
                                  # $ sets or unsets a Global Parameter
                                  # # moves to a new interactive Menu
fec=input("Enter Front End Command")  # this is a lot of what front end does 
if fec[0] == "!" :           #  then
    command='python ip_rev1.py'
    os.system(command)             # Input processor needs to return 
