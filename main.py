import os
import discord
from discord.ext import commands

TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None:
    raise ValueError("BOT_TOKEN not set in environment variables")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_NAME = "Member"
RULES_CHANNEL_NAME = "rules"

# ------------------------
# BUTTON VIEW (PERSISTENT)
# ------------------------
class RulesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="I Agree to the Rules",
        style=discord.ButtonStyle.green,
        custom_id="agree_rules_button"
    )
    async def agree(self, interaction: discord.Interaction, button: discord.ui.Button):

        role = discord.utils.get(interaction.guild.roles, name=ROLE_NAME)

        if role is None:
            await interaction.response.send_message(
                "❌ Member role not found. Ask an admin.",
                ephemeral=True
            )
            return

        if role in interaction.user.roles:
            await interaction.response.send_message(
                "You already have access 👍",
                ephemeral=True
            )
            return

        await interaction.user.add_roles(role)

        await interaction.response.send_message(
            "✅ Verified! You now have access to the server.",
            ephemeral=True
        )

# ------------------------
# BOT READY
# ------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Keeps button working after restarts
    bot.add_view(RulesView())

# ------------------------
# POST RULES MESSAGE (MANUAL SETUP)
# ------------------------
@bot.command()
async def postrules(ctx):
    """Run once in #rules channel to create the verification message"""
    await ctx.send(
        "📜 **Server Rules**\n\n"
        "1. Be respectful\n"
        "2. Dive safe\n"
        "3. No unsafe behaviour\n\n"
        "Click below to get access:",
        view=RulesView()
    )

# ------------------------
# OPTIONAL: WELCOME MESSAGE
# ------------------------
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")

    if channel:
        await channel.send(
            f"👋 Welcome {member.mention}!\n"
            "Please read #rules and click the button there to get access."
        )

# ------------------------
# RUN BOT
# ------------------------
bot.run(TOKEN)
