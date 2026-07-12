import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import datetime
import aiohttp
import io
import os
from urllib.parse import urlparse

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
        await interaction.response.send_message("⛔ Access denied.", ephemeral=True)
        return False
    return True

# ---------- TROLLING MESSAGE (unique) ----------
TROLL_MSG = "🔹 Trolling sequence initiated..."

# ---------- RAID TEXT ----------
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

# ---------- NSFW URLS FROM TEXT FILE (fallback to hardcoded) ----------
NSFW_URLS = []
try:
    # Try to read from nsfw.txt in the same directory
    if os.path.exists("nsfw.txt"):
        with open("nsfw.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip()]
            if lines:
                NSFW_URLS = lines
except:
    pass

# If no file, fallback to a small set of safe-for-work placeholder images (just to avoid errors)
# But we want NSFW, so we'll keep a small set of public domain NSFW-ish images (actually we can use the API as fallback)
# We'll combine: try to use URLs from file, else use waifu.pics API.
def get_nsfw_urls(count=5):
    if NSFW_URLS:
        # Pick random URLs from the list
        return random.sample(NSFW_URLS, min(count, len(NSFW_URLS)))
    else:
        # Fallback: use waifu.pics API (may still work)
        return None  # will be handled in command

# ---------- VIEWS ----------
class RaidView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="☠️ RAID", style=discord.ButtonStyle.danger, custom_id="raid_button")
    async def raid_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        is_dm = interaction.guild is None
        can_send = True
        can_mention_everyone = False

        if not is_dm:
            perms = interaction.channel.permissions_for(interaction.guild.me)
            can_send = perms.send_messages
            can_mention_everyone = perms.mention_everyone

        if not can_send:
            await interaction.followup.send("❌ I can't send messages here.", ephemeral=True)
            return

        # Send the public raid messages
        for _ in range(5):
            if is_dm:
                await interaction.channel.send(RAID_TEXT)
            else:
                if can_mention_everyone:
                    await interaction.channel.send(content="@everyone\n" + RAID_TEXT)
                else:
                    await interaction.channel.send(RAID_TEXT)
            await asyncio.sleep(0.4)

        # Unique ephemeral confirmation
        embed = discord.Embed(
            title="⬛ RAID EXECUTED",
            description="Your raid was delivered successfully.\nNobody else knows it was you.",
            color=discord.Color.dark_red()
        )
        embed.set_footer(text="Classified – Exilon Operations")
        await interaction.followup.send(embed=embed, ephemeral=True)

    @discord.ui.button(label="🔄 EXTRA", style=discord.ButtonStyle.secondary, custom_id="extra_button")
    async def extra_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Opens a new ephemeral raid panel
        embed = discord.Embed(
            title="☠️ RAID PANEL",
            description="Use the buttons below.\nThis panel is only visible to you.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Exilon | Stealth Mode")
        view = RaidView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class NitroAcceptView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success, custom_id="nitro_accept")
    async def nitro_accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"HAHA EZ U FELL FOR THIS LOL JOIN {interaction.user.mention}\nhttps://discord.gg/BjtRhW6VHN",
            ephemeral=False
        )

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged as {bot.user}")

# ---------- FREE COMMANDS (with trolling ephemeral) ----------
@bot.tree.command(name="raid", description="[🆓] Open stealth raid panel")
async def raid(interaction: discord.Interaction):
    if not await blacklist_check(interaction): return
    # Send trolling ephemeral first
    await interaction.response.send_message(TROLL_MSG, ephemeral=True)
    # Then send the panel as follow-up (ephemeral)
    embed = discord.Embed(
        title="☠️ RAID PANEL",
        description="Use the buttons below.\nThis panel is only visible to you.",
        color=discord.Color.red()
    )
    embed.set_footer(text="Exilon | Stealth Mode")
    view = RaidView()
    await interaction.followup.send(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="blame", description="[🆓] Blame a specific user")
@app_commands.describe(user="The user to blame")
async def blame(interaction: discord.Interaction, user: discord.Member):
    if not await blacklist_check(interaction): return
    await interaction.response.send_message(TROLL_MSG, ephemeral=True)
    msg = get_blame_message(user)
    await interaction.followup.send(msg)

