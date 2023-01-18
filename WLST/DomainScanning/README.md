# Domain Creation
The [DomainCreation](DomainCreation) folder contains several example scripts to create a domain.getAppDeploymentTargetProps.py
To use these scripts I would recommend you to download this folder and copy it to your target system. Instead of forking/checking this out.

## FMW12c Environment
The script [fmw12c_env.sh](fmw12c_env.sh) sets the FusionMiddleware/WebLogic settings. It runs the _setWLSEnv.sh_ script, to set the WebLogic Environment properly. 
Also it adds the _$FMW_HOME/oracle_common/common/bin_ folder to the path. This folder contains the _wlst.sh_ script. 

Modify this script to set the _$ORACLE_BASE_ and the depending _$FMW_HOME_ folder to reflect the install folder of your FusionMiddleware/WebLogic installation. 

Create an _environment.properties_ file, with the following content:

````
environment=dev
adminUrl=oracle-vde.oracle.local:7001
adminUser=weblogic
adminPwd=welcome1
adminServerName=AdminServer
domainHome=/app/oracle/domains/mft_domain
````

Name it for instance _[dev.properties](dev.properties)_, _uat.properties_, etc.

See the article [Start and stop a WebLogic (soa/osb) domain](http://blog.darwin-it.nl/2016/07/start-and-stop-weblogic-soaosb-domain.html) to create User Config and Key files.
These contain encrypt admin credentials, to prevent the need to have the username/password in plain text.

I could invest to implement this in these scripts.

## Scripts
To use the scripts below, first set the FMW12c Environment as follows

    $ . fmw12c_env.sh
    
The dot is short for _source_, so you could also do:

    $ source fmw12c_env.sh

This makes sure that the settings in the session running the script are exported to the current session. 

Each of the scripts below are created as a pair. A bash script accompanying the WLST script. 
Having an environment property file like _[dev.properties](dev.properties)_, you can run the following scripts like:

    $ listDataSources.sh dev

The parameter _dev_ here refers to the environment you want to run the script for. This is used to load the properties file and call _wlst.sh_ for the WLST script: 

    $ wlst.sh ./listDataSources.py -loadProperties ${ENV}.properties

### List Application Deployments
The combination [listAppDeployments.py](listAppDeployments.py)/[sh](getAppDeploymentTargetProps.sh) lists the AppDeployments of the DomainConfig. 
The script creates a CSV file, called: *listAppDeployments_$environment.csv*, where *$environment* refers to the environment property in the _environment.properties_ file.

### List/test DataSources
The combination [listDataSources.py](listDataSources.py)/[sh](listDataSources.sh) lists the Datasources of DomainConfig and the Server Runtimes. 
It lists about all the properties known to WebLogic (a few properties are left out, because of less important and the need to transform/interpret the content).

The script delivers two CSV files:

* *listDataSourceRuntimes_$environment.csv*
* *listDataSourceConfigs_$environment.csv*

The scripts [listDS.py](listDS.py)/[sh](listDS.sh) are a simple, earlier version, that outputs the main config properties in tabular format. 

With [testDS.py](testDS.py)/[sh](testDS.sh) you can test the DataSources in your domain. 


### List Domain Config
The script [listDomainConfig.py](listDomainConfig.py)/[sh](listDomainConfig.sh) are to scan the Domain primarly for High Availability properties. Think of the cluster _Migration Basis_, datasources being GridLink, etc.
The script outputs all the data in CSV snippets that can be copied to Excel.

### List Migratable Targets
WebLogic uses two migratable target concepts, one for JMS Servers and persistence stores, and one for JTA.

The script combination [listMigratableTargets.py](listMigratableTargets.py)/[sh](listMigratableTargets.sh) list both types of migratable targets. 
The following files are the result of the script:

* *listMigratableTargets_$environment.csv*
* *listJTAMigratableTargets_$environment.csv*

The most important column is the _MigrationPolicy_. Default the value is _manual_, but for Automatic Service Migration you would set it on "Failure Migration" in the console. 

### List Server Groups
The script [listServerGroups.py](listServerGroups.py)/[sh](listServerGroups.sh) shows the server group assignments in your domain. Read more on server groups in the article [Set your Oracle FusionMiddleware 12c ServerGroups properly](https://medium.com/nerd-for-tech/set-your-oracle-fusionmiddleware-12c-servergroups-properly-318772e930cb).

### List System Components
The script [listSystemComponents.py](listSystemComponents.py)/[sh](listSystemComponents.sh), list the System Components of a Fusion Middleware domain. Think of embedded Oracle HTTP instances, or BI Publisher system components.











