from discord.ext import commands

class HelloCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.reply("Ciao!")

async def setup(bot):
    await bot.add_cog(HelloCog(bot))