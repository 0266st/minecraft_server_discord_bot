import discord
from discord import app_commands
import subprocess
import win32gui
import time
import os
import json
import time
import mcrcon
from dotenv import load_dotenv
load_dotenv()
rcserver = {
    'address' : os.environ['SERVER_ADDR'],
    'port' : os.environ['SERVER_PORT'],
    'server_pass': os.environ['SERVER_PASS']
}
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

def rcon_cmd(command):
    global rcserver
    with mcrcon.MCRcon(rcserver['address'], rcserver['server_pass'], int(rcserver['port'])) as mcr:
        log=mcr.command(command)
        return log

def write_json(filename):
    global vcon
    global ajon
    global def_vcid
    f = open(filename, "w")
    f.write(str('{"vcon":'+'"'+vcon+'"'+',"ajon":'+'"'+ajon+'"'+',"def_vcid":'+'"'+str(def_vcid)+'"'+'}'))
    f.close()
    print('change setting(s) : ')
    print(str('{"vcon":'+"'"+vcon+"'"+',"ajon":'+'"'+ajon+"'"+',"def_vcid":'+"'"+str(def_vcid)+"'"+'}'))


async def init():
    global vcon
    global ajon
    global def_vcid
    global config
    global vcclient
    config = load_settings('C:/minecraft_servers/script/settings.json') 
    vcon = config.get('vcon')
    ajon = config.get('ajon')
    def_vcid = int(config.get('def_vcid'))
    if vcclient == None:
        if ajon == 'true':
            vcclient = await client.get_channel(def_vcid).connect()
    else:
        await vcclient.disconnect()


