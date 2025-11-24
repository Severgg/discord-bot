import discord
import os
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Канал, куда бот будет отправлять логи
LOG_CHANNEL_ID = 1441248218619838524


async def send_log(message, guild):
    channel = guild.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(embed=message)


@bot.event
async def on_ready():
    print(f"Бот запущен как {bot.user}")


# 🔸 Лог: удалено сообщение
@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    embed = discord.Embed(
        title="🗑 Удалено сообщение",
        description=(
            f"**Автор:** {message.author.mention}\n"
            f"**Канал:** {message.channel.mention}\n\n"
            f"**Текст:**\n```{message.content}```"
        ),
        color=discord.Color.red()
    )
    await send_log(embed, message.guild)


# 🔸 Лог: отредактировано сообщение
@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    if before.content == after.content:
        return

    embed = discord.Embed(
        title="✏ Изменено сообщение",
        description=(
            f"**Автор:** {before.author.mention}\n"
            f"**Канал:** {before.channel.mention}"
        ),
        color=discord.Color.orange()
    )
    embed.add_field(name="До:", value=f"```{before.content}```", inline=False)
    embed.add_field(name="После:", value=f"```{after.content}```", inline=False)

    await send_log(embed, before.guild)


# 🔸 Лог: участник зашёл
@bot.event
async def on_member_join(member):
    embed = discord.Embed(
        title="👤 Участник зашёл",
        description=f"{member.mention} присоединился к серверу!",
        color=discord.Color.green()
    )
    await send_log(embed, member.guild)


# 🔸 Лог: участник вышел
@bot.event
async def on_member_remove(member):
    embed = discord.Embed(
        title="🚪 Участник вышел",
        description=f"{member.name} покинул сервер.",
        color=discord.Color.red()
    )
    await send_log(embed, member.guild)


# 🔸 Лог: создан канал
@bot.event
async def on_guild_channel_create(channel):
    embed = discord.Embed(
        title="📁 Создан канал",
        description=f"Создан канал: {channel.mention}",
        color=discord.Color.blue()
    )
    await send_log(embed, channel.guild)


# 🔸 Лог: удалён канал
@bot.event
async def on_guild_channel_delete(channel):
    embed = discord.Embed(
        title="🗑 Удалён канал",
        description=f"Удалён канал: **{channel.name}**",
        color=discord.Color.red()
    )
    await send_log(embed, channel.guild)


# 🔸 Лог: изменения ролей у участника
@bot.event
async def on_member_update(before, after):
    before_roles = set(before.roles)
    after_roles = set(after.roles)

    gained = after_roles - before_roles
    removed = before_roles - after_roles

    for role in gained:
        embed = discord.Embed(
            title="🎖 Выдана роль",
            description=f"{after.mention} получил роль **{role.name}**",
            color=discord.Color.green()
        )
        await send_log(embed, after.guild)

    for role in removed:
        embed = discord.Embed(
            title="❌ Снята роль",
            description=f"{after.mention} потерял роль **{role.name}**",
            color=discord.Color.red()
        )
        await send_log(embed, after.guild)


# 🔸 Лог: бан
@bot.event
async def on_member_ban(guild, user):
    embed = discord.Embed(
        title="🔨 Бан",
        description=f"{user} был забанен.",
        color=discord.Color.dark_red()
    )
    await send_log(embed, guild)


# 🔸 Лог: разбан
@bot.event
async def on_member_unban(guild, user):
    embed = discord.Embed(
        title="🕊 Разбан",
        description=f"{user} был разбанен.",
        color=discord.Color.green()
    )
    await send_log(embed, guild)


bot.run(os.getenv("DISCORD_TOKEN"))
