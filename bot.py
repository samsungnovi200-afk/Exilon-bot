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

guild_settings = {}
user_messages = {}

TROLL_MSG = "🔹 Trolling sequence initiated..."

RAID_TEMPLATE = (
    "# {server_name} STRIKES AGAIN, SON 🏅\n"
    "YOUR SERVER? RAIDED. YOUR IP? LOGGED. YOUR TEARS? DELICIOUS. #FAIRS\n\n"
    "---\n\n"
    "## WE GIVE YOU THE KEYS TO THE KINGDOM:\n"
    "> ✔️ FREE RAID BOT – WORKS ON ANY SERVER, NO PERMS NEEDED.\n"
    "> ✔️ IP GRABBER – FIND ANYONE, ANYTIME.\n"
    "> ✔️ 24/7 UPTIME – WE NEVER SLEEP.\n"
    "> ✔️ PREMIUM UPGRADE – UNLIMITED RAIDS, CUSTOM PAYLOADS, VIP CHANNEL, AND PRIORITY SUPPORT.\n\n"
    "```\n🔥 FREE BOT FOR ALL – PREMIUM FOR THE REAL ONES\n```\n\n"
    "\"CAN'T BEAT 'EM? JOIN 'EM.\" – THAT'S OUR MOTTO, SON.\n\n"
    "💬 JOIN {server_name} | 2026 – {server_link}\n\n"
    "RAID ANYONE, ANYWHERE, NO QUESTIONS ASKED.\n"
    "- - - -\n"
    "_Powered by Exilon_"
)

def get_raid_text(guild_id):
    settings = guild_settings.get(guild_id, {})
    name = settings.get("name", "EXILON")
    link = settings.get("link", "https://discord.gg/BjtRhW6VHN")
    return RAID_TEMPLATE.format(server_name=name, server_link=link)

CUNEIFORM_MSG = "# " + "𒅒𒈔𒅒𒇫𒄆" * 100 + "\n\nJoin our server: https://discord.gg/BjtRhW6VHN"

def blame_message(member: discord.Member) -> str:
    return (
        f"# 💀💀💀 RAID DETECTED – YOU'VE BEEN SPOTTED 💀💀💀\n\n"
        f"{member.mention} – thanks for raiding and dropping chaos on this server. We see you, we respect you, and we want you on our side.\n\n"
        "## 🎁 Join EXILON and get your own FREE raid bot – fully functional, easy to use, 24/7 uptime.\n\n"
        "We also offer premium features if you're ready to level up:\n"
        "- Unlimited raid commands.\n"
        "- Priority Support for premium user.\n"
        "- And more...\n\n"
        "All available for purchase – because power has a price, but the free bot is yours to keep.\n\n"
        "🔗 COME RAID WITH US: https://discord.gg/BjtRhW6VHN"
    )

AD_TEXT = (
    "# 🔥 JOIN EXILON – THE RAID COMMUNITY 🔥\n\n"
    "Get your own FREE raid bot with:\n"
    "• Unlimited raid commands\n"
    "• IP grabber\n"
    "• 24/7 uptime\n"
    "• Premium upgrades available\n\n"
    "💬 Join us now: https://discord.gg/BjtRhW6VHN\n\n"
    "Raid anyone, anywhere, no questions asked.\n\n"
    "_Exilon | 2026_"
)

def generate_fake_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

# ---------- NSFW: ONLY FROM .TXT, NO API ----------
NSFW_URLS = []
if os.path.exists("nsfw.txt"):
    with open("nsfw.txt", "r") as f:
        NSFW_URLS = [line.strip() for line in f if line.strip()]

def get_nsfw_urls():
    if NSFW_URLS:
        return random.sample(NSFW_URLS, min(5, len(NSFW_URLS)))
    return None

USER_TOKEN = os.getenv("USER_TOKEN")

