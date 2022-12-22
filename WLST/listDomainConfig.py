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
def appendCSV(lineCSV, item):
  if (lineCSV == ""):
    lineCSV = item
  else:
    lineCSV = lineCSV+','+item
  return lineCSV
# 
# Concatenate the targets into a comma separated values list.
def listTargets(targetList):
  targetCSV = ""
  for target in targetList:
    targetCSV = appendCSV(targetCSV, target.getName()+' ('+target.getType()+')')
  return targetCSV
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
  migratableTargets = cmo.getMigratableTargets()
  print lineSeperator
  print 'Check if MigrationBasis for all clusters is database\n'
  print 'ClusterName,MigrationBasis,DataSourceForAutomaticMigration,WeblogicPluginEnabled,FrontendHost,FrontendHTTPPort,FrontendHTTPSPort'
  for cluster in clusters:
    clusterCSV = ""
    clusterCSV = appendCSV(clusterCSV, cluster.getName())
    clusterCSV = appendCSV(clusterCSV, cluster.getMigrationBasis())
    if (cluster.getDataSourceForAutomaticMigration() != None):
      clusterCSV = appendCSV(clusterCSV, cluster.getDataSourceForAutomaticMigration().getName())
    else:
      clusterCSV = appendCSV(clusterCSV, "")
    clusterCSV = appendCSV(clusterCSV, bool2str(cluster.isWeblogicPluginEnabled()))
    clusterCSV = appendCSV(clusterCSV, optional2str(cluster.getFrontendHost()))
    clusterCSV = appendCSV(clusterCSV, str(cluster.getFrontendHTTPPort()))
    clusterCSV = appendCSV(clusterCSV, str(cluster.getFrontendHTTPSPort()))
    print clusterCSV
  print '\n'+lineSeperator
  print 'List Servers and their Transaction Log Stores\n'
  cd('/')
  print 'ServerName,Machine,DataSourceName,Enabled,WeblogicPluginEnabled,FrontendHost,FrontendHTTPPort,FrontendHTTPSPort'
  for server in servers:
    serverCSV = ""
    serverName = server.getName()
    serverCSV = appendCSV(serverCSV, serverName)
    if (server.getMachine() != None):
      serverCSV = appendCSV(serverCSV,server.getMachine().getName())
    else:
      serverCSV = appendCSV(serverCSV, 'None')
    cd('/Servers/' + serverName + '/TransactionLogJDBCStore/' + serverName)
    if (cmo.getDataSource() != None): 
      serverCSV = appendCSV(serverCSV, cmo.getDataSource().getName())
    else:
      serverCSV = appendCSV(serverCSV, 'None')
    serverCSV = appendCSV(serverCSV,bool2str(cmo.isEnabled()))
    serverCSV = appendCSV(serverCSV, bool2str(server.isWeblogicPluginEnabled()))
    webServer = server.getWebServer()
    serverCSV = appendCSV(serverCSV,optional2str(webServer.getFrontendHost()))
    serverCSV = appendCSV(serverCSV,str(webServer.getFrontendHTTPPort()))
    serverCSV = appendCSV(serverCSV,str(webServer.getFrontendHTTPSPort()))
    print serverCSV
  print '\n'+lineSeperator
  print 'List existing File persistent stores... \n'
  cd('/')
  print 'FileStoreName,Targets,Determined JDBCStoreName'
  for fileStore in cmo.getFileStores():
      fileStoreName = fileStore.getName()
      jdbcStoreName = re.sub('(File)?Store', 'JdbcStore', fileStoreName)
      cd('/')
      targetCSV = listTargets(fileStore.getTargets())
      print fileStoreName+', "'+targetCSV+'"',','+jdbcStoreName
  print '\n'+lineSeperator
  print 'List existing JDBC persistent stores... \n'
  cd('/')
  print 'JDBCStoreName,Targets'
  for jdbcStore in cmo.getJDBCStores():
      jdbcStoreName = jdbcStore.getName()
      cd('/')
      targetCSV = listTargets(jdbcStore.getTargets())
      print jdbcStoreName+', "'+targetCSV +'"'
  print '\n'+lineSeperator
  print 'List JMS Servers\n'
  cd('/')
  print 'JMS Server,FileStore,Targets,TemporaryTemplateResource,TemporaryTemplateName'
  for jmsServer in cmo.getJMSServers():
      jmsServerName = jmsServer.getName()
      cd('/JMSServers/'+jmsServerName)
      persistenceStore = cmo.getPersistentStore()
      if (persistenceStore != None):
        fileStoreName = cmo.getPersistentStore().getName()
      targetCSV = listTargets(jmsServer.getTargets())
      print jmsServerName + ',' + fileStoreName  + ',"'+ targetCSV +'",'+ optional2str(cmo.getTemporaryTemplateResource()) + ',' + optional2str(cmo.getTemporaryTemplateName())
  print '\n'+lineSeperator
  print 'Disconnecting from AdminServer'
  disconnect()
  print '\n'+lineSeperator
  print 'Done.'
  print '\n'+lineSeperator
main()
exit()
