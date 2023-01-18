#############################################################################
# Create WebLogic 12c Domain for WLS 12c Tuning & Troubleshooting workshop
#
# @author Martien van den Akker, Darwin-IT Professionals
# @version 1.0, 2018-01-22
#
#############################################################################
# Modify these values as necessary
import os,sys, traceback
scriptName = sys.argv[0]
wlHome=os.environ["WL_HOME"]
domainsHome=os.environ["DOMAINS_HOME"]
ttDomainName=os.environ["TTDOMAIN_NAME"]
ttDomainHome=domainsHome+'/'+ttDomainName
ttMachineName=os.environ["TTMCN_NAME"]
nmHost=os.environ["NM_HOST"]
nmPort=os.environ["NM_PORT"]
nmType=os.environ["NM_TYPE"]
#
adminServerName='AdminServer';
adminServerPort=os.environ["ADM_PORT"]
#
adminUser='weblogic'
adminPwd='welcome1'
#
ttServerName=os.environ["TTSVR_NAME"]
ttServerPort=os.environ["TTSVR_PORT"]
#
templateHome=wlHome+'/common/templates/wls'
domainTemplate=templateHome+'/wls.jar'
#
nmHome=ttDomainHome+'/nodemanager'
nmPropertyFile=nmHome+'/nodemanager.properties'
#
# Create a Machine
def createMachine(machineName, nmType, nmHost, nmPort):
  cd('/')
  print 'Create a Machine: '+machineName
  create(machineName,'UnixMachine')
  cd('UnixMachine/'+machineName)
  create(machineName,'NodeManager')
  cd('NodeManager/'+machineName)
  set('ListenAddress',nmHost)
  set('ListenPort', int(nmPort))
  set('NMType', nmType)
#
# Create a Managed Server
def createMgdSvr(serverName, listenPort, machineName):
  cd('/')
  print 'Create ManagedServer: '+serverName
  create(serverName, 'Server')
  cd('/Servers/'+serverName)
  print '. Set listen port to: '+str(listenPort)
  #set('ListenAddress',listenAddress)
  set('ListenPort'   ,int(listenPort))
  set('AutoRestart','True')
  set('AutoKillIfFailed','True')
  set('RestartMax', 2)
  set('RestartDelaySeconds', 10)
  print 'Add ManagedServer: '+serverName + 'to machine: '+machineName;
  set('Machine',machineName)
#
# Create a boot properties file.
def createBootPropertiesFile(directoryPath,fileName, username, password):
  print('Create Boot Properties File for folder: '+directoryPath)
  serverDir = File(directoryPath)
  bool = serverDir.mkdirs()
  fileNew=open(directoryPath + '/'+fileName, 'w')
  fileNew.write('username=%s\n' % username)
  fileNew.write('password=%s\n' % password)
  fileNew.flush()
  fileNew.close()
#
# Create a base domain.
def createTTDomain():
  print 'Create Domain';
  print '. Domain template:  \''+domainTemplate+'\''
  print '. Domain Name: \''+ttDomainName+'\''
  print '. Domain Home:  \''+ttDomainHome+'\''
  print '. Admin User:  \''+adminUser+'\'' 
  print '. Admin Password:  \''+adminPwd+'\''
  createDomain(domainTemplate,ttDomainHome,adminUser,adminPwd)
  # Create boot properties file for AdminServer and nodemanager
  createBootPropertiesFile(ttDomainHome+'/servers/AdminServer/security','boot.properties',adminUser,adminPwd)
  createBootPropertiesFile(ttDomainHome+'/config/nodemanager','nm_password.properties',adminUser,adminPwd)
  # Re-read the domain
  readDomain(ttDomainHome);
  # Set the domain to productionMode
  cmo.setProductionModeEnabled(true);
  # Create a Machine definition
  createMachine(ttMachineName, nmType, nmHost, nmPort)
  # Create a Managed Server
  createMgdSvr(ttServerName, ttServerPort, ttMachineName)
  # Create boot properties file for TTServer
  createBootPropertiesFile(ttDomainHome+'/servers/'+ttServerName+'/security','boot.properties',adminUser,adminPwd)
  #  Update the Domain
  updateDomain();
  closeDomain();
#
# Update the Nodemanager Properties
def updateNMProps(nmPropertyFile, nodeMgrListenAddress, nodeMgrListenPort, nodeMgrType):
  nmProps = ''
  print ('Read Nodemanager properties file%s: ' % nmPropertyFile)
  f = open(nmPropertyFile)
  for line in f.readlines():
    if line.strip().startswith('ListenPort'):
      line = 'ListenPort=%s\n' % nodeMgrListenPort
    elif line.strip().startswith('ListenAddress'):
      line = 'ListenAddress=%s\n' % nodeMgrListenAddress
    elif line.strip().startswith('SecureListener'):
       if nodeMgrType == 'ssl':
         line = 'SecureListener=true\n'
       else:
         line = 'SecureListener=false\n'
    # making sure these properties are set to true:
    elif line.strip().startswith('QuitEnabled'):
      line = 'QuitEnabled=%s\n' % 'true'
    elif line.strip().startswith('CrashRecoveryEnabled'):
      line = 'CrashRecoveryEnabled=%s\n' % 'true'
    elif line.strip().startswith('weblogic.StartScriptEnabled'):
      line = 'weblogic.StartScriptEnabled=%s\n' % 'true'
    elif line.strip().startswith('weblogic.StopScriptEnabled'):
      line = 'weblogic.StopScriptEnabled=%s\n' % 'true'         
    nmProps = nmProps + line
  # print nmProps
  # Backup file
  nmPropertyFileOrg=nmPropertyFile+'.org'
  print ('Rename File %s to %s ' % (nmPropertyFile, nmPropertyFileOrg))
  os.rename(nmPropertyFile, nmPropertyFileOrg)  
  # Save New File
  print ('\nNow save the changed property file to %s' % nmPropertyFile)
  fileNew=open(nmPropertyFile, 'w')
  fileNew.write(nmProps)
  fileNew.flush()
  fileNew.close()
#
def startDomain():
  print 'Start Nodemanager'
  startNodeManager(verbose='true', NodeManagerHome=nmHome, ListenPort=nmPort, ListenAddress=nmHost);
  print 'Connect to the Node Manager';
  nmConnect(adminUser, adminPwd, nmHost, nmPort, ttDomainName, ttDomainHome, nmType);
  print 'Start AdminServer';
  nmStart(adminServerName);
  print 'Connect to the AdminServer';
  connect(adminUser, adminPwd);
  print 'Start ManagedServer: '+ttServerName;
  start(ttServerName);
#
def main():
  try:
    #
    createTTDomain()
    #
    updateNMProps(nmPropertyFile, nmHost, nmPort, nmType)
    #
    startDomain()
    #    
    print("\nExiting...")
    exit()
  except:
    apply(traceback.print_exception, sys.exc_info())
    exit(exitcode=1)
#call main()
main()
