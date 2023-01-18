#!/bin/bash
#############################################################################
# List Application Deployments on a domain using wlst
#
# @author Martien van den Akker, Oracle Nederland B.V.
# @version 1.0, 2023-01-06
#
#############################################################################
#
. fmw12c_env.sh
export ENV=$1
echo
echo "List Application Deployments"
wlst.sh ./listAppDeployments.py -loadProperties ${ENV}.properties
