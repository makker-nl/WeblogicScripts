#!/bin/bash
#############################################################################
# List Migratable targets using wlst
#
# @author Martien van den Akker, Darwin-IT Professionals
# @version 1.0, 2022-12-16
#
#############################################################################
#
. fmw12c_env.sh
export ENV=$1
echo
echo "List Weblogic Migratable Targets"
wlst.sh ./listMigratableTargets.py -loadProperties ${ENV}.properties