@bot.tree.command(name="ip", description="[🆓] Fake intrusion alert")
@app_commands.describe(user="Target user")
async def ip(interaction: discord.Interaction, user: discord.Member):
    if not await blacklist_check(interaction): return
    await interaction.response.send_message(TROLL_MSG, ephemeral=True)
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
    embed.set_footer(text="Simulated alert – no real data.")
    await interaction.followup.send(content=user.mention, embed=embed)

@bot.tree.command(name="say", description="[🆓] Make bot say something")
@app_commands.describe(message="Text to say")
async def say(interaction: discord.Interaction, message: str):
    if not await blacklist_check(interaction): return
    await interaction.response.send_message(TROLL_MSG, ephemeral=True)
    await interaction.followup.send(message)

@bot.tree.command(name="nitro", description="[🆓] Fake Nitro gift")
@app_commands.describe(user="(Optional) Target user")
async def nitro(interaction: discord.Interaction, user: discord.Member = None):
    if not await blacklist_check(interaction): return
    await interaction.response.send_message(TROLL_MSG, ephemeral=True)
    target = user if user else interaction.user
    embed = discord.Embed(
        title="You've been gifted a subscription!",
        description=f"@{target.display_name} You Only Have 72h to earn it!",
        color=discord.Color.gold()
    )
    embed.set_image(url="https://refillarena.com/_next/image?url=https%3A%2F%2Frefillarena.s3.amazonaws.com%2Fdiscord+nitro.png&w=640&q=75")
    view = NitroAcceptView()
    await interaction.followup.send(content=target.mention, embed=embed, view=view)

@bot.tree.command(name="checkraid", description="[🆓] Flash invite link")
async def checkraid(interaction: discord.Interaction):
    if not await blacklist_check(interaction): return
    await interaction.response.send_message(TROLL_MSG, ephemeral=True)
    await interaction.followup.send("https://discord.gg/BjtRhW6VHN", ephemeral=False)
    msg = await interaction.original_response()
    await asyncio.sleep(1)
    await msg.delete()
    # Also send ephemeral confirmation
    await interaction.followup.send("✅ Link flashed.", ephemeral=True)

@bot.tree.command(name="ad", description="[🆓] Show Exilon ad")
async def ad(interaction: discord.Interaction):
    if not await blacklist_check(interaction): return
    await interaction.response.send_message(TROLL_MSG, ephemeral=True)
    await interaction.followup.send(AD_TEXT)

# ---------- PREMIUM MANAGEMENT (owner only, no trolling needed) ----------
@bot.tree.command(name="addpremium", description="[🔒] Grant premium (owner only)")
@app_commands.describe(user="User to grant")
async def addpremium(interaction: discord.Interaction, user: discord.Member):
    if not is_owner(interaction):
        await interaction.response.send_message("❌ Owner only.", ephemeral=True)
        return
    if user.id in PREMIUM_USERS:
        await interaction.response.send_message(f"{user.mention} already has premium.", ephemeral=False)
        return
    PREMIUM_USERS.append(user.id)
    await interaction.response.send_message(f"{user.mention} [💎] Premium granted.", ephemeral=False)

@bot.tree.command(name="removepremium", description="[🔒] Remove premium (owner only)")
@app_commands.describe(user="User to remove")
async def removepremium(interaction: discord.Interaction, user: discord.Member):
    if not is_owner(interaction):
        await interaction.response.send_message("❌ Owner only.", ephemeral=True)
        return
    if user.id not in PREMIUM_USERS:
        await interaction.response.send_message(f"{user.mention} not premium.", ephemeral=False)
        return
    PREMIUM_USERS.remove(user.id)
    await interaction.response.send_message(f"{user.mention} [💎] Premium revoked.", ephemeral=False)

