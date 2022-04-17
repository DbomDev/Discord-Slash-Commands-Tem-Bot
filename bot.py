import os
import asyncio
from pathlib import Path
import json
from math import radians
import random
import wikipedia
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext.commands import MissingPermissions, has_permissions
from discord_components import Button, ButtonStyle, Select, SelectOption, interaction, InteractionEventType, Interaction
import platform
import sys
import traceback
import re
import lavalink
from discord import utils

import cogs._json

print("\n---------\n")

intents = discord.Intents.all()
client = discord.Client(intents=intents)
slash = SlashCommand(client, sync_commands=True)

#Lists

guild_ids = []

client.version = 1.0
lastupdate = """```v1.0: Fully New
The Bot has now slashcommands!
```"""

colors_list = {
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_NAVY': 0x2C3E50
}

option_types={
    "SUB_COMMAND":1,
    "SUB_COMMAND_GROUP":2,
    "STRING":3,
    "INTEGER":4,
    "BOOLEAN":5,
    "USER":6,
    "CHANEL":7,
    "ROLE":8
}

#Events
async def all_guilds_func():
    for guild in client.guilds:
        id = guild.id
        guild_ids.append(id)

@client.event
async def on_ready():
    await all_guilds_func()
    print(f"ALl Guild Id's\n{guild_ids}")

    print("\n---------\n")
    print(f"Logged in as {client.user}")
    print("\n---------\n")

sniped_message = None
sniped_author = None

@client.event
async def on_message_delete(message):
    global sniped_message
    global sniped_author
    sniped_message = message.content
    sniped_author = message.author.id

old_edit = None
new_edit = None
author_edit = None

@client.event
async def on_message_edit(before, after):
    global old_edit
    global new_edit
    global author_edit
    old_edit = before.content
    new_edit = after.content
    author_edit = after.author.id
    
time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time

#general embeds
help_embed = discord.Embed(
    title="Help",
    description="Use /help to get help options",
    color=colors_list['GOLD']
).set_thumbnail(url="https://www.bing.com/images/search?view=detailV2&ccid=PVXL5Gz4&id=A80ADB46F7609340A463715133A093C45616CA48&thid=OIP.PVXL5Gz4v4QHR3b3xZA78wHaHa&mediaurl=https%3a%2f%2ffiverr-res.cloudinary.com%2fimages%2ft_main1%2cq_auto%2cf_auto%2fgigs%2f115316237%2foriginal%2f64f78862282815a5853efb158c43201f068d74bc%2fmake-you-a-professional-discord-server.png&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.3d55cbe46cf8bf84074776f7c5903bf3%3frik%3dSMoWVsSToDNRcQ%26pid%3dImgRaw%26r%3d0&exph=680&expw=680&q=discord+standard+bot+icon&simid=607998796144249889&FORM=IRPRST&ck=F3BAE42585B0F69D7A9525EA06B97A49&selectedIndex=0")
help_embed.add_field(name="**Moderation**", value="Discord Server Moderation commands", inline=True)
help_embed.add_field(name="**Channels**", value="Server Channel commands", inline=True)
help_embed.add_field(name="**Fun**", value="Fun/Game commands", inline=True)
help_embed.add_field(name="**Music**", value="Music Server commands", inline=True)
help_embed.add_field(name="**Messages**", value="Server Message Commands", inline=True)
help_embed.add_field(name="**Users**", value="Discord about Users commands", inline=True)
help_embed.add_field(name="**Website API's**", value="Website API Commands", inline=True)
help_embed.add_field(name="**Omega**", value="The Bots special commands", inline=True)
help_embed.set_thumbnail(url="https://www.bing.com/images/search?view=detailV2&ccid=PVXL5Gz4&id=A80ADB46F7609340A463715133A093C45616CA48&thid=OIP.PVXL5Gz4v4QHR3b3xZA78wHaHa&mediaurl=https%3a%2f%2ffiverr-res.cloudinary.com%2fimages%2ft_main1%2cq_auto%2cf_auto%2fgigs%2f115316237%2foriginal%2f64f78862282815a5853efb158c43201f068d74bc%2fmake-you-a-professional-discord-server.png&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.3d55cbe46cf8bf84074776f7c5903bf3%3frik%3dSMoWVsSToDNRcQ%26pid%3dImgRaw%26r%3d0&exph=680&expw=680&q=discord+standard+bot+icon&simid=607998796144249889&FORM=IRPRST&ck=F3BAE42585B0F69D7A9525EA06B97A49&selectedIndex=0")
help_embed.set_footer(text="Testing v1 Bot", icon_url="https://www.bing.com/images/search?view=detailV2&ccid=PVXL5Gz4&id=A80ADB46F7609340A463715133A093C45616CA48&thid=OIP.PVXL5Gz4v4QHR3b3xZA78wHaHa&mediaurl=https%3a%2f%2ffiverr-res.cloudinary.com%2fimages%2ft_main1%2cq_auto%2cf_auto%2fgigs%2f115316237%2foriginal%2f64f78862282815a5853efb158c43201f068d74bc%2fmake-you-a-professional-discord-server.png&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.3d55cbe46cf8bf84074776f7c5903bf3%3frik%3dSMoWVsSToDNRcQ%26pid%3dImgRaw%26r%3d0&exph=680&expw=680&q=discord+standard+bot+icon&simid=607998796144249889&FORM=IRPRST&ck=F3BAE42585B0F69D7A9525EA06B97A49&selectedIndex=0")

