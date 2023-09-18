@echo off
chcp 65001 > nul
echo セットアップするユーザのユーザIDを入力してください:
set /p USERID=
echo メッセージを送信するチャンネルのIDを入力してください:
set /p CHANNEL_ID=
echo サーバーのjarファイルのパスを入力してください(例:C:\path\to\server.jar):
set /p JARFILE_PATH=
echo サーバーアドレスを入力してください:
set /p SERVER_ADDRESS=
echo サーバーのRCONポートを入力してください
set /p RCON_PORT=
echo サーバーのRCONパスワードを指定してください
set /p RCON_PASS=
echo DiscordのBotトークンを入力してください:
set /p DISCORD_BOT_TOKEN=

REM ダブルクォーテーションを削除
set "JARFILE_PATH=%JARFILE_PATH:"=%"

REM バックスラッシュ(\)をスラッシュ(/)に変換
set "converted_path=%JARFILE_PATH:\=/%"

echo ロード中です。しばらくお待ちください....
echo 注意! settings.jsonにはDiscordのBotトークンが含まれています。"絶対に"公開しないでください。

echo {"user_id":"%USERID%","server_jar_path":"%converted_path%", "channel_id":"%CHANNEL_ID%", "server_address":"%SERVER_ADDRESS%", "rcon_port":"%RCON_PORT%", "rcon_pass":"%RCON_PASS%", "TOKEN":"%DISCORD_BOT_TOKEN%"} > settings.json
echo セットアップが完了しました。何かキーを押して退出してください.
pause
