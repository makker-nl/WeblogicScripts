#############################################################################
# Create a diagnostic Module for WLS 12c Tuning & Troubleshooting workshop
# Lab 06
#
# @author Martien van den Akker, Darwin-IT Professionals
# @version 1.0, 2019-10-08
#
#############################################################################
# Modify these values as necessary
import os,sys, traceback
#
adminHost=os.environ["ADM_HOST"]
adminPort=os.environ["ADM_PORT"]
admServerUrl = 't3://'+adminHost+':'+adminPort
#
adminUser='weblogic'
adminPwd='welcome1'
ttServerName=os.environ["TTSVR_NAME"]
diagModuleName='TTDiagnostics'
#
def getMServer(serverName):
  server=getMBean('/Servers/'+serverName)
  return server
#
def createDiagnosticModule(diagModuleName, targetServerName):
  module=getMBean('/WLDFSystemResources/'+diagModuleName)
  if module==None:
    print 'Create new Diagnostic Module'+diagModuleName
    edit()
    startEdit()
    cd('/')
    module = cmo.createWLDFSystemResource(diagModuleName)
    targetServer=getMServer(targetServerName)
    module.addTarget(targetServer)
    # Activate changes
    save()
    activate(block='true')
    print 'Diagnostic Module created successfully.'
  else:
    print 'Diagnostic Module'+diagModuleName+' already exists!'
  return module
#
def createCollector(diagModuleName, metricType, namespace, harvestedInstances,attributesCsv):
  harvesterName='/WLDFSystemResources/'+diagModuleName+'/WLDFResource/'+diagModuleName+'/Harvester/'+diagModuleName 
  harvestedTypesPath=harvesterName+'/HarvestedTypes/';
  print 'Check Collector '+harvestedTypesPath+metricType
  collector=getMBean(harvestedTypesPath+metricType)
  if collector==None:
    print 'Create new Collector for '+metricType+' in '+diagModuleName
    edit()
    startEdit()
    cd(harvestedTypesPath)
    collector=cmo.createHarvestedType(metricType)
    cd(harvestedTypesPath+metricType)
    attributeArray=jarray.array([String(x.strip()) for x in attributesCsv.split(',')], String)
    collector.setHarvestedAttributes(attributeArray)
    collector.setHarvestedInstances(harvestedInstances)
    collector.setNamespace(namespace)
    # Activate changes
    save()
    activate(block='true')
    print 'Collector created successfully.'
  else:
    print 'Collector '+metricType+' in '+diagModuleName+' already exists!'
  return collector
#
def createJmsNotificationAction(diagModuleName, actionName, destination, connectionFactory):
  policiesActionsPath='/WLDFSystemResources/'+diagModuleName+'/WLDFResource/'+diagModuleName+'/WatchNotification/'+diagModuleName
  jmsNotificationPath=policiesActionsPath+'/JMSNotifications/'
  print 'Check notification action '+jmsNotificationPath+actionName
  jmsNtfAction=getMBean(jmsNotificationPath+actionName)
  if jmsNtfAction==None:
    print 'Create new JMS NotificationAction '+actionName+' in '+diagModuleName
    edit()
    startEdit()
    cd(policiesActionsPath)
    jmsNtfAction=cmo.createJMSNotification(actionName)
    jmsNtfAction.setEnabled(true)
    jmsNtfAction.setTimeout(0)
    jmsNtfAction.setDestinationJNDIName(destination)
    jmsNtfAction.setConnectionFactoryJNDIName(connectionFactory)
    # Activate changes
    save()
    activate(block='true')
    print 'JMS NotificationAction created successfully.'
  else:
    print 'JMS NotificationAction '+actionName+' in '+diagModuleName+' already exists!'
  return jmsNtfAction
  

