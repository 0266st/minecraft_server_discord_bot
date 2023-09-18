import discord
from discord import app_commands
import subprocess
import win32gui
import time
import os
import json
import time
import mcrcon
import asyncio
from dotenv import load_dotenv
load_dotenv()
Intents = discord.Intents.all()
Intents.members = True
client = discord.Client(intents=Intents)
cmdtree = app_commands.CommandTree(client)

def load_settings(filepath):
    try:
        with open(filepath) as f:
            settings = json.load(f)
    except FileNotFoundError:
        print(f"{filepath} is not found.")
        settings = {}
    return settings

def rcon_cmd(command):
    global rcserver
    with mcrcon.MCRcon(rcserver['address'], rcserver['server_pass'], int(rcserver['port'])) as mcr:
        log=mcr.command(command)
        return log



def init():
    global config
    config = load_settings('C:/minecraft_servers/script/settings.json') 


@client.event
async def on_ready():
    global rcserver    
    rcserver = {
        'address' : config['server_address'],
        'port' : config['rcon_port'],
        'server_pass': config['rcon_pass']
    }
    await init()
    print(str('config : '))
    print(config)
    await cmdtree.sync()


@cmdtree.command(name="server", description="サーバーの起動、再起動をコマンドで司ります。")
@discord.app_commands.choices(
    run_opt=[
        discord.app_commands.Choice(name="Open",value="open"),
        discord.app_commands.Choice(name="Reboot",value="reboot"),
        discord.app_commands.Choice(name="Shutdown", value="shutdown"),
        discord.app_commands.Choice(name="Message", value="message"),
        discord.app_commands.Choice(name="command", value="cmd")
    ]
)
async def server(interaction, run_opt:str, run_arg:str=None):#サーバー管理
    global config
    await interaction.response.defer()
    await interaction.followup.send("Executing Commands...")
    if run_opt == "open": #openメゾット(サーバー開始)
        if not win32gui.FindWindow(None, "Minecraft_server") == 0:
            await interaction.followup.send("ERROR : Server is already running. please try to `[/server shutdown]`")
        else:
            #サーバー解放
            subprocess.run(str(f'start {config["server_jar_path"]}'), shell=True)
            channel = client.get_channel(config["notify_channel"])
            await channel.send(f"@everyone {client.get_user(config['user_id']).name} 's Minecraft server starting...")
    elif run_opt == "reboot": # rebootメゾット(再起動)
        if win32gui.FindWindow(None, "Minecraft_server") == 0:
            await interaction.followup.send("ERROR : Server is not running. please try to `[/server open]`")
        else:
            #TODO 再起動を実装
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[再起動のお知らせ]§bこれより、§610§b秒後にサーバーが再起動します:理由:Discordから再起動コマンドが実行されたため。'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[再起動のお知らせ]§6 9'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[再起動のお知らせ]§6 8'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[再起動のお知らせ]§6 7'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[再起動のお知らせ]§6 6'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[再起動のお知らせ]§6 5'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[再起動のお知らせ]§6 4'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[再起動のお知らせ]§6 3'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[再起動のお知らせ]§6 2'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[再起動のお知らせ]§6 1'))
            asyncio.sleep(1)
            rcon_cmd('stop')
            channel = client.get_channel(config["channel_id"])
            await channel.send(f"@everyone {client.get_user(config['user_id']).name} 's minecraft server is shutting down. It will restart in a few seconds... Hold on a second!")
            asyncio.sleep(10)
            subprocess.run(str(f'start C:/minecraft_servers/script/start.bat {config["server_jar_path"]}'), shell=True)
    elif run_opt == "shutdown":#shutdownメゾット(シャットダウン)
        if win32gui.FindWindow(None, "Minecraft_server") == 0:
            await interaction.followup.send("ERROR : Server is not running. please try to `[/server open]`")
            return
        else:
            channel = client.get_channel(config["channel_id"])
            await channel.send(f"@everyone {client.get_user(config['user_id']).name} 's minecraft server shutting down...")
            #TODO シャットダウンを実装
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[シャットダウンのお知らせ]§bこれより、§610§b秒後にサーバーがシャットダウンします:理由:Discordからシャットダウンコマンドが実行されたため。'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[シャットダウンのお知らせ]§6 9'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[シャットダウンのお知らせ]§6 8'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[シャットダウンのお知らせ]§6 7'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[シャットダウンのお知らせ]§6 6'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[シャットダウンのお知らせ]§6 5'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[シャットダウンのお知らせ]§6 4'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[シャットダウンのお知らせ]§6 3'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[シャットダウンのお知らせ]§6 2'))
            asyncio.sleep(1)
            rcon_cmd(str('say [from] @' + interaction.user.name + '§c[シャットダウンのお知らせ]§6 1'))
            asyncio.sleep(1)
            rcon_cmd('stop')
            asyncio.sleep(10)
            subprocess.run('taskkill /im playit.exe /f', shell=True)
    elif run_opt == "message":#messageメゾット(メッセージを送る)
        if win32gui.FindWindow(None, "Minecraft_server") == 0:
            await interaction.followup.send("ERROR : Server is not running. please try to `[/server open]`")
            return
        else:
            rcon_cmd(str('say [from] @' + interaction.user.name + ' ' + run_arg))
    elif run_opt == 'cmd':
        if win32gui.FindWindow(None, "Minecraft_server") == 0:
            await interaction.followup.send("ERROR : Server is not running. please try to `[/server open]`")
        elif interaction.permissions.administrator:
            rcon_cmd(run_arg)
            await interaction.followup.send(str('@' + interaction.user.name + ' run command : ' + run_arg))
        else:
            await interaction.followup.send('ERROR : You dont have permissions "Admin". please check you have this permissions.', ephemeral=True)
    else:
        await interaction.followup.send(str("ERROR : command doesn't work: incorrect argments : " + run_opt))
        return
    await interaction.followup.send(":white_check_mark: Operation completed successfully.")
    return

@cmdtree.command(name="shutdown", description="BOTをシャットダウンします。(管理者権限を持っているユーザに限り)")
async def shutdown(interaction):
    if interaction.permissions.administrator:
        await interaction.response.send_message('Shut down the server bot', ephemeral=True)
        await client.close()
    else:
        await interaction.response.send_message('You dont have "Admin" permission. Make sure you have "Admin" permission', ephemeral=True)

init()
client.run(config['TOKEN'])