import os
import discord
from discord.ext import commands

# ----------------------------
# 1. LOAD TOKEN SAFELY
# ----------------------------
TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None:
    raise ValueError("BOT_TOKEN environment variable not set!")

# ----------------------------
# 2. INTENTS
# ----------------------------
intents = discord.Intents.default()
intents.members = True

# ----------------------------
# 3. BOT SETUP
# ----------------------------
bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------
# 4. CONFIG
# ----------------------------
ROLE_NAME = "Member"

# ----------------------------
# 5. BUTTON VIEW
# ----------------------------
class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="I Agree to the Rules",
        style=discord.ButtonStyle.green,
        custom_id="verify_button"  # IMPORTANT: persistent button ID
    )
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):

        role = discord.utils.get(interaction.guild.roles, name=ROLE_NAME)

        if role is None:
            await interaction.response.send_message(
                "❌ Role not found. Ask an admin.",
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
            "✅ Access granted. Welcome aboard!",
            ephemeral=True
        )

# ----------------------------
# 6. READY EVENT
# ----------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # This makes buttons survive restarts (VERY important for Railway)
    bot.add_view(VerifyView())

# ----------------------------
# 7. COMMAND TO POST RULES MESSAGE
# ----------------------------
@bot.command()
async def rules(ctx):
    view = VerifyView()

    await ctx.send(
        "📜 **Server Rules**\n\n"
        "1. Be respectful\n"
        "2. Dive safe\n"
        "3. No reckless ascents (in chat or water 😄)\n\n"
        "Click below to get access:",
        view=view
    )

# ----------------------------
# 8. RUN BOT
# ----------------------------
bot.run(TOKEN)