@bot.tree.command(name="blacklist", description="[🔒] Blacklist user (owner only)")
@app_commands.describe(user="User to blacklist")
async def blacklist(interaction: discord.Interaction, user: discord.Member):
    if not is_owner(interaction):
        await interaction.response.send_message("❌ Owner only.", ephemeral=True)
        return
    if user.id in BLACKLIST:
        await interaction.response.send_message(f"{user.mention} already blacklisted.", ephemeral=False)
        return
    BLACKLIST.append(user.id)
    await interaction.response.send_message(f"{user.mention} blacklisted.", ephemeral=False)

@bot.tree.command(name="unblacklist", description="[🔒] Unblacklist user (owner only)")
@app_commands.describe(user="User to unblacklist")
async def unblacklist(interaction: discord.Interaction, user: discord.Member):
    if not is_owner(interaction):
        await interaction.response.send_message("❌ Owner only.", ephemeral=True)
        return
    if user.id not in BLACKLIST:
        await interaction.response.send_message(f"{user.mention} not blacklisted.", ephemeral=False)
        return
    BLACKLIST.remove(user.id)
    await interaction.response.send_message(f"{user.mention} unblacklisted.", ephemeral=False)

# ---------- PREMIUM COMMANDS (with trolling ephemeral) ----------
@bot.tree.command(name="spam", description="[💎] Send custom message multiple times")
@app_commands.describe(message="Message", total="Times (1-5)")
async def spam(interaction: discord.Interaction, message: str, total: int):
    if not await blacklist_check(interaction): return
    if not is_premium(interaction):
        await interaction.response.send_message("❌ Premium only.", ephemeral=True)
        return
    if total > 5 or total < 1:
        await interaction.response.send_message("❌ Total 1-5.", ephemeral=True)
        return
    await interaction.response.send_message(TROLL_MSG, ephemeral=True)
    await interaction.followup.defer(ephemeral=False)  # we want public messages
    for _ in range(total):
        await interaction.channel.send(message)
        await asyncio.sleep(0.5)
    await interaction.followup.send(f"✅ Sent {total} times.", ephemeral=True)

@bot.tree.command(name="nsfw", description="[💎] Send 5 NSFW images")
async def nsfw(interaction: discord.Interaction):
    if not await blacklist_check(interaction): return
    if not is_premium(interaction):
        await interaction.response.send_message("❌ Premium only.", ephemeral=True)
        return

    await interaction.response.send_message(TROLL_MSG, ephemeral=True)
    await interaction.followup.defer(ephemeral=False)

    # Try to get URLs from file, else use API
    urls = get_nsfw_urls(5)
    if urls:
        for i, url in enumerate(urls):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        if resp.status != 200:
                            await interaction.followup.send(f"⚠️ Failed to fetch image {i+1}.", ephemeral=False)
                            continue
                        img_data = await resp.read()
                ext = url.split('.')[-1].split('?')[0]
                if ext.lower() not in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
                    ext = 'png'
                file = discord.File(io.BytesIO(img_data), filename=f"nsfw_{i+1}.{ext}")
                await interaction.followup.send(file=file)
                await asyncio.sleep(0.3)
            except:
                await interaction.followup.send(f"⚠️ Error on image {i+1}.", ephemeral=False)
    else:
        # Fallback to waifu.pics API
        APIs = [
            "https://api.waifu.pics/nsfw/waifu",
            "https://api.waifu.pics/nsfw/neko",
            "https://api.waifu.pics/nsfw/trap"
        ]
        for attempt in range(5):
            success = False
            for api in APIs:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(api) as resp:
                            if resp.status != 200:
                                continue
                            data = await resp.json()
                            image_url = data.get("url")
                            if not image_url:
                                continue
                            async with session.get(image_url) as img_resp:
                                if img_resp.status != 200:
                                    continue
                                img_data = await img_resp.read()
                            ext = image_url.split('.')[-1].split('?')[0]
                            if ext.lower() not in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
                                ext = 'png'
                            file = discord.File(io.BytesIO(img_data), filename=f"nsfw_{attempt+1}.{ext}")
                            await interaction.followup.send(file=file)
                            success = True
                            break
                except:
                    continue
            if not success:
                await interaction.followup.send(f"⚠️ Failed attempt {attempt+1}.", ephemeral=False)
            await asyncio.sleep(0.3)

bot.run(os.getenv("DISCORD_TOKEN"))
