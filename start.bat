@echo on
cd server_scripts
title minecraft_server
java -Xmx12G -Xms12G -jar server.jar -nogui
call ./backup.bat
exit