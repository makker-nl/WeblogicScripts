#############################################################################
# Deploy SharedFolder to WLS 12c
#
# @author Martien van den Akker, Darwin-IT Professionals
# @version 1.0, 2018-02-08
#
#############################################################################
# Modify these values as necessary
import os,sys, traceback
scriptName = sys.argv[0]
#
appName='SharedFolder'
appSource='dist/SharedFolder/SharedFolder.war'
#
# usage
def usage():
  print "Call script as: "
  print "Windows: wlst.cmd "+scriptName+" -loadProperties localhost.properties"
  print "Linux: wlst.sh "+scriptName+" -loadProperties environment.properties"
  print "Property file should contain the following properties: "
  print "adminUrl=localhost:7001"
  print "adminUser=weblogic"
print "adminPwd=welcome1"
#
# Deploy the application
def deployApplication(appName, appSource, targetServerName):
  print 'Deploying application ' + appName + '.'
  progress = deploy(appName=appName,path=appSource,targets=targetServerName)
  # Wait for deploy to complete
  while progress.isRunning():
	  pass
  print 'Application ' + appName + ' deployed.'
#
#
def main():
  # Connect to administration server
  try:
    connect(adminUser, adminPwd, adminUrl)
    #
    deployApplication(appName, appSource, targetServerName)
    #    
    print("\nExiting...")
    exit()
  except NameError, e:
    print("Apparently properties not set.")
    print "Please check the property: ", sys.exc_info()[0], sys.exc_info()[1]
    usage()
  except:
    apply(traceback.print_exception, sys.exc_info())
    exit(exitcode=1)
#call main()
main()