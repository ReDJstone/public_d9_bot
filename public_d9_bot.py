import asyncio
import discord
import websockets
import re
from discord.ext import commands
from pytube import YouTube
import validators
import os
import random
import ffmpeg


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='-', case_insensitive=True, description='ReDJBoT', help_command=None, intents=intents)

vars = {
    "chat": "ic",
    "watch": "all",
    "callwords": 'off'
}


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Attorney Online | d9!"))
    global red, msgs_channel, d9_discord_lobby
    red = await bot.fetch_user(226408382448402433)
    msgs_channel = await bot.fetch_channel(1017848437577875507)
    d9_discord_lobby = await bot.fetch_channel(1008073342248550430)
    await msgs_channel.send('Bot Connected.')


@bot.event
async def on_message(ctx):
    if ctx.channel.id == msgs_channel.id:
        if ctx.author.id == 226408382448402433:
            if str(ctx.content).startswith(bot.command_prefix):
                await bot.process_commands(ctx)

        elif ctx.author.id != bot.user.id:
            await ctx.channel.send(
                'Anda! No esperaba que nadie me mandara un mensaje privado! Gracias! Toma una galleta! :cookie:')
            await msgs_channel.send('DM from <@{}>: {}'.format(ctx.author, ctx.content))
            return

@bot.command()
async def test(ctx):
    return


@bot.command()
async def pair(ctx):
    response = await set_msg_param("self_offset", '-15<and>0')
    await ctx.send(response)
    response = await set_msg_param("other_charid", ctx.message.content[6:])
    await ctx.send(response)
    '''
    [20] AAI Franziska
    [26] Adrian
    [61] Blackquill DD Wit
    [62] BlackquillSoJ
    [63] BlackquillSoJCo
    '''


@bot.command()
async def unpair(ctx):
    response = await set_msg_param("self_offset", '0<and>0')
    await ctx.send(response)
    response = await set_msg_param("other_charid", '-1')
    await ctx.send(response)


@bot.command()
async def emote(ctx):
    response = await set_msg_param("emote", ctx.message.content[7:])
    await ctx.send(response)


@bot.command()
async def offset(ctx):
    off_x = ctx.message.content[8:].split(', ')[0]
    off_y = ctx.message.content[8:].split(', ')[1]
    response = await set_msg_param("self_offset", f'{off_x}<and>{off_y}')
    await ctx.send(response)


@bot.command()
async def msgpref(ctx):
    param = ctx.message.content[9:].split(', ')[0]
    value = ctx.message.content[9:].split(', ')[1:][0]
    response = await set_msg_param(param, value)
    await ctx.send(response)


@bot.command()
async def usrpref(ctx):
    param = ctx.message.content[9:].split(', ')[0]
    value = ctx.message.content[9:].split(', ')[1:][0]
    response = await set_usr_param(param, value)
    await ctx.send(response)


@bot.command()
async def custom(ctx):
    await msgs_channel.send(ctx.message.content[8:])


@bot.command()
async def char(ctx):
    await change_character(ctx.message.content[6:])


@bot.command()
async def area(ctx):
    await change_area(ctx.message.content[6:])

@bot.command()
async def yt_toggle(ctx):
    if client_params["yt"]:
        client_params["yt"] = False
        await ctx.send('Youtube music disabled in AO')
    else:
        client_params["yt"] = True
        await ctx.send('Youtube music enabled in AO')

@bot.command()
async def checkall(ctx):
    await msgs_channel.send(re.sub(', ', '\n', f'```Vars:\n{vars}```'))
    await msgs_channel.send(re.sub(', ', '\n', f'```Msg_params:\n{msg_params}```'))
    await msgs_channel.send(re.sub(', ', '\n', f'```Client_Params:\n{client_params}```'))


@bot.command()
async def stop(ctx):
    await ctx.send('Stopping...')
    await shutdown(loop)

# =======================================


msg_params = {
    "desk_mod": "0",
    "preanim": "-",
    "emote": "normal",
    "messages": [],
    "sfx_name": "0",
    "emote_modifier": "0",
    "sfx_delay": "0",
    "shout_modifier": "9",
    "evidence": "0",
    "flip": "0",
    "realization": "0",
    "text_color": "0",
    "other_charid": "-1",
    "self_offset": "0<and>0",
    "noninterrupting_preanim": "1",
    "sfx_looping": "0",
    "screenshake": "0",
    "frames_shake": "-",
    "frames_realization": "-",
    "frames_sfx": "-",
    "additive": "0",
    "effect": "||"
}


# MC#Tribunal 1#2#%
client_params = {
    "ID": 0,
    "area_name": "Lobby",
    "showname": "BeeBot",
    "server_name": "BeeBot",
    "character": "TsumugiShirogane HD",
    "side": "wit",
    "char_id": 8,
    "rng_red": 10,
    "yt": False
}

rcv_queue = []

