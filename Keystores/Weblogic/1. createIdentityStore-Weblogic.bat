@call keystore_env.bat
"%JAVA_HOME%"\bin\keytool -genkeypair -keyalg RSA -alias %IDENTITY_ALIAS%  -keypass %KEY_PASS% -keystore %IDENTITY_STORE% -storepass %IDENTITY_PASS% -dname %DNAME% -validity %VALIDITY% -keysize %KEYSIZE% -ext SAN=%SAN%