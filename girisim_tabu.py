import discord
from discord import mentions
from discord import team
from discord import colour
from discord.embeds import Embed
from discord.ext import commands
from discord.utils import get
from discord.ext.commands.bot import when_mentioned
from random import choice
import asyncio
from os import chdir

chdir("C:\\Users\\LENOVO\\Desktop\\Python\\Discord\\ITU_GIRISIM\\girisim_tabu")
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix="-t ", intents=intents, help_command=None)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="-t yardim"))
    print(f"{client.user.name} ÇALIŞIYOR")

puanlar = [["pas", 0], ["skor_t1", 0], ["skor_t2", 0]]
#team1 = [] #kişi sayısı tekse 1 kişi fazla-6
#team2 = [] #kişi sayısı tekse 1 kişi az-5

@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    else:
        try:
            #karşı takımdan birisi team1e bakmalı.
            if user == anlatıcı and user in team1:
                if reaction.emoji == "🟩":

                    puanlar[1][1] += 1
                    await tabu_yolla(t_emb, 1)

                    await reaction.remove(user)
                    
                elif reaction.emoji == "🟥":

                    puanlar[1][1] -= 1
                    await tabu_yolla(t_emb, 1)

                    await reaction.remove(user)
                    
                elif reaction.emoji == "🟨":
                    if puanlar[0][1] > 0:

                        puanlar[0][1] -= 1
                        await tabu_yolla(t_emb, 1)

                        await reaction.remove(user)

                    else:
                        await reaction.remove(user)

            elif user in team2 and anlatıcı == user:
                if reaction.emoji == "🟩":

                    puanlar[2][1] += 1
                    await tabu_yolla(t_emb, 2)

                    await reaction.remove(user)
                
                elif reaction.emoji == "🟥":

                    puanlar[2][1] -= 1
                    await tabu_yolla(t_emb, 2)

                    await reaction.remove(user)

                elif reaction.emoji == "🟨":
                    if puanlar[0][1] > 0:
                        puanlar[0][1] -= 1
                        await tabu_yolla(t_emb, 2)

                        await reaction.remove(user)

                    else:
                        await reaction.remove(user)

        except:
            pass


@client.command(aliases=['yardım', 'help'])
async def yardim(ctx):
    y_emb = discord.Embed(tittle="Yardım", colour=discord.Colour(0x00fff1))
    y_emb.set_thumbnail(url=client.user.avatar_url )
    y_emb.add_field(name="tabu", value="Oyunu başlatmak için kullanılır\n*Örnek Kullanım:* .t tabu @Tolga @Cemre @Zeynep @Ali", inline=False)
    y_emb.add_field(name="çiçek", value="Çiçekler takımının anlatma sırası geldiğinde ve hazır hissettiklerinde komutu kullanarak oyunu başlatırlar.\n*Örnek Kullanım:* .t çiçek 3(pas hakkınızı belirleyin)\nKomut kullanıldığında anlatıcı ve karşı takımın görebileceği bir kanal açılır.", inline=False)
    y_emb.add_field(name="sböcek", value="Sümüklü böcekler takımının anlatma sırası geldiğinde ve hazır hissettiklerinde komutu kullanarak oyunu başlatırlar.\n*Örnek Kullanım:* .t sböcek 3(pas hakkınızı belirleyin)\nKomut kullanıldığında anlatıcı ve karşı takımın görebileceği bir kanal açılır.", inline=False)
    await ctx.send(embed=y_emb)

    #await ctx.send(file=discord.File("guard1.png"))
    #await ctx.send(file=discord.File("guard2.png"))

kelimeler_Sozlugu = {}

kelime_Bank = open("tabu.txt", "r", encoding="utf-8")

for i in kelime_Bank.readlines():
    i = i[:len(i)-1]
    tabu = i.split(": ")

    kelime, tabu = tabu[0], tabu[1]

    tabular = tabu.split("-")

    kelimeler_Sozlugu.setdefault(kelime, tabular)


