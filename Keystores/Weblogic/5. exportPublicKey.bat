@call keystore_env.bat
keytool -export -keystore %IDENTITY_STORE% -storepass %IDENTITY_PASS% -alias %IDENTITY_ALIAS%  -file %IDENTITY_ALIAS%.cer