async def receive_msg():
    await asyncio.sleep(5)
    global rcv_msg
    while True:
        received_message = await ws.recv()
        if str(received_message).startswith('ID#'):
            client_params["ID"] = received_message.split('#')[1]
            await ws.send(f'CC#{client_params["ID"]}#-1#web#%')
            print(f'Assigned ID: {client_params["ID"]}')
            await change_character(client_params["char_id"])
            #await ws.send(f'CT#{client_params["server_name"]}#/area 23#%')
            await change_character(client_params["char_id"])
            #await ws.send(
            #    f'MS#{msg_params["desk_mod"]}#{msg_params["preanim"]}#{client_params["character"]}#{msg_params["emote"]}#BOT Enabled.#{client_params["side"]}#{msg_params["sfx_name"]}#{msg_params["emote_modifier"]}#{client_params["char_id"]}#{msg_params["sfx_delay"]}#{msg_params["shout_modifier"]}#{msg_params["evidence"]}#{msg_params["flip"]}#{msg_params["realization"]}#{msg_params["text_color"]}#{client_params["showname"]}#{msg_params["other_charid"]}#{msg_params["self_offset"]}#{msg_params["noninterrupting_preanim"]}#{msg_params["sfx_looping"]}#{msg_params["screenshake"]}#{msg_params["frames_shake"]}#{msg_params["frames_realization"]}#{msg_params["frames_sfx"]}#{msg_params["additive"]}#{msg_params["effect"]}#%')

        elif str(received_message).startswith('TI#') or str(received_message).startswith('CHECK#') or str(
                received_message).startswith('ARUP#') or str(
                received_message).startswith('FM#') or str(
                received_message).startswith('CharsCheck#'):
            continue

        elif str(received_message).startswith('MS#'):  # IC Message
            rcv_msg = received_message.split('#')[5]
            msg_author = received_message.split('#')[16] # El showname
            author_char = received_message.split('#')[3]
            if not msg_author:
                msg_author = author_char

            if rcv_msg.lower().startswith('bee!') or 'beebot' in str(rcv_msg).lower() and msg_author not in ['BeeBot']:
                await process_ao_commands("ic", rcv_msg, msg_author)

        elif str(received_message).startswith('CT#'):  # OOC Message
            rcv_msg = received_message.split('#')[2]
            msg_author = received_message.split('#')[1]

            if (rcv_msg.lower().startswith('bee!') or 'beebot' in str(rcv_msg).lower()) and msg_author not in ['<dollar>D9', '[BOT]BeeBot']:
                await process_ao_commands("ooc", rcv_msg, msg_author)
            else:
                print(received_message)

        else:
            print(received_message)


async def process_ao_commands(ic_or_ooc, msg, msg_author):
    response = ''
    temp_emote = None
    print(f'Received: {msg}')
    if 'beebot' in str(msg).lower() and not msg.lower().startswith('bee!'):
        line_cnt = int(sum(1 for line in open("{}/comandos/mention.txt".format(os.path.dirname(__file__)))) - 1)
        rng = random.randint(0, line_cnt)
        response = (str(open("{}/comandos/mention.txt".format(os.path.dirname(__file__))).readlines()[rng]))

    elif str(msg).lower().startswith('bee!'):
        command = msg.split(' ')[0][4:]

        if command == 'ping':
            response = ('Pong! {}ms'.format(round(bot.latency * 1000, 5)))

        elif command == 'yt' and client_params["yt"]:
            response = await yt(msg.split(' ')[1], msg_author)

        elif command == 'insulta':
            target = ''
            if len(msg.split(' ')) > 1:
                if 'beebot' in ''.join(msg.split(' ')[1:]).lower():
                    response = '[explain2] No voy a insultarme a mí misma porque tú quieras, {}!'.format(msg_author)
                elif len(msg.split(' ')) <= 1:
                    target = msg.split(' ')[1]
                else:
                    target = ' '.join(msg.split(' ')[1:])
            else:
                target = msg_author

            if not response:
                line_cnt = int(
                    sum(1 for line in open("{}/comandos/insultos.txt".format(os.path.dirname(__file__)))) - 1)
                rng = random.randint(0, line_cnt)
                frase = str(open("{}/comandos/insultos.txt".format(os.path.dirname(__file__))).readlines()[rng])
                temp_emote = random.choice(['explain2', 'm-point2', 'point'])
                response = ('[{}] {}, ¡{}!'.format(temp_emote, target, frase.strip()))

        else:
            return

    if response:
        print(f'Response: {response}')
        if response.startswith('['):
            temp_emote = response.split('] ')[0][1:]
            response = response.split('] ')[1].lower().capitalize().strip()
        else:
            response = response.strip()

        await asyncio.sleep(2)
        if ic_or_ooc == 'ooc' or response.startswith('http'):
            print(f'Sending OOC: {response}...')
            await send_ooc(response)
        elif ic_or_ooc == 'ic':
            print(f'Sending IC: {response}...')
            await send_ic(response, emote=temp_emote)



    '''
    command = globals()[msg.split(' ')[0][3:]]
    response = command(msg)
    if ic_or_ooc == "ic":
        await send_ic(response)
    elif ic_or_ooc == "ooc":
        await send_ooc(response)
    '''

async def yt(link, msg_author):
    if validators.url(link):
        # Download file
        yt = YouTube(link)
        secs = int(yt.length % 60)
        mins = int((yt.length - secs) / 60)
        if mins <= 10:
            await send_ooc(f"Tema solicitado: {yt.title} , duración: {mins}:{secs}.")
        else:
            await send_ooc(f"La duración de {yt.title} es {mins}:{secs}! El límite es de 10 minutos!")
            return
        ys = yt.streams.filter(only_audio=True)
        out_file = ys[0].download('music/')

        # Convert to opus
        base, ext = os.path.splitext(out_file)
        new_file = f'{base}.opus'

        video = ffmpeg.input(out_file)
        stream = ffmpeg.output(video.audio, new_file)
        ffmpeg.run(stream)
        #subprocess.run(['music\\ffmpeg.exe', '-i', out_file, new_file])
        # Send to discord and copy link
        try:
            messaged_file = await msgs_channel.send(content=f'{msg_author}:', file=discord.File(new_file))
            file_url = messaged_file.attachments[0].url
            await send_ooc(f'/play {file_url}')
            await d9_discord_lobby.send(f'Playing:\n{link}')
            response = ''
        except Exception as e:
            await msgs_channel.send(f'```{e}```')
            response = 'La canción es demasiado pesada! (límite: 8MB, necesita poder enviarse a discord!)'

        os.remove(out_file)
        os.remove(new_file)

    else:
        response = f'El comando se usa: bee!yt youtube_link . Inténtalo de nuevo.'

    return response

