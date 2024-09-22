import discord
from discord import app_commands
import datetime
from discord.ext.commands import has_permissions
import asyncio
import discord.ext
import discord.ext.commands
from discord.utils import get
import time
import os

bot_token = "MTI4NzI0NTIzMjAzOTI2NDI5Nw.GjEO6s.5IR9v3oY0rBEYLqd7rhF4cwgXxb_V-DMlrqT5E"
invite = "discord.com/oauth2/authorize?client_id=1287245232039264297&permissions=8&scope=bot"
welcome_channel = 1221903209094844417
server_id = 1221903208352448563
rule_id = 1221903295682187265
member_count_id = 1229932518422085662



intents = discord.Intents.all() #Setting up intents
intents.message_content = True
client = discord.Client(intents=intents) #Creating bot
tree = app_commands.CommandTree(client) #Creating Slash Commands


import json

def get_server_data():
    with open(os.getcwd() + 'save_data.json') as json_file:
        return json.load(json_file)

def save_server_data(data):
    with open(os.getcwd() + 'save_data.json', 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)




#PING


@tree.command(
    name="ping",
    description="Returns the ping of the bot",
    guild=discord.Object(id=server_id)
)
async def ping(interaction):
    await interaction.response.send_message(f"My ping is {round(client.latency)} ms!")

#READY
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))
    print(f'We have logged in as {client.user}')
    



#APPLY CLASSES

async def msgs_to_str(messages: list[discord.Message], reverse_order = True, include_refer = True, line_spacing = True):
    txt_list = [] # wait for print list
    for message in messages:
        msg_string = ""
        # check and fill in refered message
        ref = message.reference
        user = client.get_user(741400228539793470)
        channel = await user.create_dm()
        if len(message.attachments) > 0:
            for i in message.attachments:
                await channel.send(content=i)
        if ref:
            refer_msg = await message.channel.fetch_message(ref.message_id) if include_refer else None
            refer_tag = "  ↱ "
            refer_present = f"{refer_tag}{refer_msg.author.display_name}: " + refer_msg.content.replace('\n', f'\n{refer_tag}')
            msg_string += refer_present + "\n"
        # fill in the message content
        msg_string += f"{message.author.display_name}: {message.content}"
        # add to print list
        txt_list.append(msg_string)
    # latest first --> oldest first
    if reverse_order:
        txt_list.reverse()
    return ('\n' if line_spacing else '' + "\n").join(txt_list)

async def read_DMs(userID):
    ch = await client.create_dm(client.get_user(userID))
    dm_msg_list = [msg async for msg in ch.history(limit=50)]
    print(await msgs_to_str(dm_msg_list, line_spacing=False))


async def print_bans():
    guild = client.get_guild(server_id)
    async for entry in guild.bans(limit=150):
        print(entry.user, entry.reason)

async def spam_dm(id, time, content):
    user = await client.fetch_user(id)
    channel = await user.create_dm()
    await channel.send("AAAAAAAAA")
    try:
        while True:
            await channel.send(content)
            await asyncio.sleep(time)
    except discord.Forbidden:
        print("User can not be dmed")
    except discord.HTTPException:
        print("Error")

async def single_dm(id, content):
    user = client.get_user(id)
    if str(type(user)) != "<class 'NoneType'>":
        channel = await client.create_dm(user)
        await channel.send(content=content)
    else:
        print("User can not be DMed!")

async def delete_msg(channelId, messageId):
    channel = client.get_channel(channelId)
    message = await channel.fetch_message(messageId)
    await channel.delete_messages([message])
  

#WELCOME & AUTOROLE

@client.event
async def on_member_join(member: discord.Member):
    channel = client.get_channel(welcome_channel)
    guild_name = member.guild.name
    role = ""
    guild = client.get_guild(server_id) #gets Guild Obj
    for obj in guild.roles: #discord.utils.get was not working, so this is my solution
        if obj.name == "Community":
            role = obj
    await member.add_roles(role) #Assigns role obj to member obj
    await channel.send(f"Welcome <@{member.id}> to {guild_name}!")
    #await client.get_channel(member_count_id).edit(name=f"Server Members: {client.get_guild(server_id).member_count}")


@tree.command(
    name="help",
    description="Displays a help message listing all available commands.",
    guild=discord.Object(id=server_id)
)
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(f"This currently does nothing.", ephemeral=True)

@tree.command(
    name="dm",
    description="Directly messages a list of users with a specified message.",
    guild=discord.Object(id=server_id)
)
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(f"This currently does nothing.", ephemeral=True)

@tree.command(
    name="roledm",
    description="Sends a direct message to all members with a specific role.",
    guild=discord.Object(id=server_id)
)
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(f"This currently does nothing.", ephemeral=True)

@tree.command(
    name="embed",
    description="Creates and sends an embed message with a title, body, and footer.",
    guild=discord.Object(id=server_id)
)
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(f"This currently does nothing.", ephemeral=True)

@tree.command(
    name="status",
    description="Changes the bot's display status message.",
    guild=discord.Object(id=server_id)
)
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(f"This currently does nothing.", ephemeral=True)


