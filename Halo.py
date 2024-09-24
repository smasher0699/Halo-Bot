import discord
from discord import app_commands
import datetime
import asyncio
import discord.ext
import discord.ext.commands
import time
import os
import typing
import json

bot_token = "MTI4NzI0NTIzMjAzOTI2NDI5Nw.GjEO6s.5IR9v3oY0rBEYLqd7rhF4cwgXxb_V-DMlrqT5E"
server_id = 1257037459292684450



#INTENTS

intents = discord.Intents.all() #Setting up intents
intents.message_content = True
client = discord.Client(intents=intents) #Creating bot
tree = app_commands.CommandTree(client) #Creating Slash Commands




#DATA FUNCTIONS

def get_server_data():
    with open(os.getcwd() + 'save_data.json') as json_file:
        return json.load(json_file)

def save_server_data(data):
    with open(os.getcwd() + 'save_data.json', 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)




#PING COMMAND


@tree.command(
    name="ping",
    description="Returns the ping of the bot.",
    guild=discord.Object(id=server_id)
)
async def ping(interaction):
    await interaction.response.send_message(f"My ping is {round(client.latency)} ms!")





#ON READY

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))
    client.add_view(ButtonView())
    print(f'We have logged in as {client.user}')
    



#WELCOME

@client.event
async def on_member_join(member: discord.Member):
    data = get_server_data()
    channel = client.get_channel(data['welcomechannel'])
    guild_name = member.guild.name
    await channel.send(f"Welcome <@{member.id}> to {guild_name}!")







#/HELP COMMAND

@tree.command(
    name="help",
    description="Displays a help message listing all available commands.",
    guild=discord.Object(id=server_id)
)
async def help(interaction: discord.Interaction):
    if interaction.user.id == interaction.guild.owner.id:
        embed = discord.Embed(title="Command Help",
                        description="These are the commands this bot can run!",
                        colour=0x00b0f4,
                        timestamp=datetime.datetime.now())

        embed.add_field(name="**/help**",
                        value="Displays a help message listing all available commands.",
                        inline=False)
        embed.add_field(name="**/ping**",
                        value="Returns the ping of the bot.",
                        inline=True)
        embed.add_field(name="**/dm**",
                        value="Directly messages a list of users with a specified message. (Separate all users with a comma and single space). (Owner Only)",
                        inline=False)
        embed.add_field(name="**/roledm**",
                        value="Sends a direct message to all members with a specific role.",
                        inline=False)
        embed.add_field(name="**/embed**",
                        value="Creates and sends an embed message with a title, body, and footer.",
                        inline=False)
        embed.add_field(name="**/set_rules_channel**",
                        value="Changes the channel that the rules are sent to.",
                        inline=False)
        embed.add_field(name="**/status**",
                        value="Changes the bot's display status message.",
                        inline=False)
        embed.add_field(name="**/streaming_status**",
                        value="Changes the bot's display status message to streaming.",
                        inline=False)
        embed.add_field(name="**/set_welcome_channel**",
                        value="Changes the welcome channel of the bot.",
                        inline=False)
        embed.add_field(name="**/rules**",
                        value="Display the rules in an embed. (Must be ran in #rules) (Owner Only)",
                        inline=False)
        embed.add_field(name="**/ban_user**",
                        value="Ban someone. (Ban permissions only)",
                        inline=False)
        embed.add_field(name="**/unban_user**",
                        value="Unban someone. (Ban permissions only)",
                        inline=False)

        embed.set_footer(text="Bot made by armedforcesholdr")

        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message("You do not have access to this command! You can view the rules in the rules channel.", ephemeral=True)





#DM CERTAIN USERS

@tree.command(
    name="dm",
    description="Directly messages a list of users with a specified message. (Separate all users with a comma and single space)",
    guild=discord.Object(id=server_id)
)
async def dmaer(interaction: discord.Interaction, users: str, message: str, ping: bool):
    if interaction.user.id == interaction.guild.owner.id:
        await interaction.response.send_message(f"DM's have started! (Some users might not be able to be DM'ed due to privacy settings.)", ephemeral=True)
        for v in users.split(", "):
            i = client.get_user(int(v))
            if ping:
                await i.dm_channel.send(message + f" <@{i.id}>")
            else:
                await i.dm_channel.send(message)
    else:
        await interaction.response.send_message(f"You do not have access to this command!", ephemeral=True)
        




