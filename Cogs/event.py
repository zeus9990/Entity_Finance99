import discord, re, time
from discord.ext import commands
from config import NO_POINT_CH, DOUBLE_POINT_CH
from db import give_points

user_activity = {}
RATE_LIMIT_SECONDS = 5
COOLDOWN_SECONDS = 60

class EventCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in NO_POINT_CH:
            return
        
        if message.author.bot:
            return
        
        if message.stickers:
            return
        
        content = message.content.strip()
        if content:
            if (content.startswith("http://") or content.startswith("https://")) and len(content.split()) == 1:
                return
            
            elif re.search(r"(.)\1{4,}", content):
                return
            
            elif re.match('<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>', content):
                return
            
            else:
                user_id = message.author.id
                current_time = time.time()

                # Initialize user data if not present
                if user_id not in user_activity:
                    user_activity[user_id] = {"last_message_time": 0, "on_cooldown": False, "cooldown_until": 0}

                user_data = user_activity[user_id]

                # Check if the user is currently on cooldown
                if user_data["on_cooldown"]:
                    if current_time < user_data["cooldown_until"]:
                        return
                    else:
                        # Cooldown has expired, reset status
                        user_data["on_cooldown"] = False

                # Check if the user has sent a message recently
                time_since_last_message = current_time - user_data["last_message_time"]
                if time_since_last_message < RATE_LIMIT_SECONDS:
                    # User is spamming, apply cooldown
                    user_data["on_cooldown"] = True
                    user_data["cooldown_until"] = current_time + COOLDOWN_SECONDS
                    return

                # Update the last message time for this user
                user_data["last_message_time"] = current_time
                
                #Adding points
                points = 0
                char = len(content)
                if char >= 50:
                    points += 3
                elif char >= 20:
                    points += 2
                elif char >= 5:
                    points += 1
                if message.channel.id in DOUBLE_POINT_CH:
                    points *= 2
                
                await give_points(user_id, message.author.name, message.author.display_name, points)

async def setup(bot):
    await bot.add_cog(EventCog(bot))