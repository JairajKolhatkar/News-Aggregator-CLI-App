@echo off
echo Creating desktop shortcut for Indian News Aggregator...

set SCRIPT="%TEMP%\create_shortcut.vbs"
set CURRENTDIR=%~dp0

echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\Indian News Aggregator.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%CURRENTDIR%start_news.bat" >> %SCRIPT%
echo oLink.WorkingDirectory = "%CURRENTDIR%" >> %SCRIPT%
echo oLink.Description = "Indian News Aggregator" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%

echo Desktop shortcut created successfully!
echo.
echo You can now start the application by double-clicking the "Indian News Aggregator" icon on your desktop.
pause 