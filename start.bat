@echo on
cd server_scripts
title minecraft_server
java -Xmx12G -Xms12G -jar C:\Minecraft_servers\server_scripts\server.jar -nogui
call ./backup.bat
exit