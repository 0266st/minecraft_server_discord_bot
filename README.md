# MinecraftとDiscordのBOTを連携させた
このコードを使いたい場合、以下のようにセットアップしてください。


## v1.2.0修正点
修正点は以下の3つです。
 - シャットダウンコマンドなどを実行する際、UWSCではなくRCONを使用してできるようにした
 - 新たに/serverコマンドにmessageを追加し、第二引数にrun_argを作り、messageが来たらRCON経由でsayコマンドを実行するようにした。