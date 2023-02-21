#!/bin/bash
SCRIPTPATH=$(dirname $0)
#
export ENV=$1
#
# Set FMW12c Environment
export ORACLE_BASE=/app/oracle
export JAVA_HOME=$ORACLE_BASE/product/jdk8
export MW_HOME=$ORACLE_BASE/product/jdeveloper/12214_BPMQS
. $MW_HOME/wlserver/server/bin/setWLSEnv.sh
export PATH=$PATH:$MW_HOME/oracle_common/common/bin
#
echo
echo "Create Users and Groups"
wlst.sh $SCRIPTPATH/createDemoUsers.py -loadProperties ${ENV}.properties