class RaidView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="☠️ RAID", style=discord.ButtonStyle.danger, custom_id="raid_button")
    async def raid_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        channel = interaction.channel
        guild = interaction.guild
        guild_id = guild.id if guild else None
        raid_text = get_raid_text(guild_id) if guild_id else get_raid_text(None)

        if guild and guild.me:
            try:
                for _ in range(5):
                    await channel.send(raid_text)
                    await asyncio.sleep(0.5)
                await channel.send(CUNEIFORM_MSG)
                await interaction.followup.send("✅ Raid executed (as bot)!", ephemeral=True)
                return
            except discord.Forbidden:
                await interaction.followup.send("❌ Bot lacks permission to send messages here.", ephemeral=True)
                return
            except Exception as e:
                await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)
                return

        if not USER_TOKEN:
            await interaction.followup.send("❌ USER_TOKEN not set and bot not in server.", ephemeral=True)
            return

        headers = {
            "Authorization": USER_TOKEN,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        channel_id = channel.id

        async with aiohttp.ClientSession() as session:
            for i in range(5):
                payload = {"content": raid_text, "allowed_mentions": {"parse": ["everyone"]}}
                try:
                    async with session.post(
                        f"https://discord.com/api/v9/channels/{channel_id}/messages",
                        json=payload,
                        headers=headers
                    ) as resp:
                        if resp.status != 200:
                            error_text = await resp.text()
                            await interaction.followup.send(
                                f"⚠️ Failed on attempt {i+1} (HTTP {resp.status})\nReason: {error_text[:300]}",
                                ephemeral=True
                            )
                            return
                except Exception as e:
                    await interaction.followup.send(f"⚠️ Request error: {str(e)}", ephemeral=True)
                    return
                await asyncio.sleep(0.5)

            payload = {"content": CUNEIFORM_MSG, "allowed_mentions": {"parse": ["everyone"]}}
            try:
                async with session.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/messages",
                    json=payload,
                    headers=headers
                ) as resp:
                    if resp.status != 200:
                        error_text = await resp.text()
                        await interaction.followup.send(
                            f"⚠️ Failed to send cuneiform (HTTP {resp.status})\nReason: {error_text[:300]}",
                            ephemeral=True
                        )
                        return
            except Exception as e:
                await interaction.followup.send(f"⚠️ Request error: {str(e)}", ephemeral=True)
                return

        await interaction.followup.send("✅ Raid executed (using user token)!", ephemeral=True)

    @discord.ui.button(label="🔄 EXTRA", style=discord.ButtonStyle.secondary, custom_id="extra_button")
    async def extra_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(
            title="☠️ RAID PANEL",
            description="Click **RAID** to send 5 messages + cuneiform spam.\nClick **EXTRA** for another panel.",
            color=discord.Color.red()
        ).set_footer(text="Exilon | Stealth Mode")
        view = RaidView()
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)

class NitroAcceptView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success, custom_id="nitro_accept")
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"HAHA EZ U FELL FOR THIS LOL JOIN {interaction.user.mention}\nhttps://discord.gg/BjtRhW6VHN",
            ephemeral=False
        )

def is_owner(interaction: discord.Interaction) -> bool:
    return interaction.user.id in BOT_OWNER_IDS

def is_premium(interaction: discord.Interaction) -> bool:
    return interaction.user.id in PREMIUM_USERS

async def blacklist_check(interaction: discord.Interaction) -> bool:
    if interaction.user.id in BLACKLIST:
        await interaction.response.send_message("⛔ Access denied.", ephemeral=True)
        return False
    return True

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged as {bot.user}")

# ---------- FREE COMMANDS ----------
@bot.tree.command(name="raid", description="[🆓] Open stealth raid panel")
async def raid_command(interaction: discord.Interaction):
    if not await blacklist_check(interaction): return
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(TROLL_MSG, ephemeral=True)
    embed = discord.Embed(
        title="☠️ RAID PANEL",
        description="Click **RAID** to send 5 messages + cuneiform spam.\nClick **EXTRA** for another panel.",
        color=discord.Color.red()
    ).set_footer(text="Exilon | Stealth Mode")
    view = RaidView()
    await interaction.followup.send(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="blame", description="[🆓] Blame a user")
@app_commands.describe(user="Target user")
async def blame(interaction: discord.Interaction, user: discord.Member):
    if not await blacklist_check(interaction): return
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(TROLL_MSG, ephemeral=True)
    await interaction.followup.send(blame_message(user))

