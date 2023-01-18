#!/bin/bash
#############################################################################
# Test Datsources using wlst
#
# @author Martien van den Akker, Darwin-IT Professionals
# @version 1.0, 2023-01-18
#
#############################################################################
#
. fmw12c_env.sh
export ENV=$1
echo
echo "Test DataSources"
wlst.sh ./testDS.py -loadProperties ${ENV}.properties
