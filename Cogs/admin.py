import discord
from discord.ext import commands
from discord import app_commands
from db import give_points, remove_points, get_user, admin_lb
from config import ADMIN_ROLES

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def check(self, interaction):
        if [i for i in interaction.user.roles if i.id in ADMIN_ROLES]:
            return True

    @app_commands.command(
        name = "addpoints",
        description = "add points to a user."
    )
    @app_commands.describe(
        user = 'user to add the points to.',
        points = 'number of points to be added.'
    )
    @app_commands.guild_only()
    async def addpoints(self, interaction: discord.Interaction, user: discord.Member, points: int):
        if await self.check(interaction):
            await interaction.response.defer(thinking=True)
            data = await give_points(userid=interaction.user.id, username=interaction.user.name, display_name=interaction.user.display_name, points=points)
            dt = discord.utils.utcnow()
            embed = discord.Embed(title=f"**Successfully added points to {user.mention}!!**",color=0x5bcff5)
            embed.set_footer(text= f'Today at', icon_url=self.client.user.avatar.url)
            embed.timestamp = dt
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(content='> **Sorry, this is a admin command only.**', ephemeral=True)

    @app_commands.command(
        name = "removepoints",
        description = "add points to a user."
    )
    @app_commands.describe(
        user = 'user to remove the points from.',
        points = 'number of points to be removed.'
    )
    @app_commands.guild_only()
    async def removepoints(self, interaction: discord.Interaction, user: discord.Member, points: int):
        if await self.check(interaction):
            await interaction.response.defer(thinking=True)
            data = await remove_points(userid=interaction.user.id, username=interaction.user.name, display_name=interaction.user.display_name, points=points)
            dt = discord.utils.utcnow()
            embed = discord.Embed(title=f"**Successfully removed points from {user.mention}!!**",color=0x5bcff5)
            embed.set_footer(text= f'Today at', icon_url=self.client.user.avatar.url)
            embed.timestamp = dt
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(content='> **Sorry, this is a admin command only.**', ephemeral=True)

    @app_commands.command(
        name = "points",
        description = "Check a users server rank and points."
    )
    @app_commands.describe(
        user = 'check details of the user.'
    )
    @app_commands.guild_only()
    async def myrank(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer(ephemeral=True, thinking=True)
        if self.check(interaction):
            data = await get_user(user.id)
            if data:
                dt = discord.utils.utcnow()
                embed = discord.Embed(title=f"**Details of the User !!**",
                                    description=f'• Username: {data['username']}\n• Display name: {data['display_name']}\n• Server rank: {data['rank']}\n• Total Points: {data['points']}', color=0x5bcff5)
                embed.set_footer(text= f'Today at', icon_url=self.client.user.avatar.url)
                embed.timestamp = dt
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(content="> **No records found for this user.**")
        else:
            await interaction.followup.send(content='> **Sorry, this is a admin command only.**')
    
    @app_commands.command(
        name = "leaderboard_admin",
        description = "Check leaderboard from a selected rank."
    )
    @app_commands.describe(
        rank = 'rank from where you want to check next 10 users.'
    )
    @app_commands.guild_only()
    async def leaderboard(self, interaction: discord.Interaction, rank: int):
        await interaction.response.defer(thinking=True)
        if self.check(interaction):
            is_data, data = await admin_lb(rank)
            if is_data:
                dt = discord.utils.utcnow()
                embed = discord.Embed(title=f"**Leadererboard of top 10 after rank {rank}!!**",
                                    description=data, color=0x5bcff5)
                embed.set_image(url="https://imgur.com/1ViskLR")
                embed.set_footer(text= f'Today at', icon_url=self.client.user.avatar.url)
                embed.timestamp = dt
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(content=f'> **{data}**')
        else:
            await interaction.followup.send(content='> **Sorry, this is a admin command only.**', ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminCog(bot))