#DM USERS IN A ROLE

@tree.command(
    name="roledm",
    description="Sends a direct message to all members with a specific role.",
    guild=discord.Object(id=server_id)
)
async def roledm(interaction: discord.Interaction, role: discord.Role, message: str, ping: bool):
    if interaction.user.id == interaction.guild.owner.id:
        await interaction.response.send_message(f"DM's have started! (Some users might not be able to be DM'ed due to privacy settings.)", ephemeral=True)
        for i in interaction.guild.members:
            for v in i.roles:
                if v.id == role.id:
                    if ping:
                        await i.dm_channel.send(message + f" <@{i.id}>")
                    else:
                        await i.dm_channel.send(message)
    else:
        await interaction.response.send_message(f"You do not have access to this command!", ephemeral=True)






#SEND A CUSTOM EMBED


@tree.command(
    name="embed",
    description="Creates and sends an embed message with a title, body, and footer.",
    guild=discord.Object(id=server_id)
)
async def embedsend(interaction: discord.Interaction, title: str, hexcolor: str, body_description: str, title_url: str = None, author_title: str = None, author_url: str = None, author_icon_url: str = None, field_a_title: str = None, field_a_body: str = None, field_a_inline: bool = None, field_b_title: str = None, field_b_body: str = None, field_b_inline: bool = None, field_c_title: str = None, field_c_body: str = None, field_c_inline: bool = None, field_d_title: str = None, field_d_body: str = None, field_d_inline: bool = None, field_e_title: str = None, field_e_body: str = None, field_e_inline: bool = None, field_f_title: str = None, field_f_body: str = None, field_f_inline: bool = None, field_g_title: str = None, field_g_body: str = None, field_g_inline: bool = None, field_h_title: str = None, field_h_body: str = None, field_h_inline: bool = None, field_i_title: str = None, field_i_body: str = None, field_i_inline: bool = None, image_url: str = None, thumbnail_url: str = None, footer_text: str = None, footer_icon_url: str = None, timestamp: bool = None):
    if interaction.user.id == interaction.guild.owner.id:
        emb = discord.Embed(title=title, color=hex(int(hexcolor, 16)), description=body_description)
        if title_url:
            emb.url = title_url
        if author_title:
            emb.set_author(name=author_title)
        if author_url and author_title:
            emb.set_author(name=author_title, url=author_url)
        if author_icon_url and author_url and author_title:
            emb.set_author(name=author_title, url=author_url, icon_url=author_icon_url)
        
        #FIELDS
        if field_a_body and field_a_title and field_a_inline:
            emb.add_field(name=field_a_title, value=field_a_body, inline=field_a_inline)
        elif field_a_body and field_a_title:
            emb.add_field(name=field_a_title, value=field_a_body, inline=False)
        
        if field_b_body and field_b_title and field_b_inline:
            emb.add_field(name=field_b_title, value=field_b_body, inline=field_b_inline)
        elif field_b_body and field_b_title:
            emb.add_field(name=field_b_title, value=field_b_body, inline=False)
        
        if field_c_body and field_c_title and field_c_inline:
            emb.add_field(name=field_c_title, value=field_c_body, inline=field_c_inline)
        elif field_c_body and field_c_title:
            emb.add_field(name=field_c_title, value=field_c_body, inline=False)
        
        if field_d_body and field_d_title and field_d_inline:
            emb.add_field(name=field_d_title, value=field_d_body, inline=field_d_inline)
        elif field_d_body and field_d_title:
            emb.add_field(name=field_d_title, value=field_d_body, inline=False)
        
        if field_e_body and field_e_title and field_e_inline:
            emb.add_field(name=field_e_title, value=field_e_body, inline=field_e_inline)
        elif field_e_body and field_e_title:
            emb.add_field(name=field_e_title, value=field_e_body, inline=False)
        
        if field_f_body and field_f_title and field_f_inline:
            emb.add_field(name=field_f_title, value=field_f_body, inline=field_f_inline)
        elif field_f_body and field_f_title:
            emb.add_field(name=field_f_title, value=field_f_body, inline=False)
        
        if field_g_body and field_g_title and field_g_inline:
            emb.add_field(name=field_g_title, value=field_g_body, inline=field_g_inline)
        elif field_g_body and field_g_title:
            emb.add_field(name=field_g_title, value=field_g_body, inline=False)
        
        if field_h_body and field_h_title and field_h_inline:
            emb.add_field(name=field_h_title, value=field_h_body, inline=field_h_inline)
        elif field_h_body and field_h_title:
            emb.add_field(name=field_h_title, value=field_h_body, inline=False)
        
        if field_i_body and field_i_title and field_i_inline:
            emb.add_field(name=field_i_title, value=field_i_body, inline=field_i_inline)
        elif field_i_body and field_i_title:
            emb.add_field(name=field_i_title, value=field_i_body, inline=False)

        if image_url:
            emb.set_image(url=image_url)
        if thumbnail_url:
            emb.set_thumbnail(url=thumbnail_url)
        if footer_text:
            emb.set_footer(text=footer_text)
        if footer_icon_url and footer_text:
            emb.set_footer(text=footer_text, icon_url=footer_icon_url)
        if timestamp:
            emb.timestamp = datetime.datetime.now()
        await interaction.response.send_message(embed=emb)
    else:
        await interaction.response.send_message("You do not have access to this command!", ephemeral=True)




