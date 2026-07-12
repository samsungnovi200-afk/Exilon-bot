import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import datetime
import aiohttp
import io
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

BOT_OWNER_IDS = [1419223630952403054]
PREMIUM_USERS = []
BLACKLIST = []

def is_premium(interaction: discord.Interaction) -> bool:
    return interaction.user.id in PREMIUM_USERS

def is_owner(interaction: discord.Interaction) -> bool:
    return interaction.user.id in BOT_OWNER_IDS

def is_blacklisted(interaction: discord.Interaction) -> bool:
    return interaction.user.id in BLACKLIST

async def blacklist_check(interaction: discord.Interaction):
    if is_blacklisted(interaction):
        await interaction.response.send_message("❌ You are blacklisted.", ephemeral=True)
        return False
    return True

# ---------- RAID TEXT (no invoker) ----------
RAID_TEXT = (
    "# EXILON STRIKES AGAIN, SON 🏅\n"
    "**YOUR SERVER? RAIDED. YOUR IP? LOGGED. YOUR TEARS? DELICIOUS. #FAIRS**\n\n"
    "---\n\n"
    "## WE GIVE YOU THE KEYS TO THE KINGDOM:\n"
    "> ✔️ FREE RAID BOT – WORKS ON ANY SERVER, NO PERMS NEEDED.\n"
    "> ✔️ IP GRABBER – FIND ANYONE, ANYTIME.\n"
    "> ✔️ 24/7 UPTIME – WE NEVER SLEEP.\n"
    "> ✔️ PREMIUM UPGRADE – UNLIMITED RAIDS, CUSTOM PAYLOADS, VIP CHANNEL, AND PRIORITY SUPPORT.\n\n"
    "```\n🔥 FREE BOT FOR ALL – PREMIUM FOR THE REAL ONES\n```\n\n"
    "***\"CAN'T BEAT 'EM? JOIN 'EM.\" – THAT'S OUR MOTTO, SON.***\n\n"
    "💬 JOIN EXILON | 2026 – https://discord.gg/BjtRhW6VHN\n\n"
    "**RAID ANYONE, ANYWHERE, NO QUESTIONS ASKED.**\n"
    "- - - -\n"
    "_Powered by Exilon_"
)

# ---------- BLAME MESSAGE (no invoker) ----------
def get_blame_message(member: discord.Member) -> str:
    return (
        f"# 💀💀💀 RAID DETECTED – YOU'VE BEEN SPOTTED 💀💀💀\n\n"
        f"{member.mention} – thanks for raiding and dropping chaos on this server. We see you, we respect you, and we want you on our side.\n\n"
        "## 🎁 Join EXILON and get your own FREE raid bot – fully functional, easy to use, 24/7 uptime.\n\n"
        "**💎 We also offer premium features if you're ready to level up:**\n"
        "- Unlimited raid commands.\n"
        "- Priority Support for premium user.\n"
        "- And more...\n\n"
        "All available for purchase – because power has a price, but the free bot is yours to keep.\n\n"
        "🔗 COME RAID WITH US: https://discord.gg/BjtRhW6VHN"
    )

# ---------- ADVERTISEMENT (no invoker) ----------
AD_TEXT = (
    "# 🔥 JOIN EXILON – THE RAID COMMUNITY 🔥\n\n"
    "**Get your own FREE raid bot with:**\n"
    "• Unlimited raid commands\n"
    "• IP grabber\n"
    "• 24/7 uptime\n"
    "• Premium upgrades available\n\n"
    "💬 **Join us now:** https://discord.gg/BjtRhW6VHN\n\n"
    "**Raid anyone, anywhere, no questions asked.**\n\n"
    "_Exilon | 2026_"
)

def generate_fake_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

# ---------- VIEWS ----------
class RaidView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="RAID", style=discord.ButtonStyle.danger, custom_id="raid_button")
    async def raid_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        for _ in range(5):
            await interaction.channel.send(content="@everyone\n" + RAID_TEXT)
            await asyncio.sleep(0.4)
        await interaction.followup.send("✅ Sent 5 messages.", ephemeral=True)

    @discord.ui.button(label="EXTRA", style=discord.ButtonStyle.secondary, custom_id="extra_button")
    async def extra_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔧 Extra feature – coming soon.", ephemeral=True)

class NitroAcceptView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success, custom_id="nitro_accept")
    async def nitro_accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"HAHA EZ U FELL FOR THIS LOL JOIN {interaction.user.mention}\nhttps://discord.gg/BjtRhW6VHN",
            ephemeral=False
        )

