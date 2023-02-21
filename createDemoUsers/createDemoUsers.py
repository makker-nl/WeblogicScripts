#############################################################################
# Create WebLogic Users and groups
#
# @author Martien van den Akker, Darwin-IT Professionals
# @version 1.1, 2016-07-06
#
#############################################################################
# Modify these values as necessary
import sys, traceback
scriptName = sys.argv[0]
#
#
lineSeperator="__________________________________________________________________________________"
#
#
def usage():
  print "Call script as: "
  print "Windows: wlst.cmd "+scriptName+" -loadProperties localhost.properties"
  print "Linux: wlst.sh "+scriptName+" -loadProperties environment.properties"
  print "Property file should contain the following properties: "
  print "adminUrl=localhost:7001"
  print "adminUser=weblogic"
  print "adminPwd=welcome1"
#
#

from java.io import File
from java.io import FileInputStream
from java.util import Properties
 
 
#Load properties file in java.util.Properties
def loadPropsFile(propsFile):
 inStream = FileInputStream(propsFile)
 props = Properties()
 props.load(inStream) 
  
 return props
#

def connectToadminServer(adminUrl, adminServerName):
  try:
    print(lineSeperator)
    print("Try to connect to the AdminServer")
    try:
      connect(userConfigFile=usrCfgFile, userKeyFile=usrKeyFile, url=adminUrl)
    except NameError, e:
      print("Apparently user config properties usrCfgFile and usrKeyFile not set.")
      print("Try to connect to the AdminServer adminUser and adminPwd properties")
      connect(adminUser, adminPwd, adminUrl)
  except WLSTException:
    message="Apparently AdminServer not Started!"
    print (message)
    raise Exception(message)
#
#
def getRealm(name=None):
  cd("/")
  if name == None:
    realm = cmo.getSecurityConfiguration().getDefaultRealm()
  else:
    realm = cmo.getSecurityConfiguration().lookupRealm(name)
  return realm
#
#
def getAuthenticator(realm, name=None):
  if name == None:
    authenticator = realm.lookupAuthenticationProvider("DefaultAuthenticator")
  else:
    authenticator = realm.lookupAuthenticationProvider(name)
  return authenticator  
#
#
def nvl(testParam, nullValue):
  if testParam != None:
    result=testParam
  else:
    result=nullValue
  return result
#
# Create a WLS User
def createUser(authenticator, userName, userProps):
  print ("Creating user " + userName)
  if authenticator.userExists(userName):
    print ("User "+userName+" already exists.")
  else:
    print ("User "+userName+" does not exist.")
    password=userProps.getProperty(userName+".password")
    description=userProps.getProperty(userName+".description")
    #Create User
    authenticator.createUser(userName, password, description)    
    #Set Properties
    firstName=userProps.getProperty(userName+".firstName")
    lastName=userProps.getProperty(userName+".lastName")
    displayName=nvl(firstName, " ")+" "+nvl(lastName, " ")
    authenticator.setUserAttributeValue(userName,"displayName",displayName.strip())
    email=userProps.getProperty(userName+".email")
    authenticator.setUserAttributeValue(userName,"mail",email)
    title=userProps.getProperty(userName+".title")
    authenticator.setUserAttributeValue(userName,"title",title)
    preferredlanguage=userProps.getProperty(userName+".languagePreference")
    authenticator.setUserAttributeValue(userName,"preferredlanguage",preferredlanguage)
    workPhone=userProps.getProperty(userName+".workPhone")
    authenticator.setUserAttributeValue(userName,"telephonenumber",workPhone)
    homePhone=userProps.getProperty(userName+".homePhone")
    authenticator.setUserAttributeValue(userName,"homePhone",homePhone)
    mobile=userProps.getProperty(userName+".mobile")
    authenticator.setUserAttributeValue(userName,"mobile",mobile)
    #im=userProps.getProperty(userName+".im")
    #authenticator.setUserAttributeValue(userName,"im",im)
    print("User "+userName+" created with password "+password+".")
#
# Create a WLS Group
def createGroup(authenticator, groupName, userProps):
  print ("Creating group " + groupName)
  if authenticator.groupExists(groupName):
    print ("Group "+groupName+" already exists.")
  else:
    print ("Group "+groupName+" does not exist.")
    description=userProps.getProperty(groupName+".description")
    authenticator.createGroup(groupName, description)
    # apparently you can"t set attributes on groups...
    print("Group "+groupName+" created.")
#
# Add a Member to a group
def addMember2Group(authenticator, groupName, memberName):
  print ("Adding member "+memberName+" to group " + groupName)
  if authenticator.isMember(groupName,memberName,true) == 0:
    print ("Member "+memberName+" not yet member of the group "+groupName+".")
    authenticator.addMemberToGroup(groupName, memberName)
    print ("Member "+memberName+" added to the group "+groupName+".")
  else:
    print ("Member "+memberName+" already member of the group "+groupName+".")
