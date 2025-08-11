import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime


class ReminderMessagesSlashCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_pool = bot.db_messaggi
        self.check_send_message.start()

    @discord.app_commands.command(
        name="reminder_messages",
        description="Programma un messaggio per un canale specifico ad un orario specifico"
    )
    @app_commands.checks.has_role(1398076806594035773) # Ruolo ---> Pisello petulante
    @app_commands.describe(
        message="Messaggio da inviare al canale",
        time_date="Mettere una data con il formato YYYY-MM-DD (ad esempio 2025-12-31)",
        time_hour="Mettere un orario con il formato HH:MM (ad esempio 19:00)"
    )
    async def reminder_messages(self, interaction: discord.Interaction, message: str, time_date: str, time_hour: str=None):
        time_hour = time_hour or '19:00'
        time_date_datetime = datetime.strptime(time_date, "%Y-%m-%d").date()
        time_hour_datetime = datetime.strptime(time_hour, "%H:%M").time()
        time_date_hour = datetime.combine(time_date_datetime, time_hour_datetime)

        if datetime.now() > time_date_hour:
            await interaction.response.send_message("Oh zio, non sei un viaggiatore del tempo")
            return
        
        async with self.db_pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO reminder_messages (message, time, date)
                VALUES ($1, $2, $3)
            ''', message, time_hour_datetime, time_date_datetime)

            timestamp = int(time_date_hour.timestamp())
            await interaction.response.send_message(f"È stato inserito correttamente il messaggio per il giorno <t:{timestamp}:F>")

    @tasks.loop(minutes=1)
    async def check_send_message(self):
        async with self.db_pool.acquire() as conn:
            message_to_send = await conn.fetchrow('''
                SELECT * FROM reminder_messages
                WHERE id = (SELECT MIN(id) FROM reminder_messages)
            ''')

            if message_to_send is None:
                return

            time_to_send = datetime.combine(message_to_send['date'], message_to_send['time'])

            if datetime.now() > time_to_send:
                try:
                    channel_send_in = self.bot.get_channel(1382289347285483531) # Test channel ---> 1337486382028951646 | 1382289347285483531
                
                    # embed = discord.Embed(
                    #     description=message_to_send['message'],
                    #     color=0x2dff00
                    # )

                    await channel_send_in.send(message_to_send['message'])

                    await conn.execute('''
                        DELETE FROM reminder_messages
                        WHERE id = $1
                    ''', message_to_send['id'])
                except Exception as e:
                    print(e)
                    self.check_send_message.restart()

    @check_send_message.before_loop
    async def before_check_send_message(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.check_send_message.cancel()

    @reminder_messages.error
    async def reminder_messages_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message(error)

    @check_send_message.error
    async def check_send_message_error(self, error):
        print(f"Errore task loop: {error}")

        if not self.check_send_message.is_running():
            try:
                self.check_send_message.restart()
            except Exception as e:
                print(f"Errore restart: {e}")

async def setup(bot):
    await bot.add_cog(ReminderMessagesSlashCog(bot))