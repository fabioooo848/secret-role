import discord
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_ID = 1400404225845886976  # Your role's actual ID
CHANCE = 0.01                  # 1% chance per message
EMOJI = "🥚"                   # Golden Egg emoji or whatever you prefer

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if random.random() < CHANCE:
        guild = message.guild
        role = guild.get_role(ROLE_ID)
        if not role:
            print(f"❌ Role ID {ROLE_ID} not found.")
            return

        # Filter eligible members
        eligible_members = [
            m for m in guild.members if not m.bot and role not in m.roles
        ]

        if eligible_members:
            chosen = random.choice(eligible_members)
            await chosen.add_roles(role)

            embed = discord.Embed(
                title="SECRET ROLE FOUND.",
                description=f"{chosen.mention} has found the Secret Role! {EMOJI}",
                colour=discord.Colour.gold()
            )
            await message.channel.send(embed=embed)
        else:
            print("⚠️ No eligible members found.")

    await bot.process_commands(message)