@client.command()
async def tabu(ctx, *member:discord.Member):
    global skor_t1, skor_t2, team1, team2, team1_c, team2_c, t1_role, t2_role
    team1 = []
    team2 = []
    team1_c = []
    team2_c = []
    takım_kurma = list(member).copy() 

    try:    
        t1_role = discord.utils.get(ctx.guild.roles, name='Çiçekler')
    except:
        pass

    try:    
        t2_role = discord.utils.get(ctx.guild.roles, name='Sümüklü Böcekler')
    except:
        pass

    if t1_role is not None:
        pass
    else:
        await ctx.guild.create_role(name="Çiçekler", colour=discord.Colour(0x8e01a8))
        t1_role = discord.utils.get(ctx.guild.roles, name='Çiçekler')
    
    if t2_role is not None:
        pass
    else:
        await ctx.guild.create_role(name="Sümüklü Böcekler", colour=discord.Colour(0x962bad))
        t2_role = discord.utils.get(ctx.guild.roles, name='Sümüklü Böcekler')
    
    #TAKIMLARI KURDUK
    if len(member)%2 == 0:

        for i in range(0, int(len(member)/2)):
            uye1 = choice(takım_kurma)

            team1.append(uye1)
            team1_c.append(uye1)

            takım_kurma.remove(uye1)

            await uye1.add_roles(t1_role)

            uye2 = choice(takım_kurma)

            team2.append(uye2)
            team2_c.append(uye2)

            takım_kurma.remove(uye2)

            await uye2.add_roles(t2_role)
        
    elif len(member)%2 == 1:

        try:
            for i in range(0, int((len(member)+1)/2)):
                uye = choice(takım_kurma)

                team1.append(uye)
                team1_c.append(uye)

                takım_kurma.remove(uye)

                await uye.add_roles(t1_role)

            for i in range(0, int((len(member)-1)/2)):
                uye = choice(takım_kurma)

                team2.append(uye)
                team2.append(uye)

                takım_kurma.remove(uye)

                await uye.add_roles(t2_role)
        except:
            pass
    #EMBED MESAJI GÖNDERİCEZ TAKIMLAR BU BU DİYE
    teams = discord.Embed(tittle="TAKIMLAR", colour=discord.Colour.gold())

    t1 = " "
    t2 = " "
    for player in team1:  #TAKIMLARI TEK STRİNGDE YAZDIK

        if player.nick != None:
            t1 += f"* {player.nick}\n"
        else:
            t1 += f"* {player.name}\n"
    for player in team2:

        if player.nick != None:
            t2 += f"* {player.nick}\n"
        else:
            t2 += f"* {player.name}\n"
    
    teams.add_field(name="Çiçekler", value=t1, inline=True)
    teams.add_field(name="Sümüklü Böcekler", value=t2, inline=True)

    await ctx.send(embed=teams)



@client.command(aliases=["cicek"])
async def çiçek(ctx):
    global team1_c, t_emb, anlatıcı, puanlar

    puanlar[0][1] = 3

    if len(team1_c) == 0:
        team1_c = team1.copy() 
    
    anlatıcı = choice(team1_c)

    team1_c.remove(anlatıcı)
    
    if anlatıcı.nick:
        anlatıcı_n = anlatıcı.nick
    else:
        anlatıcı_n = anlatıcı.name

    await ctx.send(f"Çiçekler toplansın. Anlatma sırası ***{anlatıcı_n}*** 'da .")

    channelTabu = discord.utils.get(ctx.guild.channels, name='│çiçekler')
    if channelTabu is not None:
        await channelTabu.delete()
    
    overwritesz = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        t1_role: discord.PermissionOverwrite(read_messages=False),
        t2_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
        anlatıcı: discord.PermissionOverwrite(read_messages=True)
        }
    channelTabu = await ctx.guild.create_text_channel(name='│çiçekler', overwrites=overwritesz)
    
    #İLK KELİME EMBEDİ
    tabu_embed = discord.Embed(tittle="Tabu", description=f"Puan: {puanlar[1][1]} , PasHakkı: {puanlar[0][1]}")

    ana_kelimeler_list = list(kelimeler_Sozlugu.keys())

    ana_kelime = choice(ana_kelimeler_list)
    tabu_list = kelimeler_Sozlugu[ana_kelime]

    del kelimeler_Sozlugu[ana_kelime]
    
    tabu_str = " "
    c = 1
    for t in tabu_list:
        tabu_str += f"**{c}. YASAK:** ----> {t.title()}\n"
        c += 1

    ana_kelime = ana_kelime.upper()

    ana_kelime.replace("I", "İ")

    tabu_embed.add_field(name=f"---------> *{ana_kelime}* <---------", value=tabu_str)

    t_emb = await channelTabu.send(embed=tabu_embed, delete_after=120)


    await t_emb.add_reaction("🟩")
    await t_emb.add_reaction("🟥")
    await t_emb.add_reaction("🟨")

    sn = 120

    kac_sn_kaldi = discord.Embed(description=f"**{sn}** saniye kaldı.")
    gitti_sn = await channelTabu.send(embed=kac_sn_kaldi)

    for min in range(1,120,10):
        await asyncio.sleep(10)
        
        sn -= 10

        new_gitti = discord.Embed(description=f"**{sn}** saniye kaldı.")
        await gitti_sn.edit(embed=new_gitti)


    emb = discord.Embed(tittle="Skor")
    emb.add_field(name=f"Tebrikler **{anlatıcı_n}**", value=f"Takımınızın Skoru: ***{puanlar[1][1]}***")
    await ctx.send(embed=emb)



