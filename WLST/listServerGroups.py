#############################################################################
# List ServerGroups for a domain
#
# @author Martien van den Akker, Darwin-IT Professionals
# @version 1.0, 2018-11-05
#
# Usage:
#   wlst listServerGroups.py
#
# When       Who                      What
# 20181105   Martien van den Akker    Create
#
#############################################################################
#
import sys, traceback
scriptName = sys.argv[0]
#
#domainHome='/data/oracle/config/domains/soa_domain'
#
#
def main():
  readDomain(domainHome)
  cd('/')
  print ('Available Server Groups:')
  listServerGroups()
  print ('Assigned Server Groups:')
  allServers=cmo.getServers()
  if (len(allServers) > 0):
    for wlserver in allServers:
      wlserverName = wlserver.getName()
      print('Groups of server: '+wlserverName)
      serverGroups=getServerGroups(wlserverName)
      for serverGroup in serverGroups:
        print('..'+serverGroup)
#
# Main
main() 
