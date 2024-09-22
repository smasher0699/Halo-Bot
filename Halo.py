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
server_id = 1257037459292684450
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
    



#WELCOME & AUTOROLE

@client.event
async def on_member_join(member: discord.Member):
    data = get_server_data()
    channel = client.get_channel(data['welcomechannel'])
    guild_name = member.guild.name
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
async def dmaer(interaction: discord.Interaction):
    await interaction.response.send_message(f"This currently does nothing.", ephemeral=True)

@tree.command(
    name="roledm",
    description="Sends a direct message to all members with a specific role.",
    guild=discord.Object(id=server_id)
)
async def roledm(interaction: discord.Interaction):
    await interaction.response.send_message(f"This currently does nothing.", ephemeral=True)

@tree.command(
    name="embed",
    description="Creates and sends an embed message with a title, body, and footer.",
    guild=discord.Object(id=server_id)
)
async def embedsend(interaction: discord.Interaction):
    await interaction.response.send_message(f"This currently does nothing.", ephemeral=True)

@tree.command(
    name="status",
    description="Changes the bot's display status message.",
    guild=discord.Object(id=server_id)
)
async def status(interaction: discord.Interaction):
    await interaction.response.send_message(f"This currently does nothing.", ephemeral=True)

@tree.command(
    name="set_welcome_channel",
    description="Changes the welcome channel of the bot.",
    guild=discord.Object(id=server_id)
)
async def status(interaction: discord.Interaction, channel: discord.TextChannel):
    if interaction.user.id == interaction.guild.owner.id:
        data = get_server_data()
        data['welcomechannel'] = channel.id
        save_server_data(data)
        await interaction.response.send_message(f"Channel has been set!", ephemeral=True)


#GOODBYE

@client.event
async def on_member_remove(member: discord.Member):
    data = get_server_data()
    channel = client.get_channel(data['welcomechannel'])
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
        embed = discord.Embed(title="Rules - Team Halo",
                        colour=000000)

        embed.add_field(name="1 — GENERAL RULES",
                    value="INSERT RULES HERE",
                    inline=False)
        embed.add_field(name="─────────────────────────────────────────────────",
                    value="",
                    inline=False)
        embed.add_field(name="2 — CONTENT RULES",
                    value="INSERT RULES HERE",
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