#SET RULES CHANNEL

@tree.command(
    name="set_rules_channel",
    description="Changes the channel that the rules are sent to.",
    guild=discord.Object(id=server_id)
)
async def welcset(interaction: discord.Interaction, channel: discord.TextChannel):
    if interaction.user.id == interaction.guild.owner.id:
        data = get_server_data()
        data['ruleschannel'] = channel.id
        save_server_data(data)
        await interaction.response.send_message("Rules channel has been changed!", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)





#SET BOT'S STATUS

@tree.command(
    name="status",
    description="Changes the bot's display status message.",
    guild=discord.Object(id=server_id)
)
async def status(interaction: discord.Interaction, activity: typing.Literal['Game', 'Listening', 'Watching'], name: str):
    if interaction.user.id == interaction.guild.owner.id:
        if activity == 'Game':
            await client.change_presence(activity=discord.Game(name=name))
        elif activity == 'Listening':
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=name))
        elif activity == 'Watching':
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=name))
        await interaction.response.send_message(f"Status was changed!", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)
        





#SET STATUS TO STREAMING

@tree.command(
    name="streaming_status",
    description="Changes the bot's display status message to streaming.",
    guild=discord.Object(id=server_id)
)
async def status(interaction: discord.Interaction, name: str, url: str):
    if interaction.user.id == interaction.guild.owner.id:
        await client.change_presence(activity=discord.Streaming(name=name, url=url))
        await interaction.response.send_message(f"Status was changed!", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)






#SET CHANNEL THAT WELCOMES GO TO

@tree.command(
    name="set_welcome_channel",
    description="Changes the welcome channel of the bot.",
    guild=discord.Object(id=server_id)
)
async def setwelc(interaction: discord.Interaction, channel: discord.TextChannel):
    if interaction.user.id == interaction.guild.owner.id:
        data = get_server_data()
        data['welcomechannel'] = channel.id
        save_server_data(data)
        await interaction.response.send_message(f"Channel has been set!", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)







#GOODBYE

@client.event
async def on_member_remove(member: discord.Member):
    data = get_server_data()
    channel = client.get_channel(data['welcomechannel'])
    await channel.send(f"Say goodbye to {member.name}!")
    #await client.get_channel(member_count_id).edit(name=f"Server Members: {client.get_guild(server_id).member_count}")





#SEND ALL DM'S TO OWNER

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






