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
# List the DataSources from the Server Config.
def listDataSourceConfigs():
  print(lineSeperator)
  print('List Datasource Configurations for domain')
  print(lineSeperator)
  try:
    jdbcSystemResourceSources=domainConfig().getJDBCSystemResources()
    if (len(jdbcSystemResourceSources) > 0):
      # OpenFile
      fileNew=open(dataSourceConfigOutputFile, 'w')
      fileNew.write('Datasource')
      # Connection Pool Parameters
      fileNew.write(',Minimum Capacity')
      fileNew.write(',Maximum Capacity')
      fileNew.write(',Initial Capacity')
      fileNew.write(',Shrink Frequency')
      fileNew.write(',CapacityIncrement')
      fileNew.write(',ConnectionCreationRetryFrequencySeconds')
      fileNew.write(',ConnectionHarvestMaxCount')
      fileNew.write(',ConnectionHarvestTriggerCount')
      fileNew.write(',ConnectionReserveTimeoutSeconds')
      fileNew.write(',CountOfRefreshFailuresTillDisable')
      fileNew.write(',CountOfTestFailuresTillFlush')
      fileNew.write(',HighestNumWaiters')
      fileNew.write(',InactiveConnectionTimeoutSeconds')
      fileNew.write(',PinnedToThread')
      fileNew.write(',ProfileConnectionLeakTimeoutSeconds')
      fileNew.write(',ProfileHarvestFrequencySeconds')
      fileNew.write(',ProfileType')
      fileNew.write(',RemoveInfectedConnections')
      fileNew.write(',SecondsToTrustAnIdlePoolConnection')
      fileNew.write(',StatementCacheSize')
      fileNew.write(',StatementCacheType')
      fileNew.write(',StatementTimeout')
      fileNew.write(',TestConnectionsOnReserve')
      fileNew.write(',TestFrequencySeconds')
      fileNew.write(',TestTableName')
      fileNew.write(',WrapJdbc')
      fileNew.write(',WrapTypes')
      # Driver Parameters
      fileNew.write(',Driver Name')
      fileNew.write(',DB URL')
      fileNew.write(',UsePasswordIndirection')
      fileNew.write(',UseXaDataSourceInterface')
      # Oracle Parameters
      fileNew.write(',ActiveGridlink')
      fileNew.write(',AffinityPolicy')
      fileNew.write(',FanEnabled')
      fileNew.write(',OnsNodeList')
      fileNew.write(',OracleEnableJavaNetFastPath')
      fileNew.write(',OracleOptimizeUtf8Conversion')
      fileNew.write(',OracleProxySession')
      fileNew.write(',ReplayInitiationTimeout')
      fileNew.write(',UseDatabaseCredentials')
      # Data Source Params
      fileNew.write(',AlgorithmType')
      fileNew.write(',FailoverRequestIfBusy')
      fileNew.write(',GlobalTransactionsProtocol')
      fileNew.write(',JNDINames')
      fileNew.write(',KeepConnAfterGlobalTx')
      fileNew.write(',KeepConnAfterLocalTx')
      fileNew.write(',RowPrefetch')
      fileNew.write(',RowPrefetchSize')
      fileNew.write(',Scope')
      fileNew.write(',StreamChunkSize')
      #
      fileNew.write('\n')
      for jdbcSystemResourceSource in jdbcSystemResourceSources:
        dataSourceName = jdbcSystemResourceSource.getName()
        print "DataSource: "+dataSourceName
        cpParams=getMBean('JDBCSystemResources/'+dataSourceName+'/JDBCResource/'+dataSourceName+'/JDBCConnectionPoolParams/'+dataSourceName)
        drvParams=getMBean('JDBCSystemResources/'+dataSourceName+'/JDBCResource/'+dataSourceName+'/JDBCDriverParams/'+dataSourceName)
        oraParams=getMBean('JDBCSystemResources/'+dataSourceName+'/JDBCResource/'+dataSourceName+'/JDBCOracleParams/'+dataSourceName)
        dsParams=getMBean('JDBCSystemResources/'+dataSourceName+'/JDBCResource/'+dataSourceName+'/JDBCDataSourceParams/'+dataSourceName)
        fileNew.write(dataSourceName)
        # Connection Pool Parameters
        fileNew.write(','+str(cpParams.getMinCapacity()))
        fileNew.write(','+str(cpParams.getMaxCapacity()))
        fileNew.write(','+str(cpParams.getInitialCapacity()))
        fileNew.write(','+str(cpParams.getShrinkFrequencySeconds()))        
        fileNew.write(','+str(cpParams.getCapacityIncrement()))
        fileNew.write(','+str(cpParams.getConnectionCreationRetryFrequencySeconds()))
        fileNew.write(','+str(cpParams.getConnectionHarvestMaxCount()))
        fileNew.write(','+str(cpParams.getConnectionHarvestTriggerCount()))
        fileNew.write(','+str(cpParams.getConnectionReserveTimeoutSeconds()))
        fileNew.write(','+str(cpParams.getCountOfRefreshFailuresTillDisable()))
        fileNew.write(','+str(cpParams.getCountOfTestFailuresTillFlush()))
        fileNew.write(','+str(cpParams.getHighestNumWaiters()))
        fileNew.write(','+str(cpParams.getInactiveConnectionTimeoutSeconds()))
        fileNew.write(','+bool2str(cpParams.isPinnedToThread()))
        fileNew.write(','+str(cpParams.getProfileConnectionLeakTimeoutSeconds()))
        fileNew.write(','+str(cpParams.getProfileHarvestFrequencySeconds()))
        fileNew.write(','+str(cpParams.getProfileType()))
        fileNew.write(','+bool2str(cpParams.isRemoveInfectedConnections()))
        fileNew.write(','+str(cpParams.getSecondsToTrustAnIdlePoolConnection()))
        fileNew.write(','+str(cpParams.getStatementCacheSize()))
        fileNew.write(','+str(cpParams.getStatementCacheType()))
        fileNew.write(','+str(cpParams.getStatementTimeout()))
        fileNew.write(','+bool2str(cpParams.isTestConnectionsOnReserve()))
        fileNew.write(','+str(cpParams.getTestFrequencySeconds()))
        fileNew.write(','+cpParams.getTestTableName())
        fileNew.write(','+bool2str(cpParams.isWrapJdbc()))
        fileNew.write(','+bool2str(cpParams.isWrapTypes()))
        # Driver Parameters
        fileNew.write(','+drvParams.getDriverName())
        fileNew.write(','+drvParams.getUrl())
        fileNew.write(','+bool2str(drvParams.isUsePasswordIndirection()))
        fileNew.write(','+bool2str(drvParams.isUseXaDataSourceInterface()))
        # Oracle Parameters
        fileNew.write(','+bool2str(oraParams.isActiveGridlink()))
        fileNew.write(','+oraParams.getAffinityPolicy())
        fileNew.write(','+bool2str(oraParams.isFanEnabled()))
        fileNew.write(',"'+optional2str(oraParams.getOnsNodeList())+'"')
        fileNew.write(','+bool2str(oraParams.isOracleEnableJavaNetFastPath()))
        fileNew.write(','+bool2str(oraParams.isOracleOptimizeUtf8Conversion()))
        fileNew.write(','+bool2str(oraParams.isOracleProxySession()))
        fileNew.write(','+str(oraParams.getReplayInitiationTimeout()))
        fileNew.write(','+bool2str(oraParams.isUseDatabaseCredentials()))
        # Data Source Params
        fileNew.write(','+optional2str(dsParams.getAlgorithmType()))
        fileNew.write(','+bool2str(dsParams.isFailoverRequestIfBusy()))
        fileNew.write(','+optional2str(dsParams.getGlobalTransactionsProtocol()))
        jndiNameList=""
        for jndiName in dsParams.getJNDINames():
          if (jndiNameList == ""):
            jndiNameList = jndiName
          else:
            jndiNameList = jndiNameList + ',' + jndiName
        fileNew.write(',"'+jndiNameList+'"')
        fileNew.write(','+bool2str(dsParams.isKeepConnAfterGlobalTx()))
        fileNew.write(','+bool2str(dsParams.isKeepConnAfterLocalTx()))
        fileNew.write(','+bool2str(dsParams.isRowPrefetch()))
        fileNew.write(','+str(dsParams.getRowPrefetchSize()))
        fileNew.write(','+optional2str(dsParams.getScope()))
        fileNew.write(','+str(dsParams.getStreamChunkSize()))
        # end        
        fileNew.write('\n')
      fileNew.flush()
      fileNew.close()
    print(lineSeperator)      
  except:
    apply(traceback.print_exception, sys.exc_info())
    exit(exitcode=1)