async def send_ic(message, emote=None):
    # MS#chat#-#Adrian#normal#asdgsdf#wit#0#0#2#0#0#0#0#0#0##-1#0<and>0#0#0#0#-#-#-#0#||#%
    msg_params['message'] = message
    if emote:
        await ws.send(
            f'MS#{msg_params["desk_mod"]}#{msg_params["preanim"]}#{client_params["character"]}#{emote}#{msg_params["message"]}#{client_params["side"]}#{msg_params["sfx_name"]}#{msg_params["emote_modifier"]}#{client_params["char_id"]}#{msg_params["sfx_delay"]}#{msg_params["shout_modifier"]}#{msg_params["evidence"]}#{msg_params["flip"]}#{msg_params["realization"]}#{msg_params["text_color"]}#{client_params["showname"]}#{msg_params["other_charid"]}#{msg_params["self_offset"]}#{msg_params["noninterrupting_preanim"]}#{msg_params["sfx_looping"]}#{msg_params["screenshake"]}#{msg_params["frames_shake"]}#{msg_params["frames_realization"]}#{msg_params["frames_sfx"]}#{msg_params["additive"]}#{msg_params["effect"]}#%')
    else:
        await ws.send(
            f'MS#{msg_params["desk_mod"]}#{msg_params["preanim"]}#{client_params["character"]}#{msg_params["emote"]}#{msg_params["message"]}#{client_params["side"]}#{msg_params["sfx_name"]}#{msg_params["emote_modifier"]}#{client_params["char_id"]}#{msg_params["sfx_delay"]}#{msg_params["shout_modifier"]}#{msg_params["evidence"]}#{msg_params["flip"]}#{msg_params["realization"]}#{msg_params["text_color"]}#{client_params["showname"]}#{msg_params["other_charid"]}#{msg_params["self_offset"]}#{msg_params["noninterrupting_preanim"]}#{msg_params["sfx_looping"]}#{msg_params["screenshake"]}#{msg_params["frames_shake"]}#{msg_params["frames_realization"]}#{msg_params["frames_sfx"]}#{msg_params["additive"]}#{msg_params["effect"]}#%')

async def send_ooc(message):
    # CT#[M]ReDJstone#Testing#%
    await ws.send(f'CT#{client_params["server_name"]}#{message}#%')


async def set_msg_param(param, value):
    if param in msg_params.keys():
        msg_params[param] = value
        return f'Message `{param}` set to `{value}`.'
    else:
        return f'Message `{param}` NOT FOUND.'


async def set_usr_param(param, value):
    if param in client_params.keys():
        client_params[param] = value
        return f'Client `{param}` set to `{value}`.'
    else:
        return f'Client `{param}` NOT FOUND.'


async def mod_login(password):
    await ws.send(f'CT#{client_params["server_name"]}#/login {password}#%')


async def change_character(char_id):
    client_params["char_id"] = int(char_id)
    await ws.send(f'CC#{client_params["ID"]}#{client_params["char_id"]}#web#%')


async def change_area(area_name):
    # MC#area_name#char_id#%
    client_params["area_name"] = area_name
    await ws.send(f'MC#{client_params["area_name"]}#{client_params["char_id"]}#%')


'''
async def play():
    link = None
    if str(ctx.message.content).startswith('-'):
        link = str(ctx.message.content[6:])
    elif str(ctx.message.content).startswith('d9!'):
        link = str(ctx.message.content[8:])
    print(link)

    if validators.url(link):
        # Download file
        yt = YouTube(link)
        await ctx.send(f"Title: {yt.title}")
        ys = yt.streams.get_highest_resolution()
        out_file = ys.download('music/')

        # Rename to .mp3
        base, ext = os.path.splitext(out_file)
        new_file = f'{base}.mp3'
        os.rename(out_file, new_file)

        # Send to discord and copy link
        try:
            messaged_file = await ctx.send(file=discord.File(f'{new_file}'))
            file_url = messaged_file.attachments[0].url
            await send_ooc(f'/play {file_url}')
        except:
            await ctx.send('The song is too large to send to discord!')
        # Delete file to avoid bullshit.
        os.remove(f'{new_file}')

    else:
        ctx.send(f'The command is used: -play youtube_link . Try again.')
'''



def handle_exception(loop, context):
    msg = context.get("exception", context["message"])
    print(f"Caught exception: {msg}")
    print("Shutting down...")
    asyncio.create_task(shutdown(loop))