#BUTTONS FOR /RULES


class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Discord TOS", style=discord.ButtonStyle.link, url='discord.com/terms')
    async def function_name(self, int: discord.Interaction):
        await int.response.send_message("")

    @discord.ui.button(label="Discord Community Guidelines", style=discord.ButtonStyle.link, url='discord.com/guidelines')
    async def function_name(self, int: discord.Interaction):
        await int.response.send_message("")





#/RULES COMMAND



@tree.command(
    name="rules",
    description="Display the rules in an embed! (Must be ran in #rules)",
    guild=discord.Object(id=server_id)
)
async def rules(interaction: discord.Interaction):
    channel_ID = get_server_data()['ruleschannel']

    if interaction.user.id == interaction.guild.owner.id:
        channel = client.get_channel(channel_ID)
        await channel.send("Hello! Welcome to Team Halo!\n\nPlease read the rules below!")
        #EMBED BUILDER
        embed = discord.Embed(title="Rules - Team Halo",
                        colour=000000)

        embed.add_field(name="1 — GENERAL RULES",
                    value="**RULES** \n\n\n**1.** Respect: Harassment, hate speech, and discrimination are strictly prohibited.\n\n**2.** Content: No spamming, NSFW content, or illegal material.\n\n**3.** Privacy: Doxxing, phishing, or sharing personal information without consent is not tolerated.\n\n**4.** Channels: Post in the appropriate channels based on the topic.\n\n**5.** Moderation: Follow moderator instructions and report any issues immediately.\n\n**6.** Engagement: Maintain a positive tone. Handle conflicts privately.\n\n**7.** Advertisements: Team ads require prior approval.\n\n**8.** Events: Follow event rules and respect organisers.\n\n**9.** Bot Usage: Misuse of bots is prohibited. Follow bot-specific rules.\n\n**10.** Voice Channels: Minimise background noise and use push-to-talk when necessary.\n\n**11.** Copyright: Respect intellectual property and credit creators.\n\n12 .External Conflicts: Handle personal drama or external conflicts in private, not in public channels.",
                    inline=False)

        await channel.send(embed=embed, view=ButtonView())
    else:
        await interaction.response.send_message(content="You can not use this command! You can view the rules in the rules channel!", ephemeral=True)







#BAN A USER

@tree.command(
    name="ban_user",
    description="Ban someone.",
    guild=discord.Object(id=server_id)
)
@app_commands.checks.has_permissions(ban_members = True)
async def ban(interaction, user: discord.Member, reason: str, del_recent_messages: bool):
    if (del_recent_messages):
        await client.get_guild(server_id).ban(user=user, reason=reason, delete_message_days=7)
    else:
        await client.get_guild(server_id).ban(user=user, reason=reason)
    await interaction.response.send_message("User has been banned", ephemeral=True)


@ban.error #Ran when user does not meet the permission requirements
async def ban_err(ctx, error):
    if isinstance(error, app_commands.MissingPermissions):
        await ctx.response.send_message(f"Hey! you don't have permission do use this command!") #Respond to user





#UNBAN SOMEONE



@tree.command(
    name="unban_user",
    description="Unban someone",
    guild=discord.Object(id=server_id)
)
@app_commands.checks.has_permissions(ban_members = True) #Make sure they have permissions
async def unban(interaction, user_id: str, reason: str):
    user_id = str(user_id) #Get user ID
    await client.get_guild(server_id).unban(user=user_id, reason=reason) #Unban them
    await interaction.response.send_message("User has been unbanned", ephemeral=True) #Respond to user


@unban.error #Ran when permissions have not been met
async def unban_err(ctx, error):
    if isinstance(error, app_commands.MissingPermissions):
        await ctx.response.send_message(f"Hey! you don't have permission do use this command!")





#RUN THE BOT

async def amain(): #Bot runner
    async with asyncio.TaskGroup() as tg:
        tg.create_task(client.start(bot_token)) #Start the bot
        await asyncio.Event().wait() #Run forever

asyncio.run(amain()) #Run the bots