@echo on
cd C:\minecraft_server
cd playit
start ./playit.exe
cd ..
title Minecraft_Java_server
:restart
java -Xms12G -Xmx12G -jar server.jar nogui
set /p isshutdown=<.\script\isshutdown.txt
call .\script\backup.bat
if %isshutdown%==0 (goto restart)
echo 0 > .\script\isshutdown.txt
exit