async def shutdown(loop, signal=None):
    """Cleanup tasks tied to the service's shutdown."""
    if signal:
        print(f"Received exit signal {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]
    [task.cancel() for task in tasks]
    print(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


async def main():
    global ws
    async with websockets.connect('ws://tribunaldistrito9.ddns.net:27017', ping_interval=None, ping_timeout=None) as ws:
    #async with websockets.connect('ws://127.0.0.1:50001', ping_interval=None, ping_timeout=None) as ws:
        await ws.send('HI#D9_BoT#%')
        await ws.send('ID#webAO#webAO#%')
        await ws.send('RD#%')
#        await ws.send(f'CT#{client_params["server_name"]}#/hub 2#%')
        await ws.send(f'CT#{client_params["server_name"]}#BeeBot ONLINE.#%')
        while True:
            await ws.send(f'CH#{client_params["char_id"]}#%')
            await asyncio.sleep(5)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.create_task(receive_msg())
    #loop.set_exception_handler(handle_exception)
    loop.create_task(bot.run('OTgzODI1MTkzNDE3OTkwMTg0.G4nsGR.gWIgHStbNCvDY-Yrg42nxVKyxmOXOAYAIJeW1M'))
    loop.run_forever()

'''
Char IDs:

[20] AAI Franziska
[26] Adrian
[61] Blackquill DD Wit
[62] BlackquillSoJ
[63] BlackquillSoJCo


[0] iniswap1
[1] iniswap2
[2] iniswap3
[3] iniswap4
[4] iniswap5
[5] iniswap6
[6] iniswap7
[7] iniswap8
[8] iniswap9
[9] iniswap10
[10] iniswap11
[11] iniswap12
[12] iniswap13
[13] iniswap14
[14] iniswap15
[15] iniswap16
[16] iniswap17
[17] iniswap18
[18] iniswap19
[19] iniswap20
[20] AAI Franziska
[21] AAI_Gumshoe
[22] AAIEdgey
[23] AAIManfred
[24] Acro
[25] Adam Redifast
[26] Adrian
[27] Ahlbi
[28] Apollo
[29] ApolloCoDLC
[30] ApolloDD
[31] ApolloDD DLC
[32] ApolloDD Wit2
[33] ApolloPro
[34] ApolloSOJ
[35] ApolloSoJWit
[36] April
[37] Alita
[38] Alita Tiala
[39] Angel
[40] Angel Starr
[41] Athena
[42] Athena DD Wit
[43] Athena DD Wit School
[44] Athena Maid W
[45] Athena WC
[46] AthenaCo
[47] AthenaCoDLC
[48] AthenaCykesSOJ
[49] AthenaH
[50] AthenaSOJ
[51] AthenaW
[52] AthenaWit
[53] Atmey
[54] Bailiff
[55] Bailiff GB
[56] Bailiff JP
[57] Bailiffs
[58] BandagedApollo
[59] Badd
[60] Blackquill
[61] Blackquill DD Wit
[62] BlackquillSoJ
[63] BlackquillSoJCo
[64] BlackquillSoJWit
[65] BlackquillWit
[66] Bobby
[67] Bonny de Famme
[68] Butz
[69] ButzEdgeworth
[70] ButzSOJ
[71] Cammy
[72] Clonco
[73] Co-Hobo
[74] Colias
[75] Colias Palaeno
[76] Cosmos
[77] Cosmos2
[78] darkthena
[79] darkgodot
[80] de Killer
[81] deKiller
[82] Dhurke
[83] Dhurke D
[84] Dhurke Def
[85] Diego
[86] DiegoDef
[87] DrHotti
[88] Duet
[89] Edgeworth
[90] EdgeworthAAI
[91] EdgeworthSOJ
[92] Edgeworthw
[93] Ema
[94] Ema H HD
[95] EmaAJ
[96] EmaSkye
[97] EmaSOJ
[98] Fawles
[99] Feenie
[100] Franny
[101] Franziska
[102] Franziska AAI
[103] Franziska AAI Young
[104] Franziska v K
[105] FranziskaGK
[106] Fulbright
[107] Furio
[108] Gant
[109] Gaspen
[110] GaspenSOJ
[111] Gavin
[112] Gavin K
[113] Godot
[114] Godot HLD
[115] GodotW
[116] Gregory
[117] Gregory AAI
[118] GregoryAAI
[119] Grossberg
[120] Gumshoe
[121] Gumshoe AAI
[122] Gumshoey
[123] GunBailiff
[124] Hobbes Def
[125] Hobo_Phoenix
[126] HoboApollo
[127] HoboDef
[128] HoboPhoenix
[129] Hotti
[130] Hugh
[131] Ini
[132] Jinxie
[133] Judge
[134] Judge C
[135] Judge ET
[136] Judge GB
[137] Judge GK
[138] Judge GK2
[139] Judge JP
[140] Judge Labyrinthia Edit
[141] JudgeBro
[142] JudgeCalifornia
[143] JudgeDGS
[144] JudgeDGS-ENG
[145] JudgeDGS-JAP
[146] JudgeKhura_in
[147] JudgeKhura'in
[148] Judge's Bro
[149] JudgeSOJ
[150] June
[151] Juniper
[152] Juniper Casual
[153] Juniper School
[154] Kay
[155] Kay Injured
[156] Klav
[157] Klavier
[158] Klavier DD Wit
[159] KlavierDD
[160] Kristoph
[161] Kristoph G
[162] Kristoph Gavin
[163] Kristoph H ET
[164] Kudo
[165] Lana
[166] LanaP
[167] Lang
[168] LangW
[169] Lbelle
[170] Long Lang
[171] Lotta
[172] Maggey
[173] Manfred
[174] Manfred AAI
[175] ManfredAAI
[176] ManfredW
[177] Marshall
[178] Maya
[179] Maya PXZ
[180] MayaDA
[181] MayaKid
[182] MayaPLvsAA
[183] MayaPLvsAA Co
[184] MayaPLvsAA Co Knight
[185] MayaSOJ
[186] Means
[187] Meekins
[188] Mia
[189] Mia Leg
[190] Mia Young
[191] Michael Eaglesworth
[192] Miles
[193] Miles D
[194] Miles ET
[195] miles pxz
[196] Miles Y HD
[197] MilesAAI
[198] MilesDD
[199] MilesKid
[200] MilesSOJ
[201] Payne
[202] Payne DGS
[203] Payne DGS Wit
[204] Payne Max
[205] Payne SOJ
[206] Payne Train v2
[207] Pearl
[208] Pearl Teen Comfy
[209] PearlSOJ
[210] PearlSOJ Def
[211] PearlSOJ2D
[212] Phoenix
[213] Phoenix Counsel
[214] Phoenix Hobo
[215] Phoenix pxz
[216] Phoenix WIT
[217] Phoenix Young
[218] PhoenixDD
[219] PhoenixDDWit
[220] PhoenixSOJ
[221] ProsecutorJustice
[222] ProsecutorJusticeW
[223] Quercus Alba
[224] Raymond
[225] Raymond Shields
[226] Raymond Shields Young
[227] Regina
[228] Regina AAI
[229] Shih-na
[230] Shi-Long
[231] Small Trucy
[232] Starbuck
[233] Trucy
[234] Trucy Def
[235] Trucy Pro
[236] Trucy SOJ
[237] Trucy Young
[238] TrucyH
[239] TrucySOJ
[240] Tyrell Badd
[241] Valant
[242] Vasquez
[243] Wellington
[244] White
[245] Winston
[246] WinstonPayne
[247] Wocky
[248] Wocky Kitaki
[249] Wright
[250] WrightPolly
[251] Y Kristoph
[252] Yanni
[253] Yew
[254] Young Klavier
[255] Young Mia
[256] YoungAAIEdgeworth
[257] YoungEdgeworth
[258] YoungRaymond
[259] Alba
[260] Aldante
[261] Altamont
[262] Amara
[263] Andistandhin
[264] Anna Mittlemont
[265] Archibald Doctor
[266] Armie
[267] Armstrong
[268] Asougi
[269] AsougiPro
[270] Auchi
[271] Aura
[272] Barnham
[273] Barok
[274] Barok van Zieks
[275] Barok Wit
[276] Barok Z
[277] Barrows
[278] Bellboy
[279] Ben
[280] Beppo
[281] Betty de Famme
[282] Bikini
[283] Bikini and Elise
[284] Blaise
[285] Blaise Debeste
[286] Bongo
[287] Bonnie and Karin
[288] Bonnie_Karin
[289] Bowl
[290] Brisbane
[291] Brisbane W
[292] Artemis Injustice
[293] Bucky
[294] Buddy
[295] Burley
[296] Butch Browning
[297] Byrne
[298] Caeser Villan
[299] Calisto
[300] Canon
[301] Charles
[302] Cicatrice
[303] Cindy
[304] Cindy Law
[305] Cody
[306] Connor
[307] Courtney
[308] Crab
[309] Crogrey
[310] Dahlia
[311] Dane Gustavia
[312] Darklaw
[313] Daryan
[314] Daryan Crescend
[315] Datz
[316] Decargo
[317] Delia
[318] Delicia
[319] Deplume
[320] Desiree
[321] Di-Jun Huang
[322] Dmitri
[323] Dogen
[324] Donnabella
[325] Drebber
[326] Drew
[327] Eddy Swop
[328] Eldoon
[329] Elise
[330] Ellen
[331] Ernest
[332] Ernest Amano
[333] Espella
[334] Everyday
[335] Filch
[336] Florent
[337] Ga'ran
[338] Geiru
[339] Gina DGS2
[340] Gina Lestrade
[341] Gina Lestrade Coat
[342] Gotts
[343] Goulloyne
[344] Gregson
[345] Greisen
[346] Grey
[347] Gustavia
[348] Guy
[349] Iris
[350] Iris Watson
[351] IrisHolmes
[352] IrisWatson
[353] IrisWatsonAssistant
[354] Old Phoenix
[355] Oldbag
[356] Olga
[357] Olga Orly
[358] Plum
[359] Plum Kitaki
[360] Polly
[361] Ponco
[362] Portsman
[363] PsycheLocks
[364] Sherlock
[365] Sherlock Casual
[366] Sherlock Goggled
[367] Sherlock Undercover
[368] SherlockWatson
[369] Moe
[370] Haori
[371] Hawk
[372] Helper Snow
[373] Hemlock
[374] Hobbes
[375] Holmes
[376] Hosonaga
[377] Huang
[378] Hutch Windibank
[379] Inga
[380] Jay Elbird
[381] Jeffrey Master
[382] Jezail
[383] Joan Garrideb
[384] Joan Garrideb Juror
[385] John
[386] John Garrideb
[387] John Marsh
[388] Josephine
[389] Justice
[390] Justine Courtney
[391] Justine CourtneyPro
[392] Katherine
[393] Katherine Hall
[394] Kazuma
[395] Kazuma Assistant
[396] Kazuma DGS2
[397] Kazuma DGS2 Wit
[398] Kazuma W
[399] KazumaKiryu
[400] Kidworth AAI
[401] Kira
[402] Knightley
[403] Lablanc
[404] Lamiroir
[405] Lance
[406] Lance Amano
[407] Lauren
[408] Lauren Paups
[409] LeTouse
[410] Lional Taylor
[411] Lisa
[412] Luis
[413] Machi
[414] Machi Tobaye
[415] Mae
[416] Maiday
[417] Mamemomi
[418] Maria
[419] Marlon Rimes
[420] Marsh
[421] Matilda
[422] Matilda Headset
[423] Matt
[424] Maurice
[425] Max
[426] Megundal
[427] Mikotoba
[428] Morgan
[429] Morgan Fey
[430] MrHat
[431] Nahyuta
[432] Narcissus
[433] Natsume
[434] Neil
[435] NeilW
[436] Nemmy Tinpillar
[437] Newman
[438] Nicole
[439] Nicole Swift
[440] Nikomina
[441] Nikomina Hatless
[442] Olivia
[443] O'Malley
[444] O'Reil
[445] Orla
[446] Oscar Fairplay
[447] Oscar Fairplay Juror
[448] Parker
[449] Patricia
[450] Patrick
[451] Paul Atishon
[452] Paynes
[453] Pees'lubin
[454] Penny
[455] Radio
[456] Retinz
[457] Rhoda
[458] Rhoda Teneiro
[459] Richard
[460] Rimes
[461] Roger Retinz
[462] Rola
[463] Ron
[464] Roylott
[465] Rozaic
[466] Rumba
[467] Ryu Arm
[468] Ryu Leg
[469] Ryunosuke
[470] Ryunosuke Witness
[471] Ryutaro
[472] Ryuunosuke
[473] Ryuutarou
[474] Sahwit
[475] Sailor
[476] Sal
[477] Sanmon
[478] Sasha
[479] Sasha Buckler
[480] Sebastian
[481] Seishirou
[482] Shiv
[483] Simon
[484] Simon Clown
[485] Sirhan Dogen
[486] Sithe
[487] Small Vera
[488] Smiles
[489] Sonohigurashi
[490] Sorin
[491] Souseki
[492] Spark
[493] Stickler
[494] Stroganov
[495] Sumireko
[496] Susato
[497] Susato Def
[498] Susato DLC
[499] Susato hld
[500] SusatoDef
[501] TakaHawk
[502] Ted
[503] Teikan Dragons
[504] Tenma
[505] Thomas
[506] Tobias
[507] Tobias Gregson
[508] Tonate
[509] Tully Tinpillar
[510] Uendo
[511] Usami
[512] Uzukamaru Taizo
[513] Uzukumaru
[514] Venus
[515] Vera
[516] Viola
[517] Vortex
[518] Wesley Stickler
[519] Will
[520] William
[521] WillP
[522] Winfred
[523] Winfred Kitaki
[524] Yutaka
[525] Yuujin Mikotoba
[526] Yuujin Mikotoba Suit
[527] Zacharias
[528] Zak
[529] Zinc
[530] Zinc Lablanc
[531] Monopoly-Guy
[532] Peppers
[533] Q
[534] Ranger Justice
[535] Rayfa
[536] Renwick
[537] Scuttlebutt
[538] Snow
[539] Vex
[540] Vex TOTS
[541] Vulper
[542] Warden
[543] Rydia
[544] Titus Kruuump
[545] Woman
[546] SayakaMaizono HD
[547] TokoFukawa HD
[548] YasuhiroHagakure HD
[549] AlterEgo HD
[550] AoiAsahina HD
[551] ByakuyaTogami HD
[552] CelestiaLudenberg HD
[553] ChihiroFujisaki HD
[554] HifumiYamada HD
[555] JunkoEnoshima HD
[556] KiyotakaIshimaru HD
[557] KyokoKirigiri HD
[558] LeonKuwata HD
[559] MakotoNaegi HD
[560] MondoOwada HD
[561] MukuroIkusaba HD
[562] MukuroIkusabaZer0 HD
[563] SakuraOgami HD
[564] SoniaNevermind HD
[565] TeruteruHanamura HD
[566] UltimateImposter HD
[567] AkaneOwari HD
[568] ChiakiNanami HD
[569] FuyuhikoKuzuryu HD
[570] GundhamTanaka HD
[571] HajimeHinata HD
[572] HiyokoSaionji HD
[573] IbukiMioda HD
[574] KazuichiSoda HD
[575] MahiruKoizumi HD
[576] MikanTsumiki HD
[577] NagitoKomaeda HD
[578] NekomaruNidai HD
[579] PekoPekoyama HD
[580] Servant HD
[581] Shirokuma HD
[582] TokoFukawaAE HD
[583] YutaAsahina HD
[584] ByakuyaTogamiAE HD
[585] HaijiTowa HD
[586] JataroKemuri HD
[587] KomaruNaegi HD
[588] KotokoUtsugi HD
[589] Kurokuma HD
[590] MakotoNaegiAE HD
[591] MasaruDaimon HD
[592] MonacaTowa HD
[593] NagisaShingetsu HD
[594] ShuichiSaiharaCapless HD
[595] TenkoChabashira HD
[596] TsumugiShirogane HD
[597] AngieYonaga HD
[598] GontaAlterEgo HD
[599] GontaGokuhara HD
[600] HimikoYumeno HD
[601] K1-B0 HD
[602] KaedeAkamatsu HD
[603] KaitoMomota HD
[604] KirumiTojo HD
[605] KokichiOma HD
[606] KorekiyoShinguji HD
[607] MakiHarukawa HD
[608] MastermindV3 HD
[609] MiuIruma HD
[610] RantaroAmami HD
[611] RyomaHoshi HD
[612] ShuichiSaihara HD
[613] ShuichiSaiharaEx
[614] Monodam
[615] Monokid
[616] Monokubs
[617] Monokuma
[618] Monokuma V3
[619] MonokumaV3
[620] MonokumaV3 1.8
[621] Akane
[622] Angie
[623] Angie Yonaga
[624] Byakuya
[625] Byakuya Twogami
[626] Byakuya2
[627] ByakuyaTogami
[628] Celeste
[629] Celestia Ludenburg
[630] Chiaki
[631] ChihiroFujisaki
[632] Fukawa
[633] Fukawa_DRAE
[634] Fuyuhiko
[635] FuyuhikoKuzuryuu
[636] GenSho
[637] Gonta
[638] Gonta Gokuhara
[639] Gundam
[640] GundhamTanaka
[641] Hagakure
[642] Haiji
[643] HaijiTowa
[644] Hanamura
[645] Hifumi
[646] Hifumi Yamada
[647] Himiko
[648] Himiko Yumeno
[649] Hiroko
[650] Hiroko Hagakure
[651] Hiyoko
[652] Ishimaru
[653] Izuru
[654] Izuru Kamukura
[655] Jataro
[656] Jataro Kemuri
[657] Junko
[658] Junko Enoshima
[659] JunkoDespair
[660] JunkoEnoshima(MI)
[661] JunkoEnoshima(MM)
[662] K1-B0
[663] Kazuichi
[664] Kiibo
[665] Koizumi
[666] Kokichi
[667] Komachi Onozuka
[668] Komaeda
[669] Komaru
[670] KomaruNaegi
[671] Korekiyo
[672] Korekiyo Shinguji
[673] Kotoko
[674] KotokoUtsugi
[675] Kotomine Kirei
[676] Kurokuma
[677] Leon
[678] Leon Kuwata
[679] Mahiru
[680] Maizono
[681] Masaru
[682] Masaru Daimon
[683] Miu
[684] Miu Iruma
[685] Monaca
[686] MonakaTowa
[687] Mondo
[688] Monomi
[689] Monophanie
[690] Monosuke
[691] Monotaro
[692] Mukuro Ikusaba
[693] Naegi
[694] Nagisa
[695] Nagisa Shingetsu
[696] Nagito
[697] NagitoBeta
[698] Nanami
[699] NanamiChiaki
[700] Peko
[701] Rantaro
[702] Rantaro Amami
[703] Ryoko
[704] Ryoma
[705] Ryoma Hoshi
[706] Ryota Mitarai
[707] Sakura
[708] Sakura Oogami
[709] Servant
[710] Shirokuma
[711] Shuichi
[712] Shuichi Saihara
[713] Shuichi Saihara (Hatless)
[714] Shuuichi Saihara
[715] Sonia
[716] SoniaNevermind
[717] Taichi
[718] Tenko
[719] Tenko Chabashira
[720] Teruteru
[721] The Servant
[722] Togami
[723] Tsumugi
[724] Tsumugi Shirogane
[725] Tsumugi Shirogane (MM)
[726] Yasuhiro
[727] Yuta
[728] Yuta Asahina
[729] Nekomaru
[730] Nidai
[731] Saionji
[732] YonedaJun
[733] Anna
[734] Azura
[735] Camilla (FE)
[736] Chrom
[737] Corrin (F)
[738] CorrinMale
[739] FemaleRobin
[740] Gaius
[741] Ike
[742] Lucina
[743] Marth (Fates)
[744] Oboro
[745] Odin Dark
[746] Robin (Fates)
[747] Sissel
[748] Lynne
[749] Missile
[750] KismetCat
[751] Cabanela
[752] Popuri
[753] Mila Evans
[754] Palutena_HD
[755] Pit
[756] Phosphora
[757] Viridi_HD
[758] Dimentio
[759] Paper Mario (Modern)
[760] Ace
[761] Lotus
[762] Santa
[763] Clover
[764] Snake
[765] Snake 999
[766] Ninth Man
[767] NinthMan
[768] Seven
[769] Bisharp
[770] Riolu
[771] Sylveon
[772] Teppo
[773] Gardevoir
[774] Layton
[775] Layton Evil
[776] Layton Inquisitor
[777] Layton Pro
[778] Layton Winter
[779] LaytonInquisitor
[780] LaytonP
[781] Luke
[782] Katrielle Layton
[783] DonPaolo
[784] Alfendi
[785] Descole
[786] Lucy
[787] Lucy Baker
[788] Makepeace
[789] Anton
[790] Chelmey
[791] Claire
[792] Clive
[793] Dimitri
[794] Emmy
[795] Flora
[796] Grosky
[797] Ilyana
[798] Arle
[799] Arle20th
[800] Carbuncle20th
[801] Lemres
[802] SatanPP
[803] Sig25th
[804] Maguro
[805] Phantom R
[806] Jeena
[807] Toon Link
[808] Young Link
[809] Beat
[810] Coco Atarashi
[811] Hanekoma
[812] Neku
[813] Neku Sakuraba_HD
[814] Rhyme
[815] Shiki
[816] Sho
[817] Joshua
[818] Kariya
[819] Reaper
[820] zettaslow
[821] Aoto
[822] Ar Ru
[823] Azrael
[824] Carl
[825] Celica A Mercury
[826] Hades Izanami
[827] Hakumen
[828] Hazama
[829] Hibiki Kohaku
[830] Jubei
[831] Jin
[832] Litchi Faye Ling
[833] Naoto Kurogane
[834] Nine The Phantom
[835] Noel Vermillion
[836] Platinum
[837] Rachel Alucard
[838] Ragna
[839] Relius-Clover
[840] Terumi Hooded
[841] Tsubaki
[842] Tsubaki Yayoi
[843] Yuuki Terumi
[844] MilaMaxwell
[845] Tina
[846] Violet
[847] Winchester
[848] J
[849] CC
[850] Lelouch
[851] Zero (CG)
[852] Archer
[853] Seiko
[854] Yuka
[855] HibikiKosuke
[856] IsshikiKotone
[857] MichibaTakashi
[858] OgiwaraSaori
[859] SagisuReiko
[860] ShiginoHana
[861] Morrigan
[862] L
[863] Shinichi Kudo
[864] Ran Mouri
[865] Conan Edogawa
[866] Juzo Megure
[867] Vergil
[868] Dante
[869] Dante DMC
[870] Etna
[871] Monika
[872] Sayori
[873] Yuri
[874] Natsuki
[875] Heather
[876] Izaya Orihara
[877] Celty
[878] Hanbei Solo
[879] Laby
[880] Gilgamesh
[881] Illya
[882] Alphonse Elric
[883] Edward Elric
[884] Greed
[885] Roy Mustang
[886] Scar
[887] Alisa
[888] Giffany
[889] RoboKy
[890] Birdman
[891] Birdman Leg
[892] Haruhi Def
[893] Andrew Hussie
[894] Arenea Sarket
[895] Cronus ampora
[896] Dave Strider
[897] John egbert
[898] Karkat Vantas
[899] Latula Pyrope
[900] Meenah Peixes
[901] Meulin leijon
[902] Nepeta leijon
[903] Rose Lalonde
[904] Blanc
[905] Cave
[906] Compa
[907] Histoire
[908] IF
[909] Linda
[910] Nepgear
[911] Neptune
[912] Noire
[913] Plutia
[914] RED
[915] Vert
[916] Inferno Cop
[917] Bruno Bucciarati
[918] Dio Brando
[919] Giorno Giovanna
[920] Jotaro Kujo
[921] KiraJ
[922] Kongou
[923] Hanako
[924] Tezuka Rin
[925] Aki Hinata
[926] Angol Mois
[927] Fuyuki Hinata
[928] Momoka Nishizawa
[929] Sora
[930] Xion
[931] Arisa
[932] Eli Ayase
[933] Nico Yazawa
[934] Umi Sonoda
[935] Maria (Mad Father)
[936] Aya_Remaster
[937] Spiderman
[938] Strider Hiryu
[939] Megaman X
[940] Zero
[941] Hippo
[942] Sheshe y Mimi
[943] Zen
[944] Adachi
[945] Aigis
[946] Akihiko Sanada
[947] Akihiko Sanada P3
[948] Chie
[949] Chie Satonaka
[950] Elizabeth
[951] Junpei (Persona)
[952] Junpei Iori
[953] Junpei Iori P3
[954] Ken
[955] Ken Amada
[956] Koromaru
[957] Kanji
[958] Labrys
[959] Margaret
[960] Marie
[961] Mitsuru
[962] MitsuruKirijo
[963] Morgana
[964] Naoto
[965] rise
[966] Shinjiro Aragaki
[967] Sho Minazuki
[968] Shuji Ikutsuki
[969] Vincent Brooks
[970] Yosuke
[971] Yu
[972] Yukiko
[973] Yukiko Amagi
[974] YuNarukami
[975] Bulleta
[976] Captain Commando
[977] Kage Maru
[978] Chris Redfield
[979] ruby rose
[980] weiss
[981] blake belladonna
[982] yangbbtag
[983] neopolitanv2
[984] Shantae
[985] Jinn
[986] Hibiki
[987] Big Band
[988] Squigly
[989] Amadeus
[990] Amane Suzuha
[991] Faris NyanNyan
[992] Faris WarTime
[993] Hashida Itaru
[994] Hiyajo Maho
[995] Makise Kurisu
[996] Mayushii Zero
[997] Kiryu Moeka
[998] Rukako
[999] Tennouji Nae
[1000] Tennouji Yuugo
[1001] Cliff (SoS)
[1002] Ryu
[1003] ColetteBrunel
[1004] Dezel
[1005] AsbelLhant
[1006] Dist
[1007] Edna
[1008] Eizen
[1009] Alisha Diphda
[1010] GuyCecil
[1011] JadeCurtiss
[1012] JuliusWillKresnik
[1013] Lailah
[1014] LloydIrving
[1015] Magilou
[1016] Raven
[1017] Rokurou
[1018] Rose
[1019] Sorey
[1020] Velvet
[1021] Velvet Crowe
[1022] Zaveid
[1023] Kazuya Mishima
[1024] Lorne
[1025] LorneDef
[1026] Heidern
[1027] Lali Tigante
[1028] Alice Margatroid
[1029] Alice Margatroid (Kid)
[1030] Yukari Yakumo
[1031] Yukari Yakumo (SWR)
[1032] Alice
[1033] Aya (FS)
[1034] Aya Shameimaru
[1035] Aya Shameimaru (SWR)
[1036] Byakuren
[1037] Cirno
[1038] Cirno SWR
[1039] Clownpiece
[1040] Eiki Shiki
[1041] Eirin
[1042] Fujiwara no Mokou
[1043] Hong Meiling
[1044] Hong Meiling (GT)
[1045] Iku Nagae
[1046] Marisa IAMP
[1047] Marisa Kirisame
[1048] Marisa Kirisame (Touhou HS)
[1049] Kagerou
[1050] Kaguya Houraisan
[1051] Koakuma Kid
[1052] Kutaka Niwatari
[1053] Meiling
[1054] Meira
[1055] Mima
[1056] Patchouli
[1057] Reimu Hakurei
[1058] Reisen
[1059] Reisen Udongein Inaba
[1060] Remilia Scarlet
[1061] Rumia
[1062] Sakuya IAMP
[1063] Sakuya Izayoi
[1064] Sanae Kochiya
[1065] Satori Komeiji
[1066] Sekibanki (SWR)
[1067] Tenshi Hinanawi
[1068] Tenshi SWR
[1069] Youmu Konpaku
[1070] Youmu Konpaku (SWR)
[1071] Shion
[1072] Suwako Moriya
[1073] Tewi Inaba
[1074] Urumi Ushizaki
[1075] Yuuka Kazami
[1076] Yuyuko Saigyouji
[1077] Gordeau
[1078] Linne
[1079] Orie
[1080] Seth
[1081] Yuzuriha
[1082] Amakusa
[1083] Battler Ushiromiya
[1084] Beatrice
[1085] Bernkastel
[1086] Erika
[1087] Majima
[1088] Reko
[1089] Safalin
[1090] Sara
[1091] Sou
[1092] Alice
[1093] Gashu
[1094] Gin
[1095] Joe
[1096] Kai
[1097] Kanna
[1098] Keiji
[1099] Miley
[1100] Mishima
[1101] Nao
[1102] QTaro
[1103] Ranger
[1104] Archibald
[1105] Chris McLean (TD)
[1106] CodeWeaver (D)
[1107] Conway Stern
[1108] Discord
[1109] El Gato
[1110] Moeziska
[1111] SANESS
[1112] Kike Morande
[1113] Noedig
[1114] Noedig W
[1115] Tee
[1116] The King
[1117] The King v2
[1118] TheKing
[1119] The Noid
[1120] Vegeta
[1121] Liza
[1122] Akihiro Bakuhatsu
[1123] Angela (P)
[1124] taokaka v2
[1125] lucario
[1126] nero claudius fgo
[1127] pandemonica (ht)_fv
[1128] beelzebub (ht)_fv
[1129] lucifer (ht)_fv
[1130] hawk
[1131] niko (oneshot)
[1132] rem
[1133] ram
[1134] gilgamesh hd
[1135] alice
[1136] TifaLockhart_(FFWOTV)
[1137] tricky (fnf)
[1138] artoria (caster) fgo
[1139] artoria pendragon (alter)
[1140] shantae (sevensirens)
[1141] shantae
[1142] astolfo_fv
[1143] beatrice
[1144] phi
[1145] sigma
[1146] quark
[1147] dio
[1148] arcueidbrunestud (meltyblood)
[1149] enhanced courtney
[1150] Taokaka_V2
[1151] Lucario
[1152] Nero Claudius (FGO)
[1153] Pandemonica (HT)_fv
[1154] Beelzebub (HT)_fv
[1155] Lucifer (HT)fv
[1156] Hawk (wit)
[1157] nikooneshot
[1158] Rem
[1159] Ram
[1160] Gilgamesh HD
[1161] Alice
[1162] TifaLockhart_(FFWOTV)
[1163] Tricky (FNF)
[1164] Artoria (Alter)
[1165] Artoria Pendragon FSN
[1166] Shantae (Silvervisions)
[1167] Shantae
[1168] Nobu
[1169] Astolfo_fv
[1170] Beatrice
[1171] Phi
[1172] Sigma
[1173] Quark
[1174] Dio
[1175] Arcueid Brunestud (Tsukihime)
[1176] Enhanced Courtney
[1177] AAI Ema
[1178] stocking anarchy (psg)
[1179] Rin Tohsaka
[1180] Kid Miles
[1181] Artoria (Caster)
[1182] Artoria (Ruler)
[1183] Jeanne D'arc
[1184] Jeanne D'arc Alter
[1185] Labrys
[1186] Labrys (Story)
[1187] Aigis (Godot)
[1188] Kokonoe
[1189] Loremaster (HT) 
'''
