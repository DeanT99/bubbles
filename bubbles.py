import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_NAME = "Member"

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="I Agree to the Rules", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name=ROLE_NAME)

        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ You now have access. Welcome!", ephemeral=True)
        else:
            await interaction.response.send_message("Role not found.", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.add_view(VerifyView())  # keeps buttons working after restart

@bot.command()
async def send_rules(ctx):
    view = VerifyView()
    await ctx.send(
        "📜 **Server Rules**\n\n"
        "1. Don't be a muppet\n"
        "2. Dive safe\n"
        "3. No unsafe ascents (including in chat)\n\n"
        "Click below to get access:",
        view=view
    )

bot.run("YOUR_BOT_TOKEN")
