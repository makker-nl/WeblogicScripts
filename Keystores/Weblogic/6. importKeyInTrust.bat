@call keystore_env.bat
keytool -import -file %IDENTITY_ALIAS%.cer -alias  %IDENTITY_ALIAS% -keystore %TRUST_STORE% -storepass %TRUST_PASS%