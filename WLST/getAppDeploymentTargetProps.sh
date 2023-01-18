#!/bin/bash
#############################################################################
# Get Application Deployment targetting properties using wlst
#
# @author Martien van den Akker, Oracle Nederland B.V.
# @version 1.0, 2023-01-09
#
#############################################################################
#
. fmw12c_env.sh
export ENV=$1
echo
echo "List Application Deployments"
wlst.sh ./getAppDeploymentTargetProps.py -loadProperties ${ENV}.properties