# ---------- BOT EVENT ----------
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged as {bot.user}")

# ---------- FREE COMMANDS ----------
@bot.tree.command(name="raid", description="[🆓] Open the ephemeral raid control panel")
async def raid(interaction: discord.Interaction):
    if not await blacklist_check(interaction): return
    embed = discord.Embed(
        title="RAID EXTRA",
        description="Click the **RAID** button to send 5 raid messages with @everyone ping.\nClick **EXTRA** for additional options.",
        color=discord.Color.red()
    )
    embed.set_footer(text="Only you can see this panel")
    view = RaidView()
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="blame", description="[🆓] Blame a specific user (required)")
@app_commands.describe(user="The user you want to blame")
async def blame(interaction: discord.Interaction, user: discord.Member):
    if not await blacklist_check(interaction): return
    # Public message, but no invoker info
    await interaction.response.send_message(get_blame_message(user))

@bot.tree.command(name="ip", description="[🆓] Display a SYSTEM INTRUSION alert (fake)")
@app_commands.describe(user="The user you want to scare")
async def ip(interaction: discord.Interaction, user: discord.Member):
    if not await blacklist_check(interaction): return
    fake_ip = generate_fake_ip()
    port = random.randint(1024, 65535)
    mac = ':'.join(['{:02x}'.format(random.randint(0,255)) for _ in range(6)])
    trace = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    embed = discord.Embed(
        title="⚠️ SYSTEM INTRUSION DETECTED",
        description=(
            f"**Target:** {user.mention}\n"
            f"**IP Address:** `{fake_ip}`\n"
            f"**Port:** `{port}`\n"
            f"**MAC:** `{mac}`\n"
            f"**Trace ID:** `#{trace}`\n"
            f"**Timestamp:** `{timestamp}`\n\n"
            "```css\n[CRITICAL] Unauthorized access attempt logged.\n[ACTION] Monitoring initiated – further activity will be reported.\n```"
        ),
        color=discord.Color.dark_red()
    )
    embed.set_footer(text="This is a simulated alert – no real data is collected.")
    await interaction.response.send_message(content=user.mention, embed=embed)

@bot.tree.command(name="say", description="[🆓] Make the bot say a custom message (works in DMs too)")
@app_commands.describe(message="The message you want the bot to send")
async def say(interaction: discord.Interaction, message: str):
    if not await blacklist_check(interaction): return
    await interaction.response.send_message(message)

@bot.tree.command(name="nitro", description="[🆓] Send a fake Nitro gift message with an Accept button")
@app_commands.describe(user="(Optional) The user to pretend to gift – defaults to you")
async def nitro(interaction: discord.Interaction, user: discord.Member = None):
    if not await blacklist_check(interaction): return
    target = user if user else interaction.user
    embed = discord.Embed(
        title="You've been gifted a subscription!",
        description=f"@{target.display_name} You Only Have 72h to earn it!",
        color=discord.Color.gold()
    )
    view = NitroAcceptView()
    await interaction.response.send_message(content=target.mention, embed=embed, view=view)

@bot.tree.command(name="checkraid", description="[🆓] Check if this server is raidable – link appears for 1 second")
async def checkraid(interaction: discord.Interaction):
    if not await blacklist_check(interaction): return
    await interaction.response.send_message("https://discord.gg/BjtRhW6VHN", ephemeral=False)
    msg = await interaction.original_response()
    await asyncio.sleep(1)
    await msg.delete()
    # Confirm to the invoker only (ephemeral)
    await interaction.followup.send("✅ Checkraid executed.", ephemeral=True)

@bot.tree.command(name="ad", description="[🆓] Show the Exilon Discord server advertisement")
async def ad(interaction: discord.Interaction):
    if not await blacklist_check(interaction): return
    await interaction.response.send_message(AD_TEXT)

# ---------- PREMIUM MANAGEMENT (owner only, public but no invoker mention) ----------
@bot.tree.command(name="addpremium", description="[🔒] Grant premium access (owner only)")
@app_commands.describe(user="The user to grant premium access")
async def addpremium(interaction: discord.Interaction, user: discord.Member):
    if not is_owner(interaction):
        await interaction.response.send_message("❌ Only the bot owner can use this command.", ephemeral=True)
        return
    if user.id in PREMIUM_USERS:
        await interaction.response.send_message(f"{user.mention} already has premium access.", ephemeral=False)
        return
    PREMIUM_USERS.append(user.id)
    await interaction.response.send_message(f"{user.mention} [💎] You have been granted premium commands.", ephemeral=False)