@client.command(aliases=["sümüklüböcek", "sbocek", "sb", "sumuklubocek"])
async def sböcek(ctx):
    global team2_c, t_emb, anlatıcı, puanlar

    puanlar[0][1] = 3

    if len(team2_c) == 0:
        team2_c = team2.copy() 
    
    anlatıcı = choice(team2_c)

    team2_c.remove(anlatıcı)
    
    if anlatıcı.nick:
        anlatıcı_n = anlatıcı.nick
    else:
        anlatıcı_n = anlatıcı.name
    
    await ctx.send(f"Sümüklü Böcekler toplansın. Anlatma sırası ***{anlatıcı_n}*** 'da .")
    
    channelTabu = discord.utils.get(ctx.guild.channels, name='│sümüklü-böcekler')
    
    if channelTabu is not None:
        await channelTabu.delete()

    overwritesz = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        t1_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        t2_role: discord.PermissionOverwrite(read_messages=False),
        anlatıcı: discord.PermissionOverwrite(read_messages=True)
        }
    channelTabu = await ctx.guild.create_text_channel(name='│sümüklü-böcekler', overwrites=overwritesz)

    #İLK KELİME EMBEDİ
    tabu_embed = discord.Embed(tittle="Tabu", description=f"Puan: {puanlar[2][1]} , PasHakkı: {puanlar[0][1]}")

    ana_kelimeler_list = list(kelimeler_Sozlugu.keys())

    ana_kelime = choice(ana_kelimeler_list)
    tabu_list = kelimeler_Sozlugu[ana_kelime]

    del kelimeler_Sozlugu[ana_kelime]
    
    tabu_str = " "
    c = 1
    for t in tabu_list:
        tabu_str += f"**{c}. YASAK:** ----> {t.title()}\n"
        c += 1

    ana_kelime = ana_kelime.upper()

    ana_kelime.replace("I", "İ")

    tabu_embed.add_field(name=f"---------> *{ana_kelime}* <---------", value=tabu_str)

    t_emb = await channelTabu.send(embed=tabu_embed, delete_after=120)


    await t_emb.add_reaction("🟩")
    await t_emb.add_reaction("🟥")
    await t_emb.add_reaction("🟨")

    sn = 120

    kac_sn_kaldi = discord.Embed(description=f"**{sn}** saniye kaldı.")
    gitti_sn = await channelTabu.send(embed=kac_sn_kaldi)


    for min in range(1,120,10):
        await asyncio.sleep(10)
        
        sn -= 10

        new_gitti = discord.Embed(description=f"**{sn}** saniye kaldı.")
        await gitti_sn.edit(embed=new_gitti)

    emb = discord.Embed(tittle="Skor")
    emb.add_field(name=f"Tebrikler **{anlatıcı_n}**", value=f"Takımınızın Skoru: ***{puanlar[2][1]}***")
    await ctx.send(embed=emb)



async def tabu_yolla(editli_emb, takım=int):
    ana_kelimeler_list = list(kelimeler_Sozlugu.keys())

    ana_kelime = choice(ana_kelimeler_list)
    tabu_list = kelimeler_Sozlugu[ana_kelime]

    del kelimeler_Sozlugu[ana_kelime]
    
    tabu_str = " "
    c = 1
    for t in tabu_list:
        tabu_str += f"**{c}. YASAK:** ----> {t.title()}\n"
        c += 1

    ana_kelime = ana_kelime.upper()

    ana_kelime.replace("I", "İ")

    new_em = discord.Embed(tittle="Tabu", description=f"Puan: {puanlar[takım][1]} , PasHakkı: {puanlar[0][1]}")

    new_em.add_field(name=f"---------> *{ana_kelime}* <---------", value=tabu_str)

    t_emb = await editli_emb.edit(embed=new_em)


    return t_emb

@client.command(aliases=["sifirla", "zero", "z"])
async def sıfırla(ctx):
    global puanlar, team1, team2, team1_c, team2_c, takım_kurma

    puanlar = [["pas", 0], ["skor_t1", 0], ["skor_t2", 0]]
    team1, team2 = [], []
    team1_c, team2_c = [], []
    takım_kurma = []

    t1_role = discord.utils.get(ctx.guild.roles, name='Çiçekler')
    t2_role = discord.utils.get(ctx.guild.roles, name='Sümüklü Böcekler')

    try:
        channelCic = discord.utils.get(ctx.guild.channels, name="│çiçekler")
        channelSB = discord.utils.get(ctx.guild.channels, name="│sümüklü-böcekler")

        if channelCic:
            await channelCic.delete()
        if channelSB:
            await channelSB.delete()

    except:
        pass

    for memb in team1:
        await memb.remove_roles(t1_role)

    for memb in team2:
        await memb.remove_roles(t2_role)


    emb = discord.Embed(tittle="sıfırla",
    description="Veriler sıfırlandı ..")
    await ctx.send(embed=emb)

client.run("ODQ1MDMwMTI3Mjc1MzQzODcy.YKbBog.ogXIfdk9gEGpgWAr_zdfXIIDRrM")


