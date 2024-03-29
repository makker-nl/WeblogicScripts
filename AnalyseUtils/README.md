# Analysis Utilities.

This sub-project contains several scripts, divided in sub-folders to analyse a Weblogic or FMW Infrastructure. It contains the following scripts:

* [ScanADFBC](ScanADFBC/README.md): Scan for all ADF business component Files in an ADF application and list applicable properties into a CSV file. 
* [ScanJCAFiles](ScanJCAFiles/README.md): Scan for all JCA Files in all SOA Composite projects and list applicable properties into a CSV file. 
* [ScanScriptsForDBObjects](ScanScriptsForDBObjects/README.md): Scan for all SQL (.sql) and Pytthon (.py) Files in a Subversion workingcopy or Git clone folder and list found occurrences of the tables and views into a CSV file. 
* [TransformMDS2JWS](TransformMDS2JWS/README.md): Convert the contents of an export of a SOA Infrastructure MDS into SOA Quickstart (JDeveloper) 12c SOA Application workspaces.
* ScanMDSReferences: Scan for XSDs in the MDS with occurrences of references to them in SOA Projects.
* ScanCDMXsdRefs: Scan for different artefacts in SOA Projects with references to XSDs in the MDS.