#
# Grant an appStripe"s appRole to a WLS Group
def grantAppRoleToWlsGroup(appStripe, appRole, wlsGroup):
    #
    # Grant an AppRole
    # http://docs.oracle.com/cd/E23943_01/web.1111/e13813/custom_infra_security.htm#WLSTC1398
    # grantAppRole(appStripe, appRoleName,principalClass, principalName)
    # appStripe: Specifies an application stripe.
    # appRoleName: Specifies a role name.
    # principalClass: Specifies the fully qualified name of a class.
    # principalName: Specifies the principal name.
    #grantAppRole("Service_Bus_Console","Monitor","oracle.security.jps.service.policystore.ApplicationRole","SBMonitor")
    #grantAppRole("Service_Bus_Console","Tester","weblogic.security.principal.WLSUserImpl","weblogic")
    try:
      print("Grant App Role: "+appRole+" in stripe "+appStripe+" to WebLogic Group: "+wlsGroup)
      grantAppRole(appStripe,appRole,"weblogic.security.principal.WLSGroupImpl",wlsGroup)
      print("Grant Succeeded")
    except javax.management.MBeanException, mbe:
      mbeStr = str(mbe)
      if "is already a member of application role" in mbeStr:
        print("AppRole "+appStripe+"."+appRole+" apparently already granted to group: "+wlsGroup) 
      else:
        print ("MBean Exception granting role "+ appStripe+"."+appRole+" to group "+wlsGroup+": ", sys.exc_info()[1])
    except:
      print("Failed to grant role "+ appStripe+"."+appRole+" to group "+wlsGroup+".", sys.exc_info()[0], sys.exc_info()[1] )
      #
#
# Grant an appStripe"s appRole to a WLS User
def grantAppRoleToWlsUser(appStripe, appRole, wlsUser):
    #
    # Grant AppRole
    # http://docs.oracle.com/cd/E23943_01/web.1111/e13813/custom_infra_security.htm#WLSTC1398
    # grantAppRole(appStripe, appRoleName,principalClass, principalName)
    # appStripe: Specifies an application stripe.
    # appRoleName: Specifies a role name.
    # principalClass: Specifies the fully qualified name of a class.
    # principalName: Specifies the principal name.
    #grantAppRole("Service_Bus_Console","Monitor","oracle.security.jps.service.policystore.ApplicationRole","SBMonitor")
    #grantAppRole("Service_Bus_Console","Tester","weblogic.security.principal.WLSUserImpl","weblogic")
    try:
      print("Grant App Role: "+appRole+" in stripe "+appStripe+" to WebLogic User: "+wlsUser)
      grantAppRole(appStripe,appRole,"weblogic.security.principal.WLSUserImpl",wlsUser)
      print("Grant Succeeded")
    except javax.management.MBeanException, mbe:
      mbeStr = str(mbe)
      if "is already a member of application role" in mbeStr:
        print("AppRole "+appStripe+"."+appRole+" apparently already granted to group: "+wlsUser) 
      else:
        print ("MBean Exception granting role "+ appStripe+"."+appRole+" to user "+wlsUser+": ", sys.exc_info()[1])
    except:
      print("Failed to grant role "+ appStripe+"."+appRole+" to user "+wlsUser+".", sys.exc_info()[0], sys.exc_info()[1] )
      
 #
 #
def main():
  try:
    print (lineSeperator)
    print ("Create DEMO Users and Groups")
    print (lineSeperator)
    print("\nConnect to AdminServer ")
    connectToadminServer(adminUrl, adminServerName)
    #
    # Get Realm and Authenticator
    realm = getRealm()
    authenticator = getAuthenticator(realm)
    # read User Properties
    userProps = loadPropsFile(userPropsFile)
    # Users
    print("\nCreate Weblogic Users "+wlsUsers)
    idx=0
    wlsUserList=wlsUsers.split(",")
    for wlsUser in wlsUserList:
      print(str(idx)+": Add "+wlsUser)
      createUser(authenticator, wlsUser, userProps)
      idx=idx+1
    #
    # Groups
    print("\nCreate Weblogic Groups "+wlsGroups)
    idx=0
    wlsGroupList=wlsGroups.split(",")
    for wlsGroup in wlsGroupList:
      print(str(idx)+": Add "+wlsGroup)
      createGroup(authenticator, wlsGroup, userProps)   
      grpMembers=userProps.getProperty(wlsGroup+".members")      
      if grpMembers != None:
        grpMemberList=grpMembers.split(",")
        for grpMember in grpMemberList:
          addMember2Group(authenticator, wlsGroup, grpMember)
      grpMemberGroups=userProps.getProperty(wlsGroup+".memberGroups")      
      if grpMemberGroups != None:
        grpMemberGroupList=grpMemberGroups.split(",")
        for grpMemberGroup in grpMemberGroupList:
          addMember2Group(authenticator, wlsGroup, grpMemberGroup)
      idx=idx+1
    #
    # Approle"s
    print("\Grant Application Roles "+appRoleGrants)
    idx=0
    appRoleGrantList=appRoleGrants.split(",")
    for appRoleGrant in appRoleGrantList:
      appStripe=userProps.getProperty(appRoleGrant+".appStripe")
      appRoleName=userProps.getProperty(appRoleGrant+".appRoleName")
      appRoleGrantMembers=userProps.getProperty(appRoleGrant+".members")      
      if appRoleGrantMembers != None:
        appRoleGrantMemberList=appRoleGrantMembers.split(",")
        for appRoleGrantMember in appRoleGrantMemberList:
          grantAppRoleToWlsUser(appStripe, appRoleName, appRoleGrantMember)
      appRoleGrantMemberGroups=userProps.getProperty(appRoleGrant+".memberGroups")      
      if appRoleGrantMemberGroups != None:
        appRoleGrantMemberGroupList=appRoleGrantMemberGroups.split(",")
        for appRoleGrantMemberGroup in appRoleGrantMemberGroupList:
          grantAppRoleToWlsGroup(appStripe, appRoleName, appRoleGrantMemberGroup)
      idx=idx+1
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
exit()