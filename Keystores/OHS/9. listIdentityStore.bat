@call keystore_env.bat
"%JAVA_HOME%"\bin\keytool -list -keystore %IDENTITY_STORE% -storepass %IDENTITY_PASS% -v