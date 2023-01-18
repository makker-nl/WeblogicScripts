#!/bin/bash
echo set Fusion MiddleWare 12cR2 environment
export ORACLE_BASE=/app/oracle
export INVENTORY_DIRECTORY=/app/oraInventory
export FMW_HOME=$ORACLE_BASE/product/middleware/FMW12214
export FMW_COMMON_HOME=$FMW_HOME/oracle_common
export WL_HOME=$FMW_HOME/wlserver
export SOA_PROD_DIR=$FMW_HOME/soa
export ESS_PROD_DIR=$FMW_HOME/ess
export BPM_PROD_DIR=$FMW_HOME/bpm
export OSB_PROD_DIR=$FMW_HOME/osb
export OHS_PROD_DIR=$FMW_HOME/ohs
export MFT_PROD_DIR=$FMW_HOME/mft
export EM_DIR=$FMW_HOME/em
export JAVA_HOME=$ORACLE_BASE/product/jdk8
export SHARED_CONFIG_DIR=$ORACLE_BASE
export APPLICATION_HOME=$SHARED_CONFIG_DIR/applications/$DOMAIN_NAME
export OHS_ORACLE_HOME=$ORACLE_HOME
export MFT_DOMAIN_NAME=mft_domain
export MFT_DOMAIN_HOME=$SHARED_CONFIG_DIR/domains/$MFT_DOMAIN_NAME
#
. $WL_HOME/server/bin/setWLSEnv.sh
export PATH=$FMW_HOME/oracle_common/common/bin:$PATH
