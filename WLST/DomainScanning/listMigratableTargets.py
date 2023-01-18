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
migratableTargetsOutputFile="listMigratableTargets_"+environment+".csv"
jtaMigratableTargetsOutputFile="listJTAMigratableTargets_"+environment+".csv"
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
# Append an item to a CSV list.
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
# Concatenate the servers into a comma separated values list.
def listServers(serverList):
  serverCSV = ""
  for server in serverList:
    serverCSV = appendCSV(serverCSV, server.getName())
  return serverCSV
# 
# Concatenate the strings in a list into a comma separated values list.
def listStrings(stringList):
  stringCSV = ""
  for item in stringList:
    stringCSV = appendCSV(stringCSV, item)
  return stringCSV
#
#
def main():
  print lineSeperator
  print 'Connect to the AdminServer: '+adminServerName
  connectToadminServer(adminUrl, adminServerName)
  print lineSeperator
  print 'List Migratable Targets\n'
  cd('/')
  try:
    migratableTargets = cmo.getMigratableTargets()
    if (len(migratableTargets) > 0):
      # OpenFile
      fileNew=open(migratableTargetsOutputFile, 'w')
      headers=""
      headers=appendCSV(headers,'Name')
      headers=appendCSV(headers,'Cluster')
      headers=appendCSV(headers,'MigrationPolicy')
      headers=appendCSV(headers,'Type')
      headers=appendCSV(headers,'AllCandidateServers')
      headers=appendCSV(headers,'UserPreferredServer')
      headers=appendCSV(headers,'ConstrainedCandidateServers')
      headers=appendCSV(headers,'AdditionalMigrationAttempts')
      headers=appendCSV(headers,'Critical')
      headers=appendCSV(headers,'DynamicallyCreated')
      headers=appendCSV(headers,'MillisToSleepBetweenAttempts')
      headers=appendCSV(headers,'NonLocalPostAllowed')
      headers=appendCSV(headers,'NumberOfRestartAttempts')
      headers=appendCSV(headers,'PostScript')
      headers=appendCSV(headers,'PostScriptFailureFatal')
      headers=appendCSV(headers,'PreScript')
      headers=appendCSV(headers,'RestartOnFailure')
      headers=appendCSV(headers,'SecondsBetweenRestarts')
      headers=appendCSV(headers,'Tags')
      fileNew.write(headers+'\n')
      for migTarget in migratableTargets:
        print '. '+migTarget.getName()
        migTargetCSV=""
        migTargetCSV=appendCSV(migTargetCSV, migTarget.getName())
        migTargetCSV=appendCSV(migTargetCSV, migTarget.getCluster().getName())
        migTargetCSV=appendCSV(migTargetCSV, migTarget.getMigrationPolicy())
        migTargetCSV=appendCSV(migTargetCSV, migTarget.getType())
        migTargetCSV=appendCSV(migTargetCSV, '"'+listServers(migTarget.getAllCandidateServers())+'"')
        migTargetCSV=appendCSV(migTargetCSV, migTarget.getUserPreferredServer().getName())
        migTargetCSV=appendCSV(migTargetCSV, '"'+listServers(migTarget.getConstrainedCandidateServers())+'"')
        migTargetCSV=appendCSV(migTargetCSV, str(migTarget.getAdditionalMigrationAttempts()))
        migTargetCSV=appendCSV(migTargetCSV, bool2str(migTarget.isCritical()))
        migTargetCSV=appendCSV(migTargetCSV, bool2str(migTarget.isDynamicallyCreated()))
        migTargetCSV=appendCSV(migTargetCSV, str(migTarget.getMillisToSleepBetweenAttempts()))
        migTargetCSV=appendCSV(migTargetCSV, bool2str(migTarget.isNonLocalPostAllowed()))
        migTargetCSV=appendCSV(migTargetCSV, str(migTarget.getNumberOfRestartAttempts()))
        migTargetCSV=appendCSV(migTargetCSV, str(migTarget.getPostScript()))
        migTargetCSV=appendCSV(migTargetCSV, bool2str(migTarget.isPostScriptFailureFatal()))
        migTargetCSV=appendCSV(migTargetCSV, str(migTarget.getPreScript()))
        migTargetCSV=appendCSV(migTargetCSV, bool2str(migTarget.getRestartOnFailure()))
        migTargetCSV=appendCSV(migTargetCSV, str(migTarget.getSecondsBetweenRestarts()))
        migTargetCSV=appendCSV(migTargetCSV, '"'+listStrings(migTarget.getTags())+'"')
        fileNew.write(migTargetCSV+'\n')
        # end
      fileNew.flush()
      fileNew.close()
    else:
      print 'No Migratable Targets configured!'    
    print(lineSeperator)  
    print 'List Server JTA Migratable Targets'
    servers = cmo.getServers()
    clusterServers = [svr for svr in servers if svr.getCluster() != None]
    if (len(clusterServers) > 0):
      # OpenFile
      fileNew=open(jtaMigratableTargetsOutputFile, 'w')
      headers=""
      headers=appendCSV(headers,'ServerName')
      headers=appendCSV(headers,'JTAMigratableTargetName')
      headers=appendCSV(headers,'MigrationPolicy')
      headers=appendCSV(headers,'Type')
      headers=appendCSV(headers,'AllCandidateServers')
      headers=appendCSV(headers,'HostingServer')
      headers=appendCSV(headers,'UserPreferredServer')
      headers=appendCSV(headers,'ConstrainedCandidateServers')
      headers=appendCSV(headers,'AdditionalMigrationAttempts')
      headers=appendCSV(headers,'Critical')
      headers=appendCSV(headers,'DynamicallyCreated')
      headers=appendCSV(headers,'MillisToSleepBetweenAttempts')
      headers=appendCSV(headers,'NonLocalPostAllowed')
      headers=appendCSV(headers,'NumberOfRestartAttempts')
      headers=appendCSV(headers,'PostScript')
      headers=appendCSV(headers,'PostScriptFailureFatal')
      headers=appendCSV(headers,'PreScript')
      headers=appendCSV(headers,'RestartOnFailure')
      headers=appendCSV(headers,'SecondsBetweenRestarts')
      headers=appendCSV(headers,'Tags')
      fileNew.write(headers+'\n')
    
      for svr in clusterServers:
        migTarget = svr.getJTAMigratableTarget()
        if (migTarget != None):
          print '. '+svr.getName()+'-'+migTarget.getName()
          migTargetCSV=""
          migTargetCSV=appendCSV(migTargetCSV, svr.getName())
          migTargetCSV=appendCSV(migTargetCSV, migTarget.getName())
          migTargetCSV=appendCSV(migTargetCSV, migTarget.getMigrationPolicy())
          migTargetCSV=appendCSV(migTargetCSV, migTarget.getType())
          migTargetCSV=appendCSV(migTargetCSV, '"'+listServers(migTarget.getAllCandidateServers())+'"')
          migTargetCSV=appendCSV(migTargetCSV, migTarget.getHostingServer().getName())
          migTargetCSV=appendCSV(migTargetCSV, migTarget.getUserPreferredServer().getName())
          migTargetCSV=appendCSV(migTargetCSV, '"'+listServers(migTarget.getConstrainedCandidateServers())+'"')    
          migTargetCSV=appendCSV(migTargetCSV, str(migTarget.getAdditionalMigrationAttempts()))
          migTargetCSV=appendCSV(migTargetCSV, bool2str(migTarget.isCritical()))
          migTargetCSV=appendCSV(migTargetCSV, bool2str(migTarget.isDynamicallyCreated()))
          migTargetCSV=appendCSV(migTargetCSV, str(migTarget.getMillisToSleepBetweenAttempts()))
          migTargetCSV=appendCSV(migTargetCSV, bool2str(migTarget.isNonLocalPostAllowed()))
          migTargetCSV=appendCSV(migTargetCSV, str(migTarget.getNumberOfRestartAttempts()))
          migTargetCSV=appendCSV(migTargetCSV, str(migTarget.getPostScript()))
          migTargetCSV=appendCSV(migTargetCSV, bool2str(migTarget.isPostScriptFailureFatal()))
          migTargetCSV=appendCSV(migTargetCSV, str(migTarget.getPreScript()))
          migTargetCSV=appendCSV(migTargetCSV, bool2str(migTarget.getRestartOnFailure()))
          migTargetCSV=appendCSV(migTargetCSV, str(migTarget.getSecondsBetweenRestarts()))
          migTargetCSV=appendCSV(migTargetCSV, '"'+listStrings(migTarget.getTags())+'"')
          fileNew.write(migTargetCSV+'\n')
          # end
        else:
          # Is this even possible?
          print 'No JTA Migratable Target found !'
      fileNew.flush()
      fileNew.close()
    else:
      print 'No Cluster Servers found'
    print '\n'+lineSeperator
    print 'Disconnecting from AdminServer'
    disconnect()
    print '\n'+lineSeperator
    print 'Done.'
    print '\n'+lineSeperator
  except:
    apply(traceback.print_exception, sys.exc_info())
    exit(exitcode=1)
main()
exit()
