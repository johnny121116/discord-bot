import os
import discord
from discord.ext import commands
from discord import app_commands

# Define the bot client

class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

        try:
            guild = discord.Object(id=1567826278659395634)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} commands for guild {guild.id}")

        except Exception as e:
            print(f"Error syncing commands: {e}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.lower().startswith("你好"):
            await message.channel.send(f"你好 {message.author}!")

        if message.content.lower().startswith("早安"):
                    await message.channel.send(f"早安 {message.author}!")

        if message.content.lower().startswith("午安"):
                    await message.channel.send(f"午安 {message.author}!")
        
        if message.content.lower().startswith("晚安"):
                    await message.channel.send(f"晚安 {message.author}!")

    async def on_message_edit(self, before, after):
        if before.author == self.user:
            return
        await before.channel.send(
            f'{before.author.mention} 編輯了一則信息從 "{before.content}" 到 "{after.content}"'
        )

    async def on_message_delete(self, message):
        if message.author == self.user:
            return
        await message.channel.send(
            f'{message.author.mention} 刪除了他的信息： "{message.content}"'
        )

    async def on_member_join(self, member):
        if member.guild.system_channel is not None:
            await member.guild.system_channel.send(f"歡迎來到伺服器 {member.mention}！")

    async def on_member_remove(self, member):
        if member.guild.system_channel is not None:
            await member.guild.system_channel.send(f"{member.mention} 離開了伺服器。")

    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        guild = reaction.message.guild
        if not guild:
            return

        if hasattr(self, "color_roles_message_id") and reaction.message.id != self.color_roles_message_id:
            return

        reaction_role_map = {
            "🟥": "紅色",
            "🟩": "綠色",
            "🟦": "藍色",
            "🟨": "黃色"
        }
        role_name = reaction_role_map.get(str(reaction.emoji))
        if role_name:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await user.add_roles(role)
                print(f"{user.mention} 給予了 {role_name} 身份組！")

    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return

        guild = reaction.message.guild
        if not guild:
            return

        if hasattr(self, "color_roles_message_id") and reaction.message.id != self.color_roles_message_id:
            return

        reaction_role_map = {
            "🟥": "紅色",
            "🟩": "綠色",
            "🟦": "藍色",
            "🟨": "黃色"
        }
        role_name = reaction_role_map.get(str(reaction.emoji))
        if role_name:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await user.remove_roles(role)
                print(f"{user.mention} 已被移除 {role_name} 身份組！")


intents = discord.Intents.default()
intents.guild_messages = True
intents.guild_reactions = True
intents.members = True
intents.message_content = True
intents.reactions = True
intents.guilds = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=1567826278659395634)

# Define slash commands

@client.tree.command(name="顏色身份組", description = "創建一則信息可以讓成員選擇顏色身份組", guild=GUILD_ID)
async def color_roles(interaction: discord.Interaction):
    #check admin
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("你沒有權限使用此指令", ephemeral=True)
        return
    # ephemeral = True means that the message will only be visible to the user who invoked the command
    
    await interaction.response.defer(ephemeral=True)

    description = ("回應相對應的表情符號來獲得顏色身份組\n\n"
                   "🟥 - 紅色\n"
                   "🟩 - 綠色\n"
                   "🟦 - 藍色\n"
                   "🟨 - 黃色\n")

    embed = discord.Embed(title="顏色身份組獲取區", description=description, color=discord.Color.blue())
    message = await interaction.channel.send(embed=embed)

    emojis=["🟥", "🟩", "🟦", "🟨"]
    for emoji in emojis:
        await message.add_reaction(emoji)

    client.color_roles_message_id = message.id

    await interaction.followup.send("顏色身份組信息已創建！", ephemeral=True)



@client.tree.command(name="嗨", description="跟機器人打招呼", guild=GUILD_ID)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"嗨, {interaction.user.mention}!")

@client.tree.command(name="說", description="說一則信息", guild=GUILD_ID)
async def print_message(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"{message}")

@client.tree.command(name="embed", description="發送一則embed（暫時還無法自定義，嗯...）", guild=GUILD_ID)
async def embed_message(interaction: discord.Interaction, title: str, message: str):
    embed = discord.Embed(title=title, url="https://youtu.be/dQw4w9WgXcQ?si=KD-PRFGqEP7WB48e", description=message, color=discord.Color.blue())
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1567826279313702964/1568523369568010380/quail.egg.jpg?ex=6af020b9&is=6aeecf39&hm=179947e4a73d643438b4ffe2815565b4a0846337ea3ec7c90f4637c9852cba0a")
    embed.add_field(name="分標題1", value="第一個小區域", inline=False)
    embed.add_field(name="分標題2", value="第二個小區域", inline=False)
    embed.set_footer(text="小梵鵪鶉蛋，嘻嘻")
    embed.set_author(name=interaction.user.name, url="https://youtu.be/dQw4w9WgXcQ?si=KD-PRFGqEP7WB48e", icon_url=interaction.user.avatar.url)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="使用說明", description="小梵蛋的說明書", guild=GUILD_ID)
