#############################################################################
# Test Datasources on a domain
#
# @author Martien van den Akker, Darwin-IT Professionals
# @version 2.1, 2016-10-04
#
#############################################################################
# Modify these values as necessary
import sys, traceback
scriptName = sys.argv[0]
#
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
  print "adminUrl=hhs-sbm3015:7001"
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
def getJdbcSystemResourceSources():
  try:
    print(lineSeperator)
    print('Get DataSources')
    jdbcSystemResourceSources=cmo.getJDBCSystemResources()
    return jdbcSystemResourceSources
  except WLSTException:
    message='Exception getting jdbcSystemResourceSources'
    print (message)
    raise Exception(message)
#
#
def listDS():
  try:
    print(lineSeperator)
    print('List datasources for domain')
    print(lineSeperator)
    jdbcSystemResourceSources=getJdbcSystemResourceSources()
    if (len(jdbcSystemResourceSources) > 0):
      print('Datasource                                                  '[:30]+'\tMinCpy\tMaxCpy\tIntCpy\tShrkFcy\tTstFcy\tRetryFcy\tUrl')
      for jdbcSystemResourceSource in jdbcSystemResourceSources:
        dataSourceName = jdbcSystemResourceSource.getName()
        cpParams=getMBean('JDBCSystemResources/'+dataSourceName+'/JDBCResource/'+dataSourceName+'/JDBCConnectionPoolParams/'+dataSourceName)
        drvParams=getMBean('JDBCSystemResources/'+dataSourceName+'/JDBCResource/'+dataSourceName+'/JDBCDriverParams/'+dataSourceName)
        dataSourceNamePad=dataSourceName+pad
        print dataSourceNamePad[:30]+'\t'+str(cpParams.getMinCapacity())+'\t'+str(cpParams.getMaxCapacity())+'\t'+str(cpParams.getInitialCapacity())+'\t'+str(cpParams.getShrinkFrequencySeconds())+'\t'+str(cpParams.getTestFrequencySeconds())+'\t'+str(cpParams.getConnectionCreationRetryFrequencySeconds())+'\t'+drvParams.getUrl()
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
    listDS()
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

