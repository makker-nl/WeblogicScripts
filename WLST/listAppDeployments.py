#############################################################################
# List Application Deployments on a domain
#
# @author Martien van den Akker, Oracle Nederland B.V.
# @version 1.0, 2023-01-06
#
#############################################################################
# Modify these values as necessary
import sys, traceback
scriptName = sys.argv[0]
#
appDeploymentsOutputFile="listAppDeployments_"+environment+".csv"
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
# List the DataSources from the Server Config.
def listAppDeployments():
  print(lineSeperator)
  print('List App Deployments for domain')
  print(lineSeperator)
  try:
    appDeployments=domainConfig().getAppDeployments()
    if (len(appDeployments) > 0):
      # OpenFile
      fileNew=open(appDeploymentsOutputFile, 'w')
      headerCSV=""
      headerCSV=appendCSV(headerCSV, 'Application')
      headerCSV=appendCSV(headerCSV, 'Type')
      headerCSV=appendCSV(headerCSV, 'ModuleType')
      headerCSV=appendCSV(headerCSV, 'PlanDir')
      headerCSV=appendCSV(headerCSV, 'Targets')
      headerCSV=appendCSV(headerCSV, 'DeploymentOrder')    
      #
      fileNew.write(headerCSV+'\n')
      for appDeployment in appDeployments:
        lineCSV=""
        appDeploymentName = appDeployment.getName()
        print ". "+appDeploymentName
        lineCSV=appendCSV(lineCSV, appDeploymentName)
        lineCSV=appendCSV(lineCSV, appDeployment.getType())
        lineCSV=appendCSV(lineCSV, appDeployment.getModuleType())
        lineCSV=appendCSV(lineCSV, optional2str(appDeployment.getPlanDir()))
        lineCSV=appendCSV(lineCSV, '"'+ listTargets(appDeployment.getTargets())+'"')
        lineCSV=appendCSV(lineCSV, str(appDeployment.getDeploymentOrder()))
        #
        fileNew.write(lineCSV+'\n')
        # end        
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