#!/bin/bash
#############################################################################
# List applicable FMW DomainConfig using wlst
#
# @author Martien van den Akker, Darwin-IT Professionals
# @version 1.0, 2022-12-12
#
#############################################################################
#
. fmw12c_env.sh
export ENV=$1
echo
echo "List FMW DomainConfig"
wlst.sh ./listDomainConfig.py -loadProperties ${ENV}.properties