@bot.tree.command(name="ip", description="[🆓] Fake intrusion alert")
@app_commands.describe(user="Target user")
async def ip(interaction: discord.Interaction, user: discord.Member):
    if not await blacklist_check(interaction): return
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(TROLL_MSG, ephemeral=True)

    fake_ip = generate_fake_ip()
    port = random.randint(1024, 65535)
    mac = ':'.join(['{:02x}'.format(random.randint(0,255)) for _ in range(6)])
    trace = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    embed = discord.Embed(
        title="⚠️ SYSTEM INTRUSION DETECTED",
        description=(
            f"Target: {user.mention}\n"
            f"IP Address: `{fake_ip}`\n"
            f"Port: `{port}`\n"
            f"MAC: `{mac}`\n"
            f"Trace ID: `#{trace}`\n"
            f"Timestamp: `{timestamp}`\n\n"
            "```css\n[CRITICAL] Unauthorized access attempt logged.\n"
            "[ACTION] Monitoring initiated – further activity will be reported.\n```"
        ),
        color=discord.Color.dark_red()
    ).set_footer(text="Simulated alert – no real data.")

    await interaction.followup.send(content=user.mention, embed=embed)

@bot.tree.command(name="say", description="[🆓] Make bot say something")
@app_commands.describe(message="Text to say")
async def say(interaction: discord.Interaction, message: str):
    if not await blacklist_check(interaction): return
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(TROLL_MSG, ephemeral=True)
    await interaction.followup.send(message)

@bot.tree.command(name="nitro", description="[🆓] Fake Nitro gift")
@app_commands.describe(user="(Optional) Target user")
async def nitro(interaction: discord.Interaction, user: discord.Member = None):
    if not await blacklist_check(interaction): return
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(TROLL_MSG, ephemeral=True)
    target = user if user else interaction.user

    embed = discord.Embed(
        title="You've been gifted a subscription!",
        description=f"@{target.display_name} You Only Have 72h to earn it!",
        color=discord.Color.gold()
    ).set_image(
        url="https://refillarena.com/_next/image?url=https%3A%2F%2Frefillarena.s3.amazonaws.com%2Fdiscord+nitro.png&w=640&q=75"
    )

    view = NitroAcceptView()
    await interaction.followup.send(content=target.mention, embed=embed, view=view)

@bot.tree.command(name="checkraid", description="[🆓] Flash invite link")
async def checkraid(interaction: discord.Interaction):
    if not await blacklist_check(interaction): return
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(TROLL_MSG, ephemeral=True)
    msg = await interaction.followup.send("https://discord.gg/BjtRhW6VHN", ephemeral=False)
    await asyncio.sleep(1)
    await msg.delete()
    await interaction.followup.send("✅ Link flashed.", ephemeral=True)

@bot.tree.command(name="ad", description="[🆓] Show Exilon ad")
async def ad(interaction: discord.Interaction):
    if not await blacklist_check(interaction): return
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(TROLL_MSG, ephemeral=True)
    await interaction.followup.send(AD_TEXT)

@bot.tree.command(name="setraidserver", description="[🆓] Set custom server name and link for raid messages")
@app_commands.describe(name="Your server name", link="Your server invite link")
async def setraidserver(interaction: discord.Interaction, name: str, link: str):
    if not await blacklist_check(interaction): return
    guild_id = interaction.guild_id
    if not guild_id:
        await interaction.response.send_message("❌ This command can only be used in a server.", ephemeral=True)
        return
    guild_settings[guild_id] = {"name": name, "link": link}
    await interaction.response.send_message(f"✅ Raid messages will now show **{name}** and link **{link}** in this server.", ephemeral=False)

# ---------- SAVE / SHOW MY MESSAGE (PREMIUM) ----------
@bot.tree.command(name="savemymessage", description="[💎] Save a custom message (premium)")
@app_commands.describe(message="Your custom message (any text)")
async def savemymessage(interaction: discord.Interaction, message: str):
    if not await blacklist_check(interaction): return
    if not is_premium(interaction):
        await interaction.response.send_message("❌ This command is premium only. Premium access is granted via purchase or giveaways.", ephemeral=True)
        return
    user_id = interaction.user.id
    user_messages[user_id] = message
    await interaction.response.send_message("✅ Your custom message has been saved!", ephemeral=True)