#GOODBYE

@client.event
async def on_member_remove(member: discord.Member):
    channel = client.get_channel(welcome_channel)
    await channel.send(f"Say goodbye to {member.name}!")
    #await client.get_channel(member_count_id).edit(name=f"Server Members: {client.get_guild(server_id).member_count}")

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if isinstance(message.channel,discord.DMChannel):
        user = client.get_user(600805505501364398)
        channel = await user.create_dm()
        await channel.send(content="New message from:\n" + message.author.name + ", " + str(message.author.id) + "\n\n" + "Said:\n" + message.content)
        if len(message.attachments) > 0:
            for i in message.attachments:
                time.sleep(3)
                await channel.send(content=i)
                
            

@tree.command(
    name="rules",
    description="Display the rules in an embed! (Must be ran in #rules)",
    guild=discord.Object(id=server_id)
)
async def rules(interaction):
    channel_ID = interaction.channel.id

    if channel_ID == rule_id:
        channel = client.get_channel(channel_ID)

        #EMBED BUILDER
        embed = discord.Embed(title="Rules - Team Vecro",
                        colour=000000)

        embed.add_field(name="1 — GENERAL RULES",
                    value="Rule 1.1 - No racist, offensive or other inappropriate usernames, nicknames or profile pictures.\n\nRule 1.2 - The staff members have the last word. Treat them with respect.\n\nRule 1.3 - Do not try to ping here or everyone.\n\nRule 1.4 - No begging for any roles (this includes staff roles, limited roles, etc.).\n\nRule 1.5 - Do not ping people or roles for no reason.\n\nRule 1.6 - Use the right channel for your needs.\n\nRule 1.7 - No similar nicknames or same usernames as staff members.\n\nRule 1.8 - No Mentioning: @.everyone / @.here\n\nRule 1.9 - No Blackmailing, Bribing, etc to staff members\n\nRule 1.10 - If banned from the server any and all alt accounts that are made by the person will be banned along with it and if rejoined on an alt account it shall be banned too",
                    inline=False)
        embed.add_field(name="─────────────────────────────────────────────────",
                    value="",
                    inline=False)
        embed.add_field(name="2 — CONTENT RULES",
                    value="Rule 2.1 - No advertising of any kind in direct messages.\n\nRule 2.2 - No spam of any type (e.g. messages, emojis, mentions, Gifs, images).\n\nRule 2.3 - No publishing of personal information (including addresses, emails, bank accounts, credit card information, etc.).\n\nRule 2.4 - No hate speech (mentioning killing, hurting, burning, etc.).\n\nRule 2.5 - No encouraging suicide or wishing harm.\n\nRule 2.6 - No slurs to a certain degree(n slur, f slur, r slur).\n\nRule 2.7 - No demeaning and shaming of other members.\n\nRule 2.8 - No \"Not Safe For Work (NSFW)\" content (this includes messages, Gifs, images, etc.).\n\nRule 2.9 - No content that relates to injuries to living beings.\n\nRule 2.10 -  Do not send malicious links/files in text channels and direct messages.\n\nRule 2.11 - If you are not welcomed in a VC do not keep joining it\n\nRule 2.12 - Self-promo channel is ONLY for personal content. DO NOT promote other teams in self-promo.",
                    inline=False)

        embed.set_footer(text="Bot created by armedforcesholdr")
        await channel.send(embed=embed)
    else:
        await interaction.response.send_message(content="You can not use this command! You can view the rules in #rules!", ephemeral=True)


@tree.command(
    name="ban_user",
    description="Ban someone",
    guild=discord.Object(id=server_id)
)
@app_commands.checks.has_permissions(ban_members = True)
async def ban(interaction, user: discord.Member, reason: str, del_recent_messages: bool):
    if (del_recent_messages):
        await client.get_guild(server_id).ban(user=user, reason=reason, delete_message_days=7)
    else:
        await client.get_guild(server_id).ban(user=user, reason=reason)
    await interaction.response.send_message("User has been banned", ephemeral=True)


@ban.error
async def ban_err(ctx, error):
    if isinstance(error, app_commands.MissingPermissions):
        await ctx.response.send_message(f"Hey! you don't have permission do use this command!")



@tree.command(
    name="unban_user",
    description="Unban someone",
    guild=discord.Object(id=server_id)
)
@app_commands.checks.has_permissions(ban_members = True)
async def unban(interaction, user_id: str, reason: str):
    user_id = str(user_id)
    await client.get_guild(server_id).unban(user=user_id, reason=reason)
    await interaction.response.send_message("User has been unbanned", ephemeral=True)


@unban.error
async def unban_err(ctx, error):
    if isinstance(error, app_commands.MissingPermissions):
        await ctx.response.send_message(f"Hey! you don't have permission do use this command!")

async def amain():
    async with asyncio.TaskGroup() as tg:
        import Vecro
        tg.create_task(Vecro.get_bot()[0].start(Vecro.get_bot()[1]))
        tg.create_task(client.start(bot_token))


        await asyncio.Event().wait() #Run the bots

asyncio.run(amain())