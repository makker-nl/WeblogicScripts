#!/bin/bash
echo set Fusion MiddleWare 12cR2 environment
#export FMW_VER=12.2.1.3
#export DOMAIN_NAME=fmw12c_domain
export OHS_DOMAIN_NAME=ohs_domain
export INSTANCE_NAME=ohs1
export ORACLE_BASE=/app/oracle
export INVENTORY_DIRECTORY=/app/oraInventory
export FMW_HOME=$ORACLE_BASE/product/middleware
export FMW_COMMON_HOME=$FMW_HOME/oracle_common
export WL_HOME=$FMW_HOME/wlserver
export SOA_PROD_DIR=$FMW_HOME/soa
export ESS_PROD_DIR=$FMW_HOME/ess
export BPM_PROD_DIR=$FMW_HOME/bpm
export OSB_PROD_DIR=$FMW_HOME/osb
export OHS_PROD_DIR=$FMW_HOME/ohs
export EM_DIR=$FMW_HOME/em
export JAVA_HOME=$ORACLE_BASE/product/jdk
export APPLICATION_HOME=$SHARED_CONFIG_DIR/applications/$DOMAIN_NAME
export OHS_ORACLE_HOME=$ORACLE_HOME
export OHS_DOMAIN_HOME=$SHARED_CONFIG_DIR/domains/$OHS_DOMAIN_NAME
export OHS_CONFIG_DIR=$SHARED_CONFIG_DIR/domains/$OHS_DOMAIN_NAME/config/fmwcomfig/components/OHS/$INSTANCE_NAME
#
. $WL_HOME/server/bin/setWLSEnv.sh
export PATH=$FMW_HOME/oracle_common/common/bin:$PATH