@client.event
async def on_ready():
    global vcclient
    await init()
    if ajon == 'true':
        if vcclient.is_playing():
            vcclient.stop()
        vcclient.play(discord.FFmpegPCMAudio("C:/minecraft_servers/script/python/sounds/yomiageon.mp3"))
    channel = client.get_channel(1092386830147670056)
    await channel.send(" :warning: WARNING : This is a test version(v1.2.0).")
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
        discord.app_commands.Choice(name="Shutdown", value="shutdown"),
        discord.app_commands.Choice(name="Message", value="message"),
        discord.app_commands.Choice(name="command", value="cmd")
    ]
)
async def server(interaction, run_opt:str, run_arg:str=None):#サーバー管理
    global vcclient
    await interaction.response.defer()
    await interaction.followup.send("Executing Commands...")
    if run_opt == "open": #openメゾット(サーバー開始)
        if not win32gui.FindWindow(None, "Minecraft_server") == 0:
            await interaction.followup.send("ERROR : Server is already running. please try to `[/server shutdown]`")
            if vcon == 'true' and not vcclient == None:
                if vcclient.is_playing():
                    vcclient.stop()
                vcclient.play(discord.FFmpegPCMAudio("C:/minecraft_servers/script/python/sounds/serverisopen.mp3"))
                return
        else:
            #サーバー解放
            subprocess.run('start C:/minecraft_servers/playit/playit.exe', shell=True)
            subprocess.run(str('start C:/minecraft_servers/script/start.bat'), shell=True)
            channel = client.get_channel(1092386830147670056)
            await channel.send("@everyone <@1059732895473868820> 's Minecraft server starting...")
            print('vcclient : ')
            print(vcclient)
            print('vcon : ')
            print(vcon)
            if vcon == 'true' and not vcclient == None:
                if vcclient.is_playing():
                    vcclient.stop()
                vcclient.play(discord.FFmpegPCMAudio("C:/minecraft_servers/script/python/sounds/open.mp3"))
    elif run_opt == "reboot": # rebootメゾット(再起動)
        if win32gui.FindWindow(None, "Minecraft_server") == 0:
            await interaction.followup.send("ERROR : Server is not running. please try to `[/server open]`")
            if vcon == 'true' and not vcclient == None:
                vcclient.play(discord.FFmpegPCMAudio("C:/minecraft_servers/script/python/sounds/serverisopen.mp3"))
                return
        else:
            #TODO 再起動を実装
            rcon_cmd('stop')
            channel = client.get_channel(1092386830147670056)
            await channel.send("@everyone <@1059732895473868820> 's minecraft server is shutting down. It will restart in a few seconds... Hold on a second!")
            if vcon == 'true' and not vcclient == None:
                if vcclient.is_playing():
                    vcclient.stop()
                vcclient.play(discord.FFmpegPCMAudio("C:/minecraft_servers/script/python/sounds/reboot.mp3"))
            time.sleep(10)
            subprocess.run(str('start C:/minecraft_servers/script/start.bat'), shell=True)
            print('vcclient : ')
            print(vcclient)
    elif run_opt == "shutdown":#shutdownメゾット(シャットダウン)
        if win32gui.FindWindow(None, "Minecraft_server") == 0:
            await interaction.followup.send("ERROR : Server is not running. please try to `[/server open]`")
            if vcon == 'true' and not vcclient == None:
                if vcclient.is_playing():
                    vcclient.stop()
                vcclient.play(discord.FFmpegPCMAudio("C:/minecraft_servers/script/python/sounds/serverdoesntopen.mp3"))
                return
        else:
            channel = client.get_channel(1092386830147670056)
            await channel.send("@everyone <@1059732895473868820> 's minecraft server shutting down...")
            #TODO シャットダウンを実装
            rcon_cmd('stop')
            if vcon == 'true' and not vcclient == None:
                if vcclient.is_playing():
                    vcclient.stop()
                vcclient.play(discord.FFmpegPCMAudio("C:/minecraft_servers/script/python/sounds/shutdown.mp3"))
            time.sleep(10)
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
            if vcon == 'true' and not vcclient == None:
                if vcclient.is_playing():
                    vcclient.stop()
                vcclient.play(discord.FFmpegPCMAudio("C:/minecraft_servers/script/python/sounds/serverdoesntopen.mp3"))
                return
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
async def vc_cfg(interaction, run_cmd:str, set_vcid:str = None):
    global vcclient
    global vcon
    global ajon
    global def_vcid
    await interaction.response.defer()
    await interaction.followup.send('executing command(s)...')
    cnl = def_vcid
    print('cnl : ')
    print(cnl)
    channel = client.get_channel(cnl)
    print('channel : ')
    print(channel)
    if not set_vcid == None:
        def_vcid = set_vcid
        write_json('C:/minecraft_servers/script')
    if run_cmd == 'reload':
        await init()
        print(vcclient)
        print(vcon)
        if vcon == 'true' and vcclient:
            if vcclient.is_playing():
                    vcclient.stop()
            vcclient.play(discord.FFmpegPCMAudio("C:/minecraft_servers/script/python/sounds/reload.mp3"))
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
        write_json('C:/minecraft_servers/script/settings.json')
        vcon = 'true'
        if vcon == 'true' and vcclient:
                if vcclient.is_playing():
                    vcclient.stop()
                vcclient.play(discord.FFmpegPCMAudio("C:/minecraft_servers/script/python/sounds/vcon.mp3"))
    
    elif run_cmd == 'vcoff':
        vcon = 'false'
        ajon = 'false'
        write_json('C:/minecraft_servers/script/settings.json')
        if vcon == 'true' and vcclient:
            if vcclient.is_playing():
                    vcclient.stop()
            vcclient.play(discord.FFmpegPCMAudio("C:/minecraft_servers/script/python/sounds/vcoff.mp3"))
            await vcclient.disconnect()
    
    elif run_cmd == 'ajon':
        ajon = 'true'
        if def_vcid == None:
            interaction.followup.send('Error: def_vcid value is invalid. Please check if it is the correct value')
        write_json('C:/minecraft_servers/script/settings.json')
        if vcon == 'true' and vcclient:
            if vcclient.is_playing():
                    vcclient.stop()
            vcclient.play(discord.FFmpegPCMAudio("C:/minecraft_servers/script/python/sounds/ajon.mp3"))

    elif run_cmd == 'ajoff':
        ajon = 'false'
        write_json('C:/minecraft_servers/script/settings.json')
        if vcon == 'true' and vcclient:
            if vcclient.is_playing():
                    vcclient.stop()
            vcclient.play(discord.FFmpegPCMAudio("C:/minecraft_servers/script/python/sounds/ajoff.mp3"))
    else:
        await interaction.response.send_message(str('invaild run_cmd : ' + run_cmd))
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

client.run(os.environ['TOKEN'])