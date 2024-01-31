SET SCRIPT_PATH=%~dp0
FOR /F "tokens=* USEBACKQ" %%g IN (`where pythonw`) do (SET "PYTHONW_PATH=%%g")
schtasks /Create /TN wow-wtf-backup /TR "%PYTHONW_PATH% %SCRIPT_PATH%wow-wtf-backup.py" /SC ONLOGON /F
schtasks /Run /TN wow-wtf-backup
pause