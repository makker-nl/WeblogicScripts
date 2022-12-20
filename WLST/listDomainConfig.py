#############################################################################
# List Datasource Configs and Runtimes on a domain
#
# @author Martien van den Akker, Oracle Nederland B.V.
# @version 3.0, 2022-12-13
#
#############################################################################
# Modify these values as necessary
import sys, traceback
scriptName = sys.argv[0]
#
dataSourceRuntimeOutputFile="listDataSourceRuntimes_"+environment+".csv"
dataSourceConfigOutputFile="listDataSourceConfigs_"+environment+".csv"
#
pad='                                                                               '
lineSeperator='__________________________________________________________________________________'
#
#
def usage():
  print 'Call script as: '
  print 'Windows: wlst.cmd '+scriptName+' -loadProperties localhost.properties'
  print 'Linux: wlst.sh '+scriptName+' -loadProperties environment.properties'
  print 'Property file should contain the following properties: '
  print "adminUrl=darlin-vce:7001"
  print "adminUser=weblogic"
  print "adminPwd=welcome1"
#
#
def connectToadminServer(adminUrl, adminServerName):
  print(lineSeperator)
  print('Try to connect to the AdminServer')
  try:
    connect(userConfigFile=usrCfgFile, userKeyFile=usrKeyFile, url=adminUrl)
  except NameError, e:
    print('Apparently user config properties usrCfgFile and usrKeyFile not set.')
    print('Try to connect to the AdminServer adminUser and adminPwd properties')
    connect(adminUser, adminPwd, adminUrl)
#
#
def bool2str(boolPar):
  result='false'
  if (boolPar == None):
    result = 'none'
  else:
    if (boolPar==1):
      result='true'
  return result
#
#
def optional2str(optionalPar):
  result='None'
  if (optionalPar!=None):
    result=optionalPar
  return result
#
#
def main():
  print lineSeperator
  print 'Connect to the AdminServer: '+adminServerName
  connectToadminServer(adminUrl, adminServerName)
  print lineSeperator
  print 'Determining domain configuration\n'
  cd('/')
  servers = cmo.getServers()
  standaloneServers = [x for x in servers if x.getCluster() == None]
  clusters = cmo.getClusters()
  print lineSeperator
  print 'Check if MigrationBasis for all clusters is database\n'
  cd('/')
  print 'ClusterName, MigrationBasis'
  for cluster in clusters:
      migrationBasis = cluster.getMigrationBasis()
      print cluster.getName() + ', '+ migrationBasis
  print '\n'+lineSeperator
  print 'List Transaction Log Stores\n'
  cd('/')
  print 'ServerName, DataSourceName, Enabled'
  for server in servers:
      serverName = server.getName()
      cd('/Servers/' + serverName + '/TransactionLogJDBCStore/' + serverName)
      dataSourceName = 'None'
      if (cmo.getDataSource() != None): 
        dataSourceName = cmo.getDataSource().getName()
      isEnabled = bool2str(cmo.isEnabled())
      print serverName +','+ dataSourceName + ',' + isEnabled
  print '\n'+lineSeperator
  print 'List existing File persistent stores... \n'
  cd('/')
  print 'FileStoreName, Targets, Determined JDBCStoreName'
  for fileStore in cmo.getFileStores():
      fileStoreName = fileStore.getName()
      jdbcStoreName = re.sub('(File)?Store', 'JdbcStore', fileStoreName)
      cd('/')
      targetList = ""
      for target in fileStore.getTargets():
        if (targetList == ""):
          targetList = target.getName()
        else:
          targetList = targetList + ',' + target.getName()
      print fileStoreName+', "'+targetList+'"',','+jdbcStoreName
  print '\n'+lineSeperator
  print 'List existing JDBC persistent stores... \n'
  cd('/')
  print 'JDBCStoreName, Targets'
  for jdbcStore in cmo.getJDBCStores():
      jdbcStoreName = jdbcStore.getName()
      cd('/')
      targetList = ""
      for target in jdbcStore.getTargets():
        if (targetList == ""):
          targetList = target.getName()
        else:
          targetList = targetList + ',' + target.getName()
      print jdbcStoreName+', "'+targetList+'"'
  print '\n'+lineSeperator
  print 'List JMS Servers\n'
  cd('/')
  print 'JMS Server, FileStore, TemporaryTemplateResource, TemporaryTemplateName'
  for jmsServer in cmo.getJMSServers():
      jmsServerName = jmsServer.getName()
      cd('/JMSServers/'+jmsServerName)
      fileStoreName = cmo.getPersistentStore().getName()
      print jmsServerName + ',' + fileStoreName  + ',' + optional2str(cmo.getTemporaryTemplateResource()) + ',' + optional2str(cmo.getTemporaryTemplateName())
  print '\n'+lineSeperator
  print 'Disconnecting from AdminServer'
  disconnect()
  print '\n'+lineSeperator
  print 'Done.'
  print '\n'+lineSeperator
main()
exit()
