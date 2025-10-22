from discord.ext import commands

class SkullCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="skull")
    async def skull(self, ctx, *args):
        message = ctx.message

        if message.author.bot:
            await ctx.reply("Bro 💀 ☠ ⚰")
            return
        
        if args:
            await ctx.reply("**Troppi argomenti. Non si accettano argomenti**")
            return

        if message.reference:
            try:
                referenced_message = await message.channel.fetch_message(message.reference.message_id)
                
                emoji_list = ["💀", "☠", "⚰"]
                already_reacted = False

                for emoji in emoji_list:
                    for reaction in referenced_message.reactions:
                        if str(reaction.emoji) == emoji and reaction.me:
                            already_reacted = True
                            break

                    if already_reacted:
                        break

                if already_reacted:
                    await ctx.reply("Messaggio già reactato")
                    return

                await referenced_message.add_reaction("💀")
                await referenced_message.add_reaction("☠")
                await referenced_message.add_reaction("⚰")
            except Exception as e:
                await ctx.send(e)
        else:
            await ctx.reply("Devi rispondere a un messaggio per usare questo comando")
    
    @skull.error
    async def skull_error(self, ctx, error):
        await ctx.reply(error)

async def setup(bot):
    await bot.add_cog(SkullCog(bot))