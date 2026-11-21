@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "LOG=%~dp0publish-log.txt"
echo ==== %DATE% %TIME% ==== > "%LOG%"
echo STEP1 START >> "%LOG%"
set "HTTP_PROXY="
set "HTTPS_PROXY="
set "http_proxy="
set "https_proxy="
set "ALL_PROXY="
set "all_proxy="
echo STEP2 PROXY_CLEARED >> "%LOG%"
where gh >nul 2>>"%LOG%"
if errorlevel 1 goto no_gh
echo STEP3 GH_FOUND >> "%LOG%"
set "TOKEN="
set /p "TOKEN=Paste GitHub token: "
if not defined TOKEN goto no_token
echo STEP4 TOKEN_RECEIVED >> "%LOG%"
<nul set /p "=%TOKEN%" > "%TEMP%\fai_gh_token.txt"
gh auth login --hostname github.com --with-token < "%TEMP%\fai_gh_token.txt" >> "%LOG%" 2>&1
if errorlevel 1 goto auth_failed
del "%TEMP%\fai_gh_token.txt" >nul 2>&1
echo STEP5 AUTH_OK >> "%LOG%"
gh repo create free-ai-credits --public --source . --remote origin --push >> "%LOG%" 2>&1
if errorlevel 1 goto push_failed
echo STEP6 SUCCESS >> "%LOG%"
echo SUCCESS! Check publish-log.txt
pause
exit /b 0
:no_gh
echo ERR GH_NOT_FOUND >> "%LOG%"
echo ERROR: gh not found. Press any key to exit.
pause
exit /b 1
:no_token
echo ERR NO_TOKEN >> "%LOG%"
echo ERROR: no token entered. Press any key to exit.
pause
exit /b 1
:auth_failed
echo ERR AUTH_FAILED >> "%LOG%"
echo ERROR: token rejected. See publish-log.txt
pause
exit /b 1
:push_failed
echo ERR PUSH_FAILED >> "%LOG%"
echo Trying direct git push... >> "%LOG%"
git push -u origin main >> "%LOG%" 2>&1
if errorlevel 1 goto final_failed
echo STEP7 SUCCESS_VIA_GIT >> "%LOG%"
echo SUCCESS! Check publish-log.txt
pause
exit /b 0
:final_failed
echo ERR FINAL_FAILED >> "%LOG%"
echo FAILED. See publish-log.txt
pause
exit /b 1