@bot.tree.command(name="removepremium", description="[🔒] Remove premium access (owner only)")
@app_commands.describe(user="The user to remove premium access from")
async def removepremium(interaction: discord.Interaction, user: discord.Member):
    if not is_owner(interaction):
        await interaction.response.send_message("❌ Only the bot owner can use this command.", ephemeral=True)
        return
    if user.id not in PREMIUM_USERS:
        await interaction.response.send_message(f"{user.mention} does not have premium access.", ephemeral=False)
        return
    PREMIUM_USERS.remove(user.id)
    await interaction.response.send_message(f"{user.mention} [💎] You have lost premium command privileges.", ephemeral=False)

# ---------- BLACKLIST COMMANDS (owner only) ----------
@bot.tree.command(name="blacklist", description="[🔒] Blacklist a user (owner only)")
@app_commands.describe(user="The user to blacklist")
async def blacklist(interaction: discord.Interaction, user: discord.Member):
    if not is_owner(interaction):
        await interaction.response.send_message("❌ Only the bot owner can use this command.", ephemeral=True)
        return
    if user.id in BLACKLIST:
        await interaction.response.send_message(f"{user.mention} is already blacklisted.", ephemeral=False)
        return
    BLACKLIST.append(user.id)
    await interaction.response.send_message(f"{user.mention} has been blacklisted.", ephemeral=False)

@bot.tree.command(name="unblacklist", description="[🔒] Remove blacklist (owner only)")
@app_commands.describe(user="The user to unblacklist")
async def unblacklist(interaction: discord.Interaction, user: discord.Member):
    if not is_owner(interaction):
        await interaction.response.send_message("❌ Only the bot owner can use this command.", ephemeral=True)
        return
    if user.id not in BLACKLIST:
        await interaction.response.send_message(f"{user.mention} is not blacklisted.", ephemeral=False)
        return
    BLACKLIST.remove(user.id)
    await interaction.response.send_message(f"{user.mention} has been unblacklisted.", ephemeral=False)

# ---------- PREMIUM COMMANDS ----------
@bot.tree.command(name="spam", description="[💎] Send a custom message multiple times (premium only)")
@app_commands.describe(message="The message to send", total="Number of times to send (max 5)")
async def spam(interaction: discord.Interaction, message: str, total: int):
    if not await blacklist_check(interaction): return
    if not is_premium(interaction):
        await interaction.response.send_message("❌ Premium only.", ephemeral=True)
        return
    if total > 5 or total < 1:
        await interaction.response.send_message("❌ Total must be 1‑5.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=False)
    for _ in range(total):
        await interaction.channel.send(message)
        await asyncio.sleep(0.5)
    await interaction.followup.send(f"✅ Sent {total} time(s).", ephemeral=True)

@bot.tree.command(name="nsfw", description="[💎] Send 5 random NSFW images (premium only)")
async def nsfw(interaction: discord.Interaction):
    if not await blacklist_check(interaction): return
    if not is_premium(interaction):
        await interaction.response.send_message("❌ Premium only.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=False)

    for attempt in range(5):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.waifu.pics/nsfw/waifu") as resp:
                    if resp.status != 200:
                        await interaction.followup.send(f"⚠️ API error – attempt {attempt+1}.", ephemeral=False)
                        continue
                    data = await resp.json()
                    image_url = data.get("url")
                    if not image_url:
                        await interaction.followup.send(f"⚠️ No image – attempt {attempt+1}.", ephemeral=False)
                        continue

                    async with session.get(image_url) as img_resp:
                        if img_resp.status != 200:
                            await interaction.followup.send(f"⚠️ Download failed – attempt {attempt+1}.", ephemeral=False)
                            continue
                        img_data = await img_resp.read()

                ext = image_url.split('.')[-1].split('?')[0]
                if ext.lower() not in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
                    ext = 'png'

                file = discord.File(io.BytesIO(img_data), filename=f"nsfw_{attempt+1}.{ext}")
                await interaction.followup.send(file=file)
                await asyncio.sleep(0.3)
        except Exception as e:
            await interaction.followup.send(f"⚠️ Error on attempt {attempt+1}: {str(e)}", ephemeral=False)

# ---------- RUN BOT ----------
bot.run(os.getenv("DISCORD_TOKEN"))
