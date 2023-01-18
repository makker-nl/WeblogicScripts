#!/bin/bash
#############################################################################
# List DataSources using wlst
#
# @author Martien van den Akker, Darwin-IT Professionals
# @version 1.0, 2022-12-12
#
#############################################################################
#
. fmw12c_env.sh
export ENV=$1
echo
echo "List DataSources"
wlst.sh ./listDS.py -loadProperties ${ENV}.properties
