import discord
from discord.ext import commands
from discord import app_commands
from db import get_lb, get_user

class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(
        name = "leaderboard",
        description = "Check leaderboard of top engagers."
    )
    @app_commands.guild_only()
    async def leaderboard(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        data = await get_lb(interaction.user.id)
        dt = discord.utils.utcnow()
        embed = discord.Embed(title="**Leadererboard of top 10 !!**",
                              description=data, color=0x5bcff5)
        embed.set_image(url="https://imgur.com/1ViskLR")
        embed.set_footer(text= f'Today at', icon_url=self.client.user.avatar.url)
        embed.timestamp = dt
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(
        name = "myrank",
        description = "Check Your server rank and points."
    )
    @app_commands.guild_only()
    async def myrank(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        data = await get_user(interaction.user.id)
        if data:
            dt = discord.utils.utcnow()
            embed = discord.Embed(title=f"**Your Server Rank: {data['rank']}**",
                                description=f'• Username: {data['username']}\n• Total Points: {data['points']}', color=0x5bcff5)
            embed.set_footer(text= f'Today at', icon_url=self.client.user.avatar.url)
            embed.timestamp = dt
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(content="> **You're not ranked yet please engage in the server and try again")

async def setup(bot):
    await bot.add_cog(UserCog(bot))