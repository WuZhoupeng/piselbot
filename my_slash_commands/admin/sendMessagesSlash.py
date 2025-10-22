import discord
from discord.ext import commands
from discord import app_commands

class SendMessagesSlashCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_pool = bot.db_messaggi

    @discord.app_commands.command(
        name="send_message",
        description="Manda un messaggio in un canale"
    )
    @app_commands.checks.has_role(1398076806594035773) # Ruolo ---> Pisello petulante
    @app_commands.describe(
        message="Messaggio da inviare al canale",
        channel="Mettere l'id del canale (OPZIONALE)",
        file="Mettere un file insieme al messaggio (OPZIONALE)"
    )
    async def send_messages(self, interaction: discord.Interaction, message: str, channel: discord.TextChannel=None, file: discord.Attachment=None):
        await interaction.response.defer()

        if channel is None:
            channel_id = 1382289347285483531
        else:
            channel_id = channel.id
        
        channel_send_in = self.bot.get_channel(channel_id) # Test channel ---> 1337486382028951646 | 1382289347285483531

        if file is None:
            await channel_send_in.send(message)
        else:
            await channel_send_in.send(message, file=await file.to_file())

        await interaction.followup.send(f"Messaggio inviato con successo nel canale <#{channel_id}>")

    @send_messages.error
    async def send_messages_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(error)

async def setup(bot):
    await bot.add_cog(SendMessagesSlashCog(bot))