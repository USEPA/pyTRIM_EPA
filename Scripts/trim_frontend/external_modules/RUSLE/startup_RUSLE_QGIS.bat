@echo off

:: If you get an error, check that the folder below exists.
set QGIS_ROOT=C:\Program Files\QGIS 3.30.0

:: The following script will set all the required environment variables.
call "%QGIS_ROOT%\bin\o4w_env.bat" 

set PATH=%QGIS_ROOT%\bin;%QGIS_ROOT%\apps\qgis\bin;C:\OSGeo4W64\apps\Qt5\bin;%PATH%
set PYTHONPATH=%QGIS_ROOT%\apps\qgis\python;%QGIS_ROOT%\apps\qgis\python\plugins;%PYTHONPATH%
set QGIS_PREFIX_PATH=%QGIS_ROOT%\apps\qgis
set QT_QPA_PLATFORM_PLUGIN_PATH=%QGIS_ROOT%\apps\Qt5\plugins

:: Add processing plugin
set PATH=%QGIS_ROOT%\apps\qgis\python\plugins\processing;%PATH%

:: Pull in venv modules
set PATH=C:\Users\55586\.virtualenvs\trim-builder-uxTFC5Sw\Lib\site-packages;%PATH%

:: Finally run the script
python %~dp0RUSLE_Script_Final.py %QGIS_ROOT%