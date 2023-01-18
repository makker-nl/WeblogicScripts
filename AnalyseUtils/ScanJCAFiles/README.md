# Scan JCA Files

## Introduction
This project contains an ANT script that scans an Oracle SOA Quickstart (Jdeveloper) 12c application/project folder structure for JCA files.
It expects a SOA Quickstart 12c Release 2, version 12.2.1.x. Latest version of 12.2.1.4 is assumed, but it should work with earlier 12.2.1 versions as well.

The script creates an CSV file that lists all the JCA files found in the structure. For each JCA File it lists the following:
* Application: The JWS the SOA Project apparently belongs to. It is expected to be in the parent folder of the SOA Project. 
* Project name: Name of the SOA Project
* jcaFile: the actual JCA File
* Adapter-config Name: Name of the JCA Configuration
* Adapter Type: apps, aq, db, file, ftp, jms
* Endpoint Type: interaction or activation
* Connection Factory Location: JNDI location of the Resource Adapter's Outbound Connection Pool
* Endpoint PortType: WSDL Port Type
* Endpoint Operation: WSDL Operation
* Adapter type specific properties.


## Build Properties
The project relies on the [build.properties](build.properties) file. 

In the properties file, the main properties to set are:

````
svnRoot=c:/Data/svn/SOA/trunk/SOAProjects
outputFile=jca-files.csv
````

* *svnRoot*: The Subversion/Git root folder where the SOA project files are placed.
* *outputFile*: The CSV File that is created. 

## Run
First set your FMW Environment with a script like [../../scripts/fmw12c_env.sh](../../scripts/fmw12c_env.sh) or a Windows variant.

Then run the script as:

    $ ant -f transformMDS2JWS.xml
    
 