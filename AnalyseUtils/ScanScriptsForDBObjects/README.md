# Scan JCA Files

## Introduction
This project contains an ANT script that scans a folder for a .sql and .py files for occurrences of views and tables.
It expects a JDeveloper Release 2, version 12.2.1.x. Latest version of 12.2.1.4 is assumed, but it should work with earlier 12.2.1 versions as well.

The script creates a CSV file that lists all the script files found in the folder structure. For script File it lists the following:
* ScriptDir: folder that the script (.sql/.py) is found.
* ScriptName: name of the script file.
* Tables: list of tables found in the file.
* Views: list of views found in the file.


## Build Properties
The project relies on the [build.properties](build.properties) file. 

In the properties file, the main properties to set are:

````
fmw.home=${env.FMW_HOME}fmw.home=${env.FMW_HOME}
#
ant-contrib.jar=${fmw.home}/oracle_common/modules/thirdparty/ant-contrib-1.0b3.jar
#
scriptsRoot=d:/workspace/git/my-scripts
outputFile=scripts.csv
views=view1,view2,view3
tables=table1,table2,table3

````

* *fmw.home*: The reference to the Oracle home where your JDeveloper instance resides. Determined from the $FMW_HOME variable.
* *ant-contrib.jar*: reference to the ANT contrib library, relative to the *fmw.home* property. 
* *scriptsRoot*: The Subversion/Git root folder where the script files are stored.
* *outputFile*: The CSV File that is created. 
* *views*: comma-separated list of the views to look for.
* *tables*: comma-separated list of the tables to look for.

## Run
First set your FMW Environment with a script like [../../scripts/fmw12c_env.sh](../../scripts/fmw12c_env.sh) or a Windows variant.

Then run the script as:

    $ ant -f scanScriptsForDBObjects.xml
    
 