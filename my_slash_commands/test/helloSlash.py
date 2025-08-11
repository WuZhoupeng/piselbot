import discord
from discord.ext import commands
from discord import app_commands

class HelloSlashCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="hello", description="Saluta una persona")
    @app_commands.describe(member="L'utente da taggare")
    async def hello(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        await interaction.response.send_message(f"Ciao {member.mention} (Adri Gay)")

    @hello.error
    async def hello_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(error, ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelloSlashCog(bot))