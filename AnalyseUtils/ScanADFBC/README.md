# Scan JCA Files

## Introduction
This project contains an ANT script that scans an Oracle ADF application for ADF business component files (Entity/View Objects).
It expects a JDeveloper Release 2, version 12.2.1.x. Latest version of 12.2.1.4 is assumed, but it should work with earlier 12.2.1 versions as well.

The script creates an CSV file that lists all the view and entity object files found in the folder structure. For each ADF BC file it lists the following:
* Application: The JWS the SOA Project apparently belongs to. It is expected to be in the parent folder of the SOA Project. 
* Project name: Name of the SOA Project
* ADF BC Type: Entity Object, or View Object
* ADF BC Folder: Folder in which the Business component is stored
* ADF BC Component: Business component file name
* ADF BC Name: Name of the Business component as registered in the *Name* attribute in the file
* Table List: For Entity Object, list of distinct table names found in the attribute list of the Entity Object.
* Column List: For Entity Object, list column names prefixed with the particular tablename (in case it is based on mulitple tables)
* CustomQuery: For View Object, if the component is based on a custom query, this provides the particular query.
* FromList: For View Object, if the component is based on a declared query the list of tables in the declared from clause.
* EntityUsage Name: For View Object, reference to the name entity object it is based upon.
* EntityUsage Entity: For View Object, reference to the entity object it is based upon.
* ViewAttributeList: : For View Object, list of View Attributes.


## Build Properties
The project relies on the [build.properties](build.properties) file. 

In the properties file, the main properties to set are:

````
fmw.home=${env.FMW_HOME}
#
ant-contrib.jar=${fmw.home}/oracle_common/modules/thirdparty/ant-contrib-1.0b3.jar
#
adfRoot=d:/workspace/git/ssp
outputFile=adf-files.csv
adfTempDir=adfFiles
adfEntPropsXsl=xsl/entityObject.xsl
adfViewPropsXsl=xsl/viewObject.xsl

````

* *fmw.home*: The reference to the Oracle home where your JDeveloper instance resides. Determined from the $FMW_HOME variable.
* *ant-contrib.jar*: reference to the ANT contrib library, relative to the *fmw.home* property. 
* *adfRoot*: The Subversion/Git root folder where the ADF project files are placed.
* *outputFile*: The CSV File that is created. 

## Run
First set your FMW Environment with a script like [../../scripts/fmw12c_env.sh](../../scripts/fmw12c_env.sh) or a Windows variant.

Then run the script as:

    $ ant -f scanADFBC.xml
    
 