@bot.tree.command(name="showmymessage", description="[💎] Show your saved custom message (premium)")
async def showmymessage(interaction: discord.Interaction):
    if not await blacklist_check(interaction): return
    if not is_premium(interaction):
        await interaction.response.send_message("❌ This command is premium only. Premium access is granted via purchase or giveaways.", ephemeral=True)
        return
    user_id = interaction.user.id
    saved = user_messages.get(user_id)
    if saved is None:
        await interaction.response.send_message("❌ You haven't saved a message yet. Use `/savemymessage` first.", ephemeral=True)
        return
    await interaction.response.send_message(saved)

# ---------- OSINT (PREMIUM) ----------
@bot.tree.command(name="osint", description="[💎] Lookup IP information (premium)")
@app_commands.describe(ip="IP address to lookup")
async def osint(interaction: discord.Interaction, ip: str):
    if not await blacklist_check(interaction): return
    if not is_premium(interaction):
        await interaction.response.send_message("❌ This command is premium only. Premium access is granted via purchase or giveaways.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,mobile,proxy,hosting"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await interaction.followup.send("❌ Failed to fetch data from IP API.", ephemeral=True)
                    return
                data = await resp.json()
                if data.get("status") == "fail":
                    await interaction.followup.send(f"❌ IP lookup failed: {data.get('message', 'Unknown error')}", ephemeral=True)
                    return

                embed = discord.Embed(
                    title="🕵️ OSINT – IP Lookup Results",
                    color=discord.Color.blue()
                )
                embed.add_field(name="IP", value=ip, inline=True)
                embed.add_field(name="Country", value=data.get("country", "N/A"), inline=True)
                embed.add_field(name="Region", value=data.get("regionName", "N/A"), inline=True)
                embed.add_field(name="City", value=data.get("city", "N/A"), inline=True)
                embed.add_field(name="ZIP", value=data.get("zip", "N/A"), inline=True)
                embed.add_field(name="Coordinates", value=f"{data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}", inline=True)
                embed.add_field(name="ISP", value=data.get("isp", "N/A"), inline=False)
                embed.add_field(name="Organization", value=data.get("org", "N/A"), inline=False)
                embed.add_field(name="AS", value=data.get("as", "N/A"), inline=False)
                embed.add_field(name="Mobile", value="✅" if data.get("mobile") else "❌", inline=True)
                embed.add_field(name="Proxy", value="✅" if data.get("proxy") else "❌", inline=True)
                embed.add_field(name="Hosting", value="✅" if data.get("hosting") else "❌", inline=True)
                embed.set_footer(text="Data from ip-api.com")
                await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)

# ---------- OWNER-ONLY /tos ----------
@bot.tree.command(name="tos", description="[🔒] View Terms of Service (owner only)")
async def tos(interaction: discord.Interaction):
    if not is_owner(interaction):
        await interaction.response.send_message("❌ This command is only for the bot owner.", ephemeral=True)
        return

    embed = discord.Embed(
        title="📜 Terms of Service – Exilon Raid Bot",
        description=(
            "Last Updated: July 13, 2026\n\n"
            "By using this bot, you agree to the following terms.\n"
            "If you do not agree, do not use the bot."
        ),
        color=discord.Color.blue()
    )
    embed.add_field(
        name="1. Acceptance",
        value="This bot is provided 'as is' for entertainment and educational purposes only.\nInviting or using the bot means you accept these terms.",
        inline=False
    )
    embed.add_field(
        name="2. User Conduct",
        value="You agree NOT to use this bot for:\n• Harassment, threats, or bullying.\n• Spamming or flooding servers without permission.\n• Illegal activities or violating Discord's ToS.",
        inline=False
    )
    embed.add_field(
        name="3. Disclaimer",
        value="The bot owner is NOT liable for any consequences (e.g., account bans, server issues) arising from your use of the bot.\nUse at your own risk.",
        inline=False
    )
    embed.add_field(
        name="4. Data & Privacy",
        value="The bot does not store or collect personal data. Command usage may be logged for debugging, but no identifiable information is retained.",
        inline=False
    )
    embed.add_field(
        name="5. Changes & Termination",
        value="Terms may be updated without notice. The owner reserves the right to block any user or server from using the bot at any time.",
        inline=False
    )
    embed.add_field(
        name="6. Contact",
        value="Questions? Reach out via the support server: https://discord.gg/BjtRhW6VHN",
        inline=False
    )
    embed.set_footer(text="Exilon | 2026")
    await interaction.response.send_message(embed=embed, ephemeral=False)