@slash.slash(name="help",description="Sends Embed with all Help categories",guild_ids=guild_ids, options=[])
async def _help(ctx):
    await ctx.send(
        embed=help_embed, 
        components = None #[Button(label="Developer", style=ButtonStyle.url,custom_id="url1", url="https://dbomdev.github.io")]
    )

@slash.slash(name="all_commands", description="shows alll avaible commands", guild_ids=guild_ids)
async def _all_commands(ctx):
    cmds1 = """
```
/kick
/ban
/unban
/mute
/unmute
/purge
/snipe
/esnipe
/userinfo
/avatar
/stats
/ping
```"""
    embed_chanel = discord.Embed(
        title="All Commands",
        description="Use /help to see all categorys of commands.",
        color=colors_list["GOLD"]
    ).add_field(name="**Commands**", value=cmds1)
    await ctx.send(embed=embed_chanel)

@slash.slash(name="help_channels", description="Help to channel commands", guild_ids=guild_ids)
async def _help_channels(ctx):
    cmds1 = """
```

```"""
    embed_chanel = discord.Embed(
        title="Help Channel Commands",
        description="Use /help for Help Commands Categorys",
        color=colors_list["GOLD"]
    ).add_field(name="**Commands**", value=cmds1)
    await ctx.send(embed=embed_chanel)


# Moderation Commands
@slash.slash(name="kick", description="Kick a Member of the Server", guild_ids=guild_ids,
    options = [
        create_option(name="member", description="choose member to kick", option_type=option_types["USER"], required=True),
        create_option(name="reason", description="optional reason", option_type=option_types["STRING"], required=False)
    ]
)
@commands.has_guild_permissions(kick_members=True)
@commands.bot_has_guild_permissions(kick_members=True)
async def _kick(ctx, member: discord.Member, *, reason: str):
    error_kick=discord.Embed(
        title="Error",
        description="You can't kick yourself!",
        color=colors_list["RED"]
    )
    error_kick2=discord.Embed(
        title="Error",
        description="You can't kick that user. The User has higher permissions",
        color=colors_list["RED"]
    )
    if member.id == ctx.author.id:
        await ctx.send("You can't kick yourself!")
    elif member.top_role > ctx.author.top_role:
        await ctx.send("Member has an higher rank and can't be kicked by you!")
    else:
        await ctx.guild.kick(user=member, reason=reason)

        embed = discord.Embed(title=f"{ctx.author.name} kicked: {member.name}", description=reason, colour=0xE74C3C)
        await ctx.send(embed=embed)

