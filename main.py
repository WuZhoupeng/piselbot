import os
import discord
from discord.ext import commands
#from dotenv import load_dotenv
import asyncio
from utils.databaseMessaggi import db_messaggi
from utils.setupTables import SetupTables

#load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
PREFIX = os.getenv("BOT_PREFIX")

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Cog caricati: {list(bot.cogs.keys())}")

    try:
        synced = await bot.tree.sync()
        print(f"Slash comandi sincronizzati: {len(synced)}")
    except Exception as e:
        print(f"Errore nella sincronizzazione degli slash commands: {e}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("**Non esiste questo comando. Ricontrollalo attentamente**")

@bot.event
async def on_message(message):
    try:
        if message.author == bot.user:
            return
    
        embed = discord.Embed(
            description="Questo bot è stato creato da **Leon Mondiale** su richiesta di Adri",
            color=0x004b06
        )
        embed.set_footer(text="© 2025, Leon Mondiale. Tutti i diritti riservati.")

        if bot.user in message.mentions and not message.reference:
            await message.reply(embed=embed)
    except Exception as e:
        await message.channel.send(e)
    
    await bot.process_commands(message)

async def load_cogs():
    from my_commands import setup as setup_commands
    from my_slash_commands import setup as setup_slash_commands
    await setup_commands(bot)
    await setup_slash_commands(bot)

async def main():
    bot.db_messaggi = await db_messaggi.create_pool()

    await SetupTables(bot.db_messaggi)

    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

    bot.db_messaggi.close()

asyncio.run(main())