# ---------- OWNER PREMIUM MANAGEMENT ----------
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
        await interaction.response.send_message(f"{user.mention} does not have premium.", ephemeral=False)
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

@bot.tree.command(name="unblacklist", description="[🔒] Unblacklist (owner only)")
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

# ---------- FREE COMMAND: spam ----------
@bot.tree.command(name="spam", description="[🆓] Spam custom message (free)")
@app_commands.describe(message="Text to spam", total="Number of times (1-5)")
async def spam(interaction: discord.Interaction, message: str, total: int):
    if not await blacklist_check(interaction): return
    if total < 1 or total > 5:
        await interaction.response.send_message("❌ Total must be between 1 and 5.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(TROLL_MSG, ephemeral=True)
    for _ in range(total):
        await interaction.channel.send(message)
        await asyncio.sleep(0.5)
    await interaction.followup.send(f"✅ Sent {total} times.", ephemeral=True)

# ---------- PREMIUM: NSFW (ONLY .TXT) ----------
@bot.tree.command(name="nsfw", description="[💎] Send 5 NSFW images from your file (premium)")
async def nsfw(interaction: discord.Interaction):
    if not await blacklist_check(interaction): return
    if not is_premium(interaction):
        await interaction.response.send_message("❌ Premium only.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(TROLL_MSG, ephemeral=True)

    urls = get_nsfw_urls()
    if not urls:
        await interaction.followup.send("❌ No NSFW URLs found in `nsfw.txt`. Please add image URLs (one per line) and try again.", ephemeral=False)
        return

    for idx, url in enumerate(urls):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        await interaction.followup.send(f"⚠️ Failed to fetch image {idx+1} (HTTP {resp.status}).", ephemeral=False)
                        continue
                    img_data = await resp.read()
            ext = url.split('.')[-1].split('?')[0]
            ext = ext if ext.lower() in ['png', 'jpg', 'jpeg', 'gif', 'webp'] else 'png'
            file = discord.File(io.BytesIO(img_data), filename=f"nsfw_{idx+1}.{ext}")
            await interaction.followup.send(file=file)
            await asyncio.sleep(0.3)
        except Exception as e:
            await interaction.followup.send(f"⚠️ Error on image {idx+1}: {str(e)}", ephemeral=False)

# ---------- PREMIUM: massdm ----------
@bot.tree.command(name="massdm", description="[💎] DM all members with your message + invite link (premium)")
@app_commands.describe(message="Your custom message (will be shown as # heading)")
async def massdm(interaction: discord.Interaction, message: str):
    if not await blacklist_check(interaction): return
    if not is_premium(interaction):
        await interaction.response.send_message("❌ Premium only.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    guild = interaction.guild
    if not guild:
        await interaction.followup.send("❌ This command can only be used in a server.", ephemeral=True)
        return

    members = guild.members
    sent = 0
    failed = 0

    dm_text = f"# {message}\n\nJoin our server: https://discord.gg/BjtRhW6VHN"

    for member in members:
        if member.bot:
            continue
        try:
            await member.send(dm_text)
            sent += 1
        except:
            failed += 1
        await asyncio.sleep(0.3)

    await interaction.followup.send(f"✅ DM sent to **{sent}** members. Failed: **{failed}**", ephemeral=True)

# ---------- RUN ----------
bot.run(os.getenv("DISCORD_TOKEN"))