@slash.slash(name="ban", description="ban a Member of the Server", guild_ids=guild_ids,
    options = [
        create_option(name="member", description="choose member to ban", option_type=option_types["USER"], required=True),
        create_option(name="reason", description="optional reason", option_type=option_types["STRING"], required=False)
    ]
)
@commands.has_guild_permissions(kick_members=True)
@commands.bot_has_guild_permissions(kick_members=True)
async def _ban(ctx, member: discord.Member, *, reason: str):
    
    error_kick=discord.Embed(
        title="Error",
        description="You can't ban yourself!",
        color=colors_list["RED"]
    )
    error_kick2=discord.Embed(
        title="Error",
        description="You can't ban that user. The User has higher permissions",
        color=colors_list["RED"]
    )

    
    if member.id == ctx.author.id:
        await ctx.send(embed=error_kick)
    elif member.top_role > ctx.author.top_role:
        await ctx.send(embed=error_kick2)
    else:
        await ctx.guild.ban(user=member, reason=reason)

        embed = discord.Embed(title=f"{ctx.author.name} banned: {member.name}", description=reason, colour=0xE74C3C)
        await ctx.send(embed=embed)


@slash.slash(name="unban", description="unban someone from the server", guild_ids=guild_ids,
    options = [
        create_option(name="user", description="choose userID to ban", option_type=option_types["USER"], required=True)
    ]
)
@commands.guild_only()
@commands.has_guild_permissions(kick_members=True)
@commands.bot_has_guild_permissions(kick_members=True)
async def _unban(ctx, user: int):
    member = await client.fetch_user(int(user))
    await ctx.guild.unban(user=member)

    embed = discord.Embed(title=f"{ctx.author.name} unbanned: {member.name}",  colour=0x2ECC71)
    await ctx.send(embed=embed)
    
@slash.slash(name="mute", description="Mute an user", guild_ids=guild_ids,
    options=[
        create_option(name="member", description="Choose Member to mute", option_type=option_types["USER"], required=True),
        #create_option(name="time", description="lengh of mute. example 1 d/h/s", option_type=option_types["STRING"], required=False)
    ]
)
@commands.guild_only()
@commands.has_permissions(manage_roles=True)
async def _mute(ctx, member:discord.Member): # , *, time:TimeConverter = None
    role = discord.utils.get(ctx.guild.roles, name="Muted")

    embed2 = discord.Embed(
        title=f"**Muted {member.display_name}**", #for {time}
        color=0x2ECC71
    ).set_footer(text="Wait until a Moderator unmutes you!")


    await member.add_roles(role)
    await ctx.send(embed=embed2)
    #if time:
        #await asyncio.sleep(time)
        #await member.remove_roles(role)

