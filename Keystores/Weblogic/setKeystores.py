#############################################################################
# Deploy SamlMetaData to WLS 12c
#
# @author Martien van den Akker, Darwin-IT Professionals
# @version 1.0, 2018-02-08
#
#############################################################################
# Modify these values as necessary
import os,sys, traceback
scriptName = sys.argv[0]
#
workingDir=os.getcwd()
identityStore=os.environ["IDENTITY_STORE"]
identityStorePwd=os.environ["IDENTITY_PASS"]
identityAlias=os.environ["IDENTITY_ALIAS"]
keyPwd=os.environ["KEY_PASS"]
trustStore=os.environ["TRUST_STORE"]
trustStorePwd=os.environ["TRUST_PASS"]
#
#
def main():
  # Connect to administration server
  try:
    connect(adminUser, adminPwd, adminUrl)
    # Set Identity Store
    edit()
    startEdit()
    cd('/Servers/'+targetServerName)
    cmo.setCustomIdentityKeyStoreFileName(workingDir+"\\"+identityStore)
    set('CustomIdentityKeyStorePassPhrase', identityStorePwd)
    cmo.setCustomTrustKeyStoreFileName(workingDir+"\\"+trustStore)
    set('CustomTrustKeyStorePassPhrase', trustStorePwd)
    cmo.setKeyStores('CustomIdentityAndCustomTrust')
    cmo.setCustomIdentityKeyStoreType('JKS')
    cmo.setCustomTrustKeyStoreType('JKS')
    cd('/Servers/'+targetServerName+'/SSL/'+targetServerName)
    cmo.setServerPrivateKeyAlias(identityAlias)
    set('ServerPrivateKeyPassPhrase', keyPwd)
    cmo.setEnabled(true)
    cmo.setListenPort(int(sslListenPort))
    save()
    activate()
    #    
    print("\nExiting...")
    exit()
  except NameError, e:
    print("Apparently properties not set.")
    print "Please check the property: ", sys.exc_info()[0], sys.exc_info()[1]
    usage()
  except:
    apply(traceback.print_exception, sys.exc_info())
    stopEdit('y')
    exit(exitcode=1)
#call main()
main()