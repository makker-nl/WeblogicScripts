#############################################################################
# List System Components of FMW Domain
#
# @author Martien van den Akker, Darwin-IT Professionals
# @version 1.1, 2017-04-20
#
#############################################################################
# Modify these values as necessary
import sys, traceback
scriptName = sys.argv[0]
#
#
lineSeperator='__________________________________________________________________________________'
pad='                                                                               '
#
#
def usage():
  print 'Call script as: '
  print 'Windows: wlst.cmd '+scriptName+' -loadProperties localhost.properties'
  print 'Linux: wlst.sh '+scriptName+' -loadProperties environment.properties'
  print 'Property file should contain the following properties: '
  print "adminUrl=localhost:7001"
  print "adminUser=weblogic"
  print "adminPwd=welcome1"
#
# Connect To the AdminServer
def connectToAdminServer(adminUrl, adminServerName):
  print(lineSeperator)
  print('Try to connect to the AdminServer')
  try:
    connect(userConfigFile=usrCfgFile, userKeyFile=usrKeyFile, url=adminUrl)
  except NameError, e:
    print('Apparently user config properties usrCfgFile and usrKeyFile not set.')
    print('Try to connect to the AdminServer adminUser and adminPwd properties')
    connect(adminUser, adminPwd, adminUrl)
#
# Get the Servers of Domain 
def getSystemComponents():
  print(lineSeperator)
  print('\nGet SystemComponents from domain')
  serverConfig()
  cd("/")
  sysComponents = cmo.getSystemComponents()
  return sysComponents
#
# Boolean to string
def bool2str(bool):
  result='false'
  if bool:
    result='true'
  return result
#
# Descr system component type
def descSysCompType(sysComponentType):
  result=sysComponentType
  if sysComponentType=='OHS':
    result='Oracle HTTP server'
  elif sysComponentType=='OBIPS':
    result='BI Presentation Service'
  elif sysComponentType=='OBIS':
    result='BI Server'
  elif sysComponentType=='OBISCH':
    result='BI Scheduler'
  elif sysComponentType=='OBICCS':
    result='BI Cluster Controller'   
  elif sysComponentType=='OBIJH':
    result='BI JavaHost'
  else:
    result=sysComponentType
  return result
#
# Start clusters
def showSystemComponents():
  print(lineSeperator)
  print ('Show SystemComponents')
  sysComponents=getSystemComponents()
  #
  if (len(sysComponents) > 0):
    print('SystemComponent                                                  '[:30]+'\t'+'Type                                                                               '[:20]+'\tAutoRestart\tMachine')
    for sysComponent in sysComponents:
      sysCompName = sysComponent.getName()
      sysCompNamePad=sysCompName+pad
      sysCompType=descSysCompType(sysComponent.getComponentType())
      sysCompTypePad=sysCompType+pad
      machine=sysComponent.getMachine()
      if machine is None:
        machineName = 'None'
      else:
        machineName = machine.getName()
      print sysCompNamePad[:30]+'\t'+sysCompTypePad[:20]+'\t'+bool2str(sysComponent.getAutoRestart())+'\t\t'+machineName
  else:
    print('No SystemComponents found!')
  #
  print ('\nFinished showing SystemComponents.')
#
# Main
def main():
  try:
    #
    print(lineSeperator)
    print('\nConnect to the AdminServer: '+adminServerName)
    connectToAdminServer(adminUrl, adminServerName)
    #
    showSystemComponents()
    #
    print('\nExiting...')
    exit()
  except NameError, e:
    print('Apparently properties not set.')
    print "Please check the property: ", sys.exc_info()[0], sys.exc_info()[1]
    usage()
  except:
    apply(traceback.print_exception, sys.exc_info())
    exit(exitcode=1)
#call main()
main()
exit()
