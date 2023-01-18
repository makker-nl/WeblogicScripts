#############################################################################
# Get Application Deployment target properties of a domain
#
# @author Martien van den Akker, Oracle Nederland B.V.
# @version 1.0, 2023-01-09
#
#############################################################################
# Modify these values as necessary
import sys, traceback
scriptName = sys.argv[0]
#
appDeploymentsOutputFile="appdeployment_"+environment+".properties"
appDeployProp="appDeployments"
srvrTargetProp=".targets.servers"
cltrTargetProp=".targets.clusters"
migTargetProp=".targets.migratable"
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
  print('Try to connect to the AdminServer: '+adminServerName+"\n")
  try:
    connect(userConfigFile=usrCfgFile, userKeyFile=usrKeyFile, url=adminUrl)
  except NameError, e:
    print('Apparently user config properties usrCfgFile and usrKeyFile not set.')
    print('Try to connect to the AdminServer adminUser and adminPwd properties')
    connect(adminUser, adminPwd, adminUrl)
#
# Append an item to a property list.
def appendPropList(lineCSV, property, item):
  if (lineCSV == ""):
    lineCSV = property+'='+item
  else:
    lineCSV = lineCSV+','+item
  return lineCSV
#
#
def name2prop(name):
  prop=name.lower().replace(" ", "_").replace(".", "-").replace("#", "-")
  return prop
#
# List the DataSources from the Server Config.
def listAppDeployments():
  try:
    appDeployments=domainConfig().getAppDeployments()
    if (len(appDeployments) > 0):
      print(lineSeperator)
      # OpenFile
      fileNew=open(appDeploymentsOutputFile, 'w')
      # First create and write a list of all the App Deployments.
      print('List App Deployments for domain')
      appDeploymentsCSV=""
      for appDeployment in appDeployments:
        appDeploymentName = appDeployment.getName()
        print ". "+appDeploymentName
        appDeploymentsCSV=appendPropList(appDeploymentsCSV, appDeployProp, name2prop(appDeploymentName))
        #
      fileNew.write(appDeploymentsCSV+'\n')
      print(lineSeperator)
      # Now loop again, but create target properties for each deployment.
      print('Create target properties per App Deployment')
      for appDeployment in appDeployments:
        serverTargets=""
        clusterTargets=""
        migratableTargets=""
        appDeploymentName = appDeployment.getName()
        print ". "+appDeploymentName
        appDeploymentProp=name2prop(appDeploymentName)
        fileNew.write(appDeploymentProp+".name="+appDeploymentName+'\n')
        targets=appDeployment.getTargets()
        for target in targets:
          if target.getType() == "Cluster":
            clusterTargets=appendPropList(clusterTargets, appDeploymentProp+cltrTargetProp, target.getName())
          elif target.getType() == "Server":
            serverTargets=appendPropList(serverTargets, appDeploymentProp+srvrTargetProp, target.getName())
          else:
            migratableTargets=appendPropList(migratableTargets, appDeploymentProp+migTargetProp, target.getName())
        if len(clusterTargets) > 0:
          fileNew.write(clusterTargets+'\n')
        if len(serverTargets) > 0:
          fileNew.write(serverTargets+'\n')
        if len(migratableTargets) > 0:
          fileNew.write(migratableTargets+'\n')
      # end        
      fileNew.flush()
      fileNew.close()
  except:
    apply(traceback.print_exception, sys.exc_info())
    exit(exitcode=1)
#
#
def main():
  try:
    print(lineSeperator)
    connectToadminServer(adminUrl, adminServerName)
    print(lineSeperator)
    listAppDeployments()
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