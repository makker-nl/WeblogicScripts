@call keystore_env.bat
echo import %ROOT_CERT_1% with alias %ROOT_CERT_ALIAS_1%
"%JAVA_HOME%"\bin\keytool -importcert -file %ROOT_CERT_HOME%\%ROOT_CERT_1% -keystore %IDENTITY_STORE%  -alias %ROOT_CERT_ALIAS_1% -storepass %IDENTITY_PASS% 
echo import %ROOT_CERT_2% with alias %ROOT_CERT_ALIAS_2%
"%JAVA_HOME%"\bin\keytool -importcert -file %ROOT_CERT_HOME%\%ROOT_CERT_2% -keystore %IDENTITY_STORE%  -alias %ROOT_CERT_ALIAS_2% -storepass %IDENTITY_PASS% 
echo import %ROOT_CERT_3% with alias %ROOT_CERT_ALIAS_3%
"%JAVA_HOME%"\bin\keytool -importcert -file %ROOT_CERT_HOME%\%ROOT_CERT_3% -keystore %IDENTITY_STORE%  -alias %ROOT_CERT_ALIAS_3% -storepass %IDENTITY_PASS% 