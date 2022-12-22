# Transform SOA MDS into SOA Quickstart (JDeveloper) 12c SOA Applications.

## Introduction
This project contains an ANT script that can transform an export of the MDS of a SOA Suite Infrastructure into a project folder structure that can be imported into Oracle SOA Quickstart (Jdeveloper) 12c.
It expects a SOA Quickstart 12c Release 2, version 12.2.1.x. Latest version of 12.2.1.4 is assumed, but it should work with earlier 12.2.1 versions as well.

## MDS export
Create an export from the SOA Infrastructure. Navigate to a SOA Infra node, Then in the SOA Infrastructure pull down menu, navigate to _Administration_ -> _MDS Configuration_.
Then Select the first radio button option _Export metadata documents to an archive on the machine where this web browser is running_ (the default) and click on Export.

This results, possibly after a few minutes, into a file called _soa-infra_metadata.zip_.

Move this file to an environment with a proper Fusion MiddleWare environment, like a SOA Quickstart. And unzip it in a project folder.


## Build Properties
The project relies on the [build.properties](build.properties) file. 

In the is file, the main properties to set are:

* _source.mds_: the folder to where _soa-infra_metadata.zip_ file is extracted.
* _target.folder_: the folder where the SOA Applications should land.

## Run
First set your FMW Environment with a script like [../../scripts/fmw12c_env.sh](../../scripts/fmw12c_env.sh) or a Windows variant.

Then run the script as:

    $ ant -f transformMDS2JWS.xml
    
 