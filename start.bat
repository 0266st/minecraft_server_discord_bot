@echo on
cd C:\minecraft_servers\playit
start C:\minecraft_servers\playit\playit.exe
cd C:\minecraft_servers\server_scripts
title minecraft_server
java -Xmx12G -Xms12G -jar %%1 -nogui
call ./backup.bat
exit