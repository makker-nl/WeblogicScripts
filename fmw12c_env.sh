#!/bin/bash
echo set Jdeveloper SOA Quickstart 12cR2 environment
export ORACLE_BASE=/app/oracle
export JAVA_HOME=$ORACLE_BASE/product/jdk8
export FMW_HOME=$ORACLE_BASE/product/jdeveloper/12214_SOAQS
export PATH=$FMW_HOME/oracle_common/common/bin:$PATH
. setWlstEnv.sh
export GMDS=~/.jdeveloper/system12.2.1.4.42.190911.2248/DefaultDomain/store/gmds