#
# List the DataSource Runtimes from the DomainConfig.
def listDataSourceRuntimes():
  try:
    print(lineSeperator)
    print('List Datasource Runtimes for domain')
    print(lineSeperator)
    allServers=domainRuntimeService.getServerRuntimes();
    if (len(allServers) > 0):
      # OpenFile
      fileNew=open(dataSourceRuntimeOutputFile, 'w')
      fileNew.write('ServerName, DataSourceName')
      fileNew.write(',ActiveConnectionsAverageCount')
      fileNew.write(',ActiveConnectionsCurrentCount')
      fileNew.write(',ActiveConnectionsHighCount')
      fileNew.write(',ConnectionDelayTime')
      fileNew.write(',ConnectionsTotalCount')
      fileNew.write(',CurrCapacity')
      fileNew.write(',CurrCapacityHighCount')
      fileNew.write(',DeploymentState')
      fileNew.write(',FailedReserveRequestCount')
      fileNew.write(',FailuresToReconnectCount')
      fileNew.write(',HighestNumAvailable')
      fileNew.write(',HighestNumUnavailable')
      fileNew.write(',LeakedConnectionCount')
      fileNew.write(',ModuleId')
      fileNew.write(',NumAvailable')
      fileNew.write(',NumUnavailable')
      fileNew.write(',Parent')
      fileNew.write(',PrepStmtCacheAccessCount')
      fileNew.write(',PrepStmtCacheAddCount')
      fileNew.write(',PrepStmtCacheCurrentSize')
      fileNew.write(',PrepStmtCacheDeleteCount')
      fileNew.write(',PrepStmtCacheHitCount')
      fileNew.write(',PrepStmtCacheMissCount')
      # fileNew.write(',Properties')
      fileNew.write(',ReserveRequestCount')
      fileNew.write(',State')
      fileNew.write(',Type')
      fileNew.write(',VersionJDBCDriver')
      fileNew.write(',WaitingForConnectionCurrentCount')
      fileNew.write(',WaitingForConnectionFailureTotal')
      fileNew.write(',WaitingForConnectionHighCount')
      fileNew.write(',WaitingForConnectionSuccessTotal')
      fileNew.write(',WaitingForConnectionTotal')
      fileNew.write(',WaitSecondsHighCount\n')
      #
      for wlsServer in allServers:
        print 'WLS Server '+wlsServer.getName()
        jdbcServiceRT = wlsServer.getJDBCServiceRuntime();
        dataSources = jdbcServiceRT.getJDBCDataSourceRuntimeMBeans();
        if (len(dataSources) > 0):
            for dataSource in dataSources:
                print 'Datasource '+dataSource.getName()
                fileNew.write(wlsServer.getName())
                fileNew.write(',' + dataSource.getName())
                fileNew.write(',' + str(dataSource.getActiveConnectionsAverageCount()))
                fileNew.write(',' + str(dataSource.getActiveConnectionsCurrentCount()))
                fileNew.write(',' + str(dataSource.getActiveConnectionsHighCount()))
                fileNew.write(',' + str(dataSource.getConnectionDelayTime()))
                fileNew.write(',' + str(dataSource.getConnectionsTotalCount()))
                fileNew.write(',' + str(dataSource.getCurrCapacity()))
                fileNew.write(',' + str(dataSource.getCurrCapacityHighCount()))
                fileNew.write(',' + str(dataSource.getDeploymentState()))
                fileNew.write(',' + str(dataSource.getFailedReserveRequestCount()))
                fileNew.write(',' + str(dataSource.getFailuresToReconnectCount()))
                fileNew.write(',' + str(dataSource.getHighestNumAvailable()))
                fileNew.write(',' + str(dataSource.getHighestNumUnavailable()))
                fileNew.write(',' + str(dataSource.getLeakedConnectionCount()))
                fileNew.write(',' + dataSource.getModuleId())
                fileNew.write(',' + str(dataSource.getNumAvailable()))
                fileNew.write(',' + str(dataSource.getNumUnavailable()))
                fileNew.write(',' + dataSource.getParent().getName())
                fileNew.write(',' + str(dataSource.getPrepStmtCacheAccessCount()))
                fileNew.write(',' + str(dataSource.getPrepStmtCacheAddCount()))
                fileNew.write(',' + str(dataSource.getPrepStmtCacheCurrentSize()))
                fileNew.write(',' + str(dataSource.getPrepStmtCacheDeleteCount()))
                fileNew.write(',' + str(dataSource.getPrepStmtCacheHitCount()))
                fileNew.write(',' + str(dataSource.getPrepStmtCacheMissCount()))
                # fileNew.write(',' + dataSource.getProperties())
                fileNew.write(',' + str(dataSource.getReserveRequestCount()))
                fileNew.write(',' + dataSource.getState())
                fileNew.write(',' + dataSource.getType())
                fileNew.write(',' + dataSource.getVersionJDBCDriver())
                fileNew.write(',' + str(dataSource.getWaitingForConnectionCurrentCount()))
                fileNew.write(',' + str(dataSource.getWaitingForConnectionFailureTotal()))
                fileNew.write(',' + str(dataSource.getWaitingForConnectionHighCount()))
                fileNew.write(',' + str(dataSource.getWaitingForConnectionSuccessTotal()))
                fileNew.write(',' + str(dataSource.getWaitingForConnectionTotal()))
                fileNew.write(',' + str(dataSource.getWaitSecondsHighCount()))
                fileNew.write('\n')
      fileNew.flush()
      fileNew.close()
    print(lineSeperator)
  except:
    apply(traceback.print_exception, sys.exc_info())
    exit(exitcode=1)    
#
#
def main():
  try:
    print(lineSeperator)
    print ('Connect to the AdminServer: '+adminServerName)
    connectToadminServer(adminUrl, adminServerName)
    print(lineSeperator)
    listDataSourceConfigs()
    listDataSourceRuntimes()
    print(lineSeperator)
    print('Done...')
    print(lineSeperator)
  except NameError, e:
    print('Apparently properties not set.')
    print "Please check the property: ", sys.exc_info()[0], sys.exc_info()[1]
    usage()
  except:
    apply(traceback.print_exception, sys.exc_info())
    exit(exitcode=1)
#
main();