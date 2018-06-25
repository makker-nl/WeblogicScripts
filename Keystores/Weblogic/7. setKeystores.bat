@call keystore_env.bat
@setlocal
@set ORACLE_HOME=C:\oracle\product\wls12213
@call %ORACLE_HOME%\wlserver\server\bin\setWLSEnv.cmd
@set PATH=%ORACLE_HOME%\oracle_common\common\bin;%PATH%
@wlst.cmd setKeystores.py -loadProperties Weblogic.properties
@endlocal