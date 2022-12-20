#!/bin/bash
#############################################################################
# List Domain System Components using wlst
#
# @author Martien van den Akker, Darwin-IT Professionals
# @version 1.0, 2017-04-19
#
#############################################################################
#
. fmw12c_env.sh
export ENV=$1
echo
echo "List Domain System Components"
wlst.sh ./listSystemComponents.py -loadProperties ${ENV}.properties
