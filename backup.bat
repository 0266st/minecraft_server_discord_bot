@echo off
set "hour=%TIME:~0,2%"
if "%hour:~0,1%"==" " set "hour=0%hour:~1,1%"
set backup_dir=C:\minecraft_server\backups\%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%_%hour%%TIME:~3,2%%TIME:~6,2%
md %backup_dir%
md %backup_dir%\world
md %backup_dir%\world_nether
md %backup_dir%\world_the_end
echo a | xcopy /s /e /y C:\minecraft_server\world %backup_dir%\world
echo a | xcopy /s /e /y C:\minecraft_server\world_nether %backup_dir%\world_nether
echo a | xcopy /s /e /y C:\minecraft_server\world_the_end %backup_dir%\world_the_end

echo Backups created successfully in %backup_dir%

setlocal
set "folder=C:\minecraft_server\backups"
set "limit=15"

for /f "skip=%limit% delims=" %%i in ('dir /ad /b /o-d "%folder%\*.*"') do (
    echo Deleting "%%i"...
    rd /s /q "%folder%\%%i"
)

endlocal