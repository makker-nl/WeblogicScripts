# Oracle Demo Community
This script is an example to import users and groups into Weblogic using a dynamic WLST script. 

It consists of the following parts:
* **usersAndGroups.properties**: Property file with all the users, groups and group-memberships.
* **createDemoUsers.py**: Actual WLST script that loops through the uses and groups, mentioned in the environment property file, reads the information from the _usersAndGroups.properties_ and creates the appropriate users and groups.
* **createDemoUsers.sh**: Shell script to run the WLST script
* **demo.properties**:  example environment property file.

# Setup
## Adapt shell script for the Weblogic Installation
The [createDemoUsers.sh](createDemoUsers.sh) script starts with setting environment variables for the Oracle Fusion Middelware 12c home and _JAVA_HOME_ to use. Using those it invokes the _setWLSEnv.sh_ script to set the proper environment to call WLST.

To adapt it to your environment change the following variables:
* **ORACLE_BASE**: Base folder of the Oracle installations on the host.
* **JAVA_HOME**: JAVA Home folder.
* **MW_HOME**: Particular Weblogic or Fusion Middleware Home.

## Environment properties.
The file [demo.properties](demo.properties) stores the Weblogic Admin server connection and the WebLogic user to use to connect to the Admin Server.

Make a copy for your target environment, like test or uat, and adapt the following properties:
* **adminServerName**: For the embedded WebLogic in SOA/BPM Quickstart (JDeveloper) installations it is called DefaultServer. For other environments it is usually AdminServer.
* **adminUrl**: host:port combination to your Admin Server. 
* **adminUser**: WebLogic Admin user to connect to the AdminServer.
* **adminPwd**: Password of the WebLogic Admin user.

Besides those the environment properties set the following properties:
* **defaultPassword=welcome1
* **userPropsFile**: refers to the specific user and group properties: [usersAndGroups.properties](usersAndGroups.properties)
* **wlsUsers**: List of users to create from the [usersAndGroups.properties](usersAndGroups.properties) file.
* **wlsGroups**:List of users to create from the [usersAndGroups.properties](usersAndGroups.properties) file.
* **appRoleGrants**: List of applicition specific role grants.
These properties are more or less static over the particular environments. Probably the belong in the[usersAndGroups.properties](usersAndGroups.properties) file.

## usersAndGroups.properties
This property file holds the complete Oracle BPM Demo community. But, you could adapt it for your own test users.

# Run
After applying the setup changes mentioned above, run the script as follows:

````
$ createDemoUsers.sh demo
````

Where _demo_ refers to the environment to create the users for. The [createDemoUsers.sh](createDemoUsers.sh) script will provide expand the _ENV_ parameter to ${ENV}.properties. In this example _demo.properties_ will be read.

# Resource
The original Oracle BPM Demo user community is given in the xml file [default-demo-community.xml](default-demo-community.xml). This is translated into the [usersAndGroups.properties](usersAndGroups.properties) file.