@slash.slash(name="unmute", description="Unmute an user", guild_ids=guild_ids,
    options=[
        create_option(name="member", description="Choose Member to unmute", option_type=option_types["USER"], required=True),
    ]
)
@commands.guild_only()
@commands.has_permissions(manage_roles=True)
async def _unmute(ctx, member:discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")

    embed2 = discord.Embed(
        title=f"**Unmuted {member.display_name}**",
        color=0x2ECC71
    ).set_footer(text="User has been unmuted by an Moderator!")


    await member.remove_roles(role)
    await ctx.send(embed=embed2)
    #You really should use an external error handler- like the one here: https://gist.github.com/Vexs/daa1dcc92ff80fad7ca020d0f7bb4f75
    
@_mute.error
async def mute_error(self, ctx, error):
    if isinstance(error, commands.CheckFailure):
        pass
    if isinstance(error, commands.BadArgument):
        await ctx.send(error)
    else:
        error = getattr(error, 'original', error)
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

# Channel Commands
@slash.slash(name="purge", description="Delete Messages in the channel", guild_ids=guild_ids, options=[create_option(name="amout", description="How many messages to purge", option_type=4, required=True)])
@commands.guild_only()
@commands.has_guild_permissions(manage_messages=True)
@commands.bot_has_guild_permissions(manage_messages=True)
async def _purge(ctx, amout: int):
    await ctx.channel.purge(limit=amout+1)

    await ctx.send(f"**Purged** {amout} **messages**")

# Message Commands
@slash.slash(name="snipe",description="snipe deleted messages",guild_ids=guild_ids)
async def _snipe(ctx):
    sniped_Embed = discord.Embed(
        title="Sniped delete Message",
        description="",
        color=colors_list["GOLD"]
    ).add_field(name="**By User**", value = f"<@{sniped_author}>", inline=False)
    sniped_Embed.add_field(name="**Message**", value = sniped_message, inline=False)

    if sniped_message is None:
        await ctx.send("There is no delete message currently")
    else:
        await ctx.send(embed=sniped_Embed)



@slash.slash(name="esnipe",description="snipe edited messages",guild_ids=guild_ids)
async def _esnipe(ctx):
    esniped_Embed = discord.Embed(
        title="Sniped edited Message",
        description="",
        color=colors_list["GOLD"]
    ).add_field(name="**By User**", value = f"<@{sniped_author}>", inline=False)
    esniped_Embed.add_field(name="**Message Before**", value = old_edit, inline=False)
    esniped_Embed.add_field(name="**Message After**", value = new_edit, inline=False)

    if sniped_message is None:
        await ctx.send("There is no delete message currently")
    else:
        await ctx.send(embed=esniped_Embed)



#User Commands
@slash.slash(name="userinfo", description="Get all Info's about an user", guild_ids=guild_ids,
    options=[
        create_option(name="user", description="CHoose the User of who you want have infos", option_type=option_types["USER"], required=True)
    ]
)
async def _userinfo(ctx, user: discord.Member=None):
    roles = []
    if user==None:
        user = ctx.author

    for role in user.roles:
        roles.append(str(role.mention))

    roles.reverse()

    embed1001 = discord.Embed(
        title=f"{user.mention}'s User Info",
        description="",
        color=colors_list["GOLD"]
    ).add_field(name="Username",value=user.name, inline=False)
    embed1001.add_field(name="Discriminator", value=f"`{user.discriminator}`", inline=False)
    embed1001.add_field(name="ID", value=f"`{user.id}`", inline=False)
    embed1001.add_field(name="Current Activity", value=f"`{user.activity}`", inline=False)
    embed1001.add_field(name="Created At", value=f"`{user.created_at}`", inline=False)
    embed1001.add_field(name="Joined at", value=f"`{user.joined_at}`", inline=False)
    if len(str(" | ".join([x.mention for x in user.roles]))) > 1024:
        embed1001.add_field(name=f"Roles [{len(user.roles)}]", value="Too many to display.", inline=False)
    else:
        embed1001.add_field(name=f"Roles [{len(user.roles)}]", value=" | ".join(roles), inline=False)
    embed1001.add_field(name="Role Color", value=user.color, inline=False)
    embed1001.set_thumbnail(url=user.avatar_url)

    await ctx.send(embed=embed1001)

@slash.slash(name="avatar", description="Get someones Discord profile image",guild_ids=guild_ids)
async def _avatar(ctx, *,  member : discord.Member=None):
    membed1 = member

    embed1 = discord.Embed(
        title="Avatar",
        description="",
        color=0xF1C40F
    ).set_image(url=membed1.avatar_url)

    await ctx.send(embed=embed1)


# Bot Stat Commands
@slash.slash(name="ping", description="This sends the response time of the Bot",guild_ids=guild_ids)
async def _ping(ctx): 
    await ctx.send(f"Pong! {client.latency*1000}ms")


@slash.slash(name="omega", description="Bot Statistics", guild_ids=guild_ids)
async def _stats(ctx):
    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(client.guilds)
    memberCount = len(set(client.get_all_members()))
    embed = discord.Embed(title=f'{client.user.name} Stats', description='\uFEFF', colour=colors_list["GOLD"], timestamp=datetime.utcnow())
    embed.add_field(name='Bot Version:', value=f"```{client.version}```",inline=True)
    embed.add_field(name='Python Version:', value=f"```{pythonVersion}```",inline=True)
    embed.add_field(name='Discord.Py Version', value=f"```{dpyVersion}```",inline=True)
    embed.add_field(name='Servers:', value=f"```{serverCount}```",inline=True)
    embed.add_field(name='Users:', value=f"```{memberCount}```",inline=True)
    embed.add_field(name='Developers:', value="<@655443924948877323>", inline=False)
    embed.add_field(name="**Last Update**", value=lastupdate, inline=False)
    embed.set_footer(text=f"Carpe Noctem | {client.user.name}")
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    await ctx.send(embed=embed)

client.run("bot_token")