async def embed_message(interaction: discord.Interaction):
    embed = discord.Embed(title="小梵蛋使用說明", url="https://youtu.be/dQw4w9WgXcQ?si=KD-PRFGqEP7WB48e", description="這是小梵蛋的使用說明", color=discord.Color.green())
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1567826279313702964/1568523369568010380/quail.egg.jpg?ex=6af020b9&is=6aeecf39&hm=179947e4a73d643438b4ffe2815565b4a0846337ea3ec7c90f4637c9852cba0a")
    embed.set_author(name=interaction.user.name, url="https://youtu.be/dQw4w9WgXcQ?si=KD-PRFGqEP7WB48e", icon_url=interaction.user.avatar.url)
    class Menu1(discord.ui.Select):
            def __init__(self):
                options = [
                    discord.SelectOption(label="按鈕", description="一個指令", emoji='1️⃣'),
                    discord.SelectOption(label="顏色身份組", description="最自豪的指令", emoji= '2️⃣'),
                    discord.SelectOption(label="embed", description="其他指令", emoji='3️⃣'),
                    discord.SelectOption(label="嗨", description="酷酷指令", emoji='4️⃣'),
                    discord.SelectOption(label="說", description="挺好的指令", emoji='5️⃣'),
                    discord.SelectOption(label="選單", description="最後一個指令", emoji='6️⃣'),
                ]
                super().__init__(placeholder="選擇一個選項...", min_values=1, max_values=1, options=options)
    
            async def callback(self, interaction: discord.Interaction):
                if self.values[0] == "按鈕":
                    await interaction.response.send_message("按鈕指令可以發送一則包含按鈕的信息，點擊按鈕後會回應一則信息。")
                elif self.values[0] == "顏色身份組":
                    await interaction.response.send_message("顏色身份組指令可以讓你創建和管理顏色身份組。（我最自豪的指令）")
                elif self.values[0] == "embed":
                    await interaction.response.send_message("embed指令可以讓你創建和管理embed信息。（世上最爛的指令）")
                elif self.values[0] == "嗨":
                    await interaction.response.send_message("嗨指令可以讓你跟機器人打招呼。")
                elif self.values[0] == "說":
                    await interaction.response.send_message("說指令可以讓你跟機器人說話。")
                elif self.values[0] == "選單":
                    await interaction.response.send_message("選單指令可以讓你創建和管理選單。")

    class MenuView1(discord.ui.View):
         def __init__(self):
            super().__init__()
            self.add_item(Menu1())

    await interaction.response.send_message(embed=embed, view=MenuView1())

class View(discord.ui.View):
    @discord.ui.button(label="紅色", style=discord.ButtonStyle.red, emoji="🟥")
    async def red_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("點了紅色按鈕，你感覺火辣辣的！")

    @discord.ui.button(label="綠色", style=discord.ButtonStyle.green, emoji="🟩")
    async def green_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("你被綠了！")

@client.tree.command(name="按鈕", description="發送一則包含按鈕的信息", guild=GUILD_ID)
async def myButton(interaction: discord.Interaction):
    await interaction.response.send_message(view = View())


class Menu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="選項 1", description="這是第一個選項", emoji='1️⃣'),
            discord.SelectOption(label="選項 2", description="這是第二個選項", emoji= '2️⃣'),
            discord.SelectOption(label="選項 3", description="這是第三個選項", emoji='3️⃣'),
        ]
        super().__init__(placeholder="選擇一個選項...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "選項 1":
            await interaction.response.send_message("你選擇了 選項 1!")
        else:
            await interaction.response.send_message(f'你選了 {self.values[0]}')


class MenuView(discord.ui.View):
   def __init__(self):
       super().__init__()
       self.add_item(Menu())



@client.tree.command(name="選單", description="發送一則包含選單的信息", guild=GUILD_ID)
async def myMenu(interaction: discord.Interaction):
    await interaction.response.send_message(view=MenuView())



client.run(os.getenv("DISCORD_TOKEN"))
