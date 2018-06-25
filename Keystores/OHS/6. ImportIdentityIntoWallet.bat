@call keystore_env.bat
%ORACLE_HOME%\oracle_common\bin\orapki wallet jks_to_pkcs12 -wallet %ORACLE_HOME%\wallet -pwd %KEY_PASS% -keystore %IDENTITY_STORE% -jkspwd %IDENTITY_PASS%