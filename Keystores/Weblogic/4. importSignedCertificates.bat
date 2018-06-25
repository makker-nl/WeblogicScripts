@call keystore_env.bat
echo import %IDENTITY_CERT% with alias %IDENTITY_ALIAS%
"%JAVA_HOME%"\bin\keytool -importcert -file %CERT_HOME%\%IDENTITY_CERT% -keystore %IDENTITY_STORE%  -alias %IDENTITY_ALIAS% -storepass %IDENTITY_PASS% 