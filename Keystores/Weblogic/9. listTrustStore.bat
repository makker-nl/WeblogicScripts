@call keystore_env.bat
keytool -list -keystore %TRUST_STORE% -storepass %TRUST_PASS% -v