def createPolicy(diagModuleName, policyName, ruleType, ruleExpression, actions):  
  policiesActionsPath='/WLDFSystemResources/'+diagModuleName+'/WLDFResource/'+diagModuleName+'/WatchNotification/'+diagModuleName
  policiesPath=policiesActionsPath+'/Watches/'
  print 'Check Policy '+policiesPath +policyName
  policy=getMBean(policiesPath +policyName)
  if policy==None:
    print 'Create new Policy '+policyName+' in '+diagModuleName
    edit()
    startEdit()
    cd(policiesActionsPath)
    policy=cmo.createWatch(policyName)
    #cd('/WLDFSystemResources/TTDiagnostics/WLDFResource/TTDiagnostics/WatchNotification/TTDiagnostics/Watches/HiStuckThreads')
    policy.setEnabled(true)
    policy.setExpressionLanguage('EL')
    policy.setRuleType(ruleType)
    policy.setRuleExpression(ruleExpression)
    policy.setAlarmType('AutomaticReset')
    policy.setAlarmResetPeriod(300000)
    cd(policiesPath +policyName)
    set('Notifications', actions)
    schedule=getMBean(policiesPath +policyName+'/Schedule/'+policyName)
    #cd('/WLDFSystemResources/TTDiagnostics/WLDFResource/TTDiagnostics/WatchNotification/TTDiagnostics/Watches/HiStuckThreads/Schedule/HiStuckThreads')
    schedule.setMinute('*')
    schedule.setSecond('*')
    schedule.setSecond('*/15')
    # Activate changes
    save()
    activate(block='true')
    print 'Policy created successfully.'
  else:
    print 'Policy '+policyName+' in '+diagModuleName+' already exists!'
  return policy
#
def main():
  try:
    print 'Connect to '+admServerUrl
    connect(adminUser,adminPwd,admServerUrl)
    createDiagnosticModule(diagModuleName, ttServerName)
    createCollector(diagModuleName, 'weblogic.management.runtime.JDBCDataSourceRuntimeMBean','ServerRuntime', None, 'ActiveConnectionsCurrentCount,CurrCapacity,LeakedConnectionCount')
    harvestedInstancesList=[]
    harvestedInstancesList.append('com.bea:ApplicationRuntime=medrec,Name=TTServer_/medrec,ServerRuntime=TTServer,Type=WebAppComponentRuntime')
    harvestedInstances=jarray.array([String(x.strip()) for x in harvestedInstancesList], String)    
    createCollector(diagModuleName, 'weblogic.management.runtime.WebAppComponentRuntimeMBean','ServerRuntime', harvestedInstances,'OpenSessionsCurrentCount') 
    createJmsNotificationAction(diagModuleName, 'JMSAction', 'com.tt.jms.WLDFNotificationQueue', 'weblogic.jms.ConnectionFactory')
    actionsList=[]
    actionsList.append('com.bea:Name=JMSAction,Type=weblogic.diagnostics.descriptor.WLDFJMSNotificationBean,Parent=[TTDomain]/WLDFSystemResources[TTDiagnostics],Path=WLDFResource[TTDiagnostics]/WatchNotification[TTDiagnostics]/JMSNotifications[JMSAction]')
    actions=jarray.array([ObjectName(action.strip()) for action in actionsList], ObjectName)    
    createPolicy(diagModuleName,'HiStuckThreads', 'Harvester', 'wls:ServerHighStuckThreads(\"30 seconds\",\"10 minutes\",5)', actions)
    ruleExpression='wls:ServerGenericMetricRule(\"com.bea:Name=MedRecGlobalDataSourceXA,ServerRuntime=TTServer,Type=JDBCDataSourceRuntime\",\"WaitingForConnectionHighCount\",\">\",0,\"30 seconds\",\"10 minutes\")'
    createPolicy(diagModuleName,'OverloadedDS', 'Harvester', ruleExpression, actions)
    disconnect()
    print("\nExiting...")
    exit()
  except:
    apply(traceback.print_exception, sys.exc_info())
    exit(exitcode=1)
#
#call main()
main()