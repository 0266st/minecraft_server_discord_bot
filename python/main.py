import discord
from discord import app_commands
import subprocess
import win32gui
import time
import os
import json
import time
from dotenv import load_dotenv
load_dotenv()
Intents = discord.Intents.all()
Intents.members = True
client = discord.Client(intents=Intents)
cmdtree = app_commands.CommandTree(client)
vcclient = None
vcon = False
ajon = False
def_vcid = 0
config = []

def load_settings(filepath):
    try:
        with open(filepath) as f:
            settings = json.load(f)
    except FileNotFoundError:
        print(f"{filepath} is not found.")
        settings = {}
    return settings


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)
    print('change setting(s) : ')
    print(data) 


async def init():
    global vcon
    global ajon
    global def_vcid
    global config
    config = load_settings('C:\\minecraft_server\\script\\python\\settings.json') 
    vcon = config.get('vcon')
    ajon = config.get('ajon')
    def_vcid = int(config.get('def_vcid'))
    global vcclient
    vcclient = await client.get_channel(def_vcid).connect()


@client.event
async def on_ready():
    global vcclient
    await init()
    if ajon == 'true':
        time.sleep(1)
        vcclient.play(discord.FFmpegPCMAudio("C:\\minecraft_server\\script\\python\\sounds\\yomiageon.mp3"))
    print(str('config : '))
    print(config)
    print('vcclient : ')
    print(vcclient)
    await cmdtree.sync()


@cmdtree.command(name="server", description="サーバーの起動、再起動をコマンドで司ります。")
@discord.app_commands.choices(
    run_opt=[
        discord.app_commands.Choice(name="Open",value="open"),
        discord.app_commands.Choice(name="Reboot",value="reboot"),
        discord.app_commands.Choice(name="Shutdown", value="shutdown")
    ]
)
async def server(interaction, run_opt:str):
    global vcclient
    await interaction.response.defer()
    await interaction.followup.send("Executing Commands...")
    if run_opt == "open":
        if not win32gui.FindWindow(None, "Minecraft_java_server") == 0:
            await interaction.followup.send("ERROR : Server is already running. please try to `[/server shutdown]`")
            if vcon == 'true' and not vcclient == None:
                vcclient.play(discord.FFmpegPCMAudio("C:\\minecraft_server\\script\\python\\sounds\\serverisopen.mp3"))
        else:
            subprocess.run('start C:\\minecraft_server\\script\\start.bat', shell=True)
            channel = client.get_channel(1092386830147670056)
            await channel.send("@everyone <@1059732895473868820> 's Minecraft server starting...")
            print('vcclient : ')
            print(vcclient)
            print('vcon : ')
            print(vcon)
            if vcon == 'true' and not vcclient == None:
                vcclient.play(discord.FFmpegPCMAudio("C:\\minecraft_server\\script\\python\\sounds\\open.mp3"))
    elif run_opt == "reboot":
        if win32gui.FindWindow(None, "Minecraft_Java_server") == 0:
            await interaction.followup.send("ERROR : Server is not running. please try to `[/server open]`")
            if vcon == 'true' and not vcclient == None:
                vcclient.play(discord.FFmpegPCMAudio("C:\\minecraft_server\\script\\python\\sounds\\serverisopen.mp3"))
        else:
            subprocess.run('start C:\\minecraft_server\\script\\UWSC\\UWSC.exe C:\\minecraft_server\\script\\UWSC\\reboot.uws', shell=True)
            channel = client.get_channel(1092386830147670056)
            await channel.send("@everyone <@1059732895473868820> 's minecraft server is shutting down. It will restart in a few seconds... Hold on a second!")
            print('vcclient : ')
            print(vcclient)
            if vcon == 'true' and not vcclient == None:
                vcclient.play(discord.FFmpegPCMAudio("C:\\minecraft_server\\script\\python\\sounds\\reboot.mp3"))
    elif run_opt == "shutdown":
        if win32gui.FindWindow(None, "Minecraft_Java_server") == 0:
            await interaction.followup.send("ERROR : Server is not running. please try to `[/server open]`")
            if vcon == 'true' and not vcclient == None:
                vcclient.play(discord.FFmpegPCMAudio("C:\\minecraft_server\\script\\python\\sounds\\serverdoesntopen.mp3"))
        else:
            channel = client.get_channel(1092386830147670056)
            await channel.send("@everyone <@1059732895473868820> 's minecraft server shutting down...")
            subprocess.run('start C:\\minecraft_server\\script\\shutdown.bat', shell=True)
            subprocess.run('taskkill /f /im playit.exe', shell=True)
            if vcon == 'true' and not vcclient == None:
                vcclient.play(discord.FFmpegPCMAudio("C:\\minecraft_server\\script\\python\\sounds\\shutdown.mp3"))
    else:
        await interaction.followup.send(str("ERROR : command doesn't work: incorrect argments : " + run_opt))
    time.sleep(30)

@cmdtree.command(name="vc-cfg", description="VCチャンネルでのサーバー起動通知に関する設定をします。")
@discord.app_commands.choices(
    run_cmd=[
        discord.app_commands.Choice(name="AutoJoin-On", value="ajon"),
        discord.app_commands.Choice(name="AutoJoin-Off", value="ajoff"),
        discord.app_commands.Choice(name="Join",value="join"),
        discord.app_commands.Choice(name="Quit",value="quit"),
        discord.app_commands.Choice(name="VC-On", value="vcon"),
        discord.app_commands.Choice(name="VC-Off", value="vcoff"),
        discord.app_commands.Choice(name="Reload", value="reload")     
    ]
)
async def vc_cfg(interaction, run_cmd:str, def_vcid:str = None):
    global vcclient
    global vcon
    global ajon
    await interaction.response.defer()
    await interaction.followup.send('executing command(s)...')
    cnl = def_vcid
    channel = client.get_channel(cnl)
    if run_cmd == 'reload':
        await init()
        return
    elif run_cmd == 'join':
        if not channel.type == discord.ChannelType.voice:
            await interaction.response.send_message('Error : Specified channel is invalid or not a voice channel')
            return
        else:
            await interaction.followup.send(str('connect to <#' + str(cnl) + '>'))
            vcclient = await channel.connect()
    elif run_cmd == 'quit':
        if vcclient == None:
            await interaction.followup.send(str('Error: Unable to disconnect: Not connected to voice channel'))
            return
        else:
            await vcclient.disconnect()
    
    elif run_cmd == 'vcon':
        write_json({'vcon':'true'}, 'C:\\minecraft_server\\script\\settings.json')
        vcon = 'true'
        if vcon == 'true' and vcclient:
                await vcclient.play(discord.FFmpegPCMAudio("C:\\minecraft_server\\script\\python\\sounds\\vcon.mp3"))
    
    elif run_cmd == 'vcoff':
        write_json({'vcon':'false'}, 'C:\\minecraft_server\\script\\settings.json')
        if vcon == 'true' and vcclient:
            vcclient.play(discord.FFmpegPCMAudio("C:\\minecraft_server\\script\\python\\sounds\\vcoff.mp3"))
            vcclient.disconnect()
    
    elif run_cmd == 'ajon':
        if def_vcid == None:
            interaction.followup.send('Error: def_vcid value is invalid. Please check if it is the correct value')
            if vcon == 'true' and vcclient:
                vcclient.play(discord.FFmpegPCMAudio("C:\\minecraft_server\\script\\python\\sounds\\ajon.mp3"))
        write_json({'ajon':'true'}, 'C:\\minecraft_server\\script\\settings.json')

    elif run_cmd == 'ajoff':
        write_json({'ajon':'false'}, 'C:\\minecraft_server\\script\\settings.json')
        if vcon == 'true' and vcclient:
            vcclient.play(discord.FFmpegPCMAudio("C:\\minecraft_server\\script\\python\\sounds\\ajoff.mp3"))
    else:
        await interaction.response.send_message(str('invaild run_cmd : ' + run_cmd))
        return 
    time.sleep(30)



    
client.run(os.environ['TOKEN'])