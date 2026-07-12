import discord,asyncio,random,datetime,aiohttp,io,os
from discord.ext import commands
from discord import app_commands

intents=discord.Intents.all()
bot=commands.Bot(command_prefix="!",intents=intents)

OWNER=[1419223630952403054]
PREMIUM=[]
BLACKLIST=[]
TROLL="🔹 Trolling sequence initiated..."

RAID_TEXT=("# EXILON STRIKES AGAIN, SON 🏅\n**YOUR SERVER? RAIDED. YOUR IP? LOGGED. YOUR TEARS? DELICIOUS. #FAIRS**\n\n---\n\n## WE GIVE YOU THE KEYS TO THE KINGDOM:\n> ✔️ FREE RAID BOT – WORKS ON ANY SERVER, NO PERMS NEEDED.\n> ✔️ IP GRABBER – FIND ANYONE, ANYTIME.\n> ✔️ 24/7 UPTIME – WE NEVER SLEEP.\n> ✔️ PREMIUM UPGRADE – UNLIMITED RAIDS, CUSTOM PAYLOADS, VIP CHANNEL, AND PRIORITY SUPPORT.\n\n```\n🔥 FREE BOT FOR ALL – PREMIUM FOR THE REAL ONES\n```\n\n***\"CAN'T BEAT 'EM? JOIN 'EM.\" – THAT'S OUR MOTTO, SON.***\n\n💬 JOIN EXILON | 2026 – https://discord.gg/BjtRhW6VHN\n\n**RAID ANYONE, ANYWHERE, NO QUESTIONS ASKED.**\n- - - -\n_Powered by Exilon_")
CUNEIFORM="# 𒅒𒈔𒅒𒇫𒄆"*20 + "\n\n**https://discord.gg/BjtRhW6VHN**"

def blame_msg(m):return f"# 💀💀💀 RAID DETECTED – YOU'VE BEEN SPOTTED 💀💀💀\n\n{m.mention} – thanks for raiding and dropping chaos on this server. We see you, we respect you, and we want you on our side.\n\n## 🎁 Join EXILON and get your own FREE raid bot – fully functional, easy to use, 24/7 uptime.\n\n**💎 We also offer premium features if you're ready to level up:**\n- Unlimited raid commands.\n- Priority Support for premium user.\n- And more...\n\nAll available for purchase – because power has a price, but the free bot is yours to keep.\n\n🔗 COME RAID WITH US: https://discord.gg/BjtRhW6VHN"
AD_TEXT="# 🔥 JOIN EXILON – THE RAID COMMUNITY 🔥\n\n**Get your own FREE raid bot with:**\n• Unlimited raid commands\n• IP grabber\n• 24/7 uptime\n• Premium upgrades available\n\n💬 **Join us now:** https://discord.gg/BjtRhW6VHN\n\n**Raid anyone, anywhere, no questions asked.**\n\n_Exilon | 2026_"
def fake_ip():return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

NSFW_URLS=[]
if os.path.exists("nsfw.txt"):
 with open("nsfw.txt","r") as f: NSFW_URLS=[l.strip() for l in f if l.strip()]
def get_nsfw():return random.sample(NSFW_URLS,5) if NSFW_URLS else None

USER_TOKEN = os.getenv("USER_TOKEN")   # Your Discord user token

class NitroView(discord.ui.View):
 def __init__(self):super().__init__(timeout=120)
 @discord.ui.button(label="Accept",style=discord.ButtonStyle.success,custom_id="nitro_accept")
 async def accept(self,i,b):
  await i.response.send_message(f"HAHA EZ U FELL FOR THIS LOL JOIN {i.user.mention}\nhttps://discord.gg/BjtRhW6VHN",ephemeral=False)

async def blacklist_check(i):
 if i.user.id in BLACKLIST:
  await i.response.send_message("⛔ Access denied.",ephemeral=True);return False
 return True

@bot.event
async def on_ready():
 await bot.tree.sync()
 print(f"Logged as {bot.user}")

# ---------- SINGLE /raid COMMAND (no parameters) ----------
@bot.tree.command(name="raid",description="[🆓] Raid this channel using your user token")
async def raid_cmd(i):
 if not await blacklist_check(i):return
 if not USER_TOKEN:
  await i.response.send_message("❌ USER_TOKEN not set. Cannot raid.", ephemeral=True)
  return
 await i.response.send_message("🚀 Raid started...", ephemeral=True)
 headers = {"Authorization": USER_TOKEN, "Content-Type": "application/json"}
 channel_id = i.channel.id
 async with aiohttp.ClientSession() as s:
  for _ in range(5):
   payload = {"content": RAID_TEXT, "allowed_mentions": {"parse": ["everyone", "here"]}}
   async with s.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", json=payload, headers=headers) as r:
    if r.status != 200:
     await i.followup.send(f"⚠️ Failed on attempt {_+1} (HTTP {r.status})", ephemeral=True)
     return
   await asyncio.sleep(.5)
  payload = {"content": CUNEIFORM, "allowed_mentions": {"parse": ["everyone", "here"]}}
  async with s.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", json=payload, headers=headers) as r:
   if r.status != 200:
    await i.followup.send("⚠️ Failed to send cuneiform message", ephemeral=True)
    return
 await i.followup.send("✅ Raid complete!", ephemeral=True)

# ---------- OTHER COMMANDS ----------
@bot.tree.command(name="blame",description="[🆓] Blame a user")
@app_commands.describe(user="Target")
async def blame(i,user:discord.Member):
 if not await blacklist_check(i):return
 await i.response.send_message(TROLL,ephemeral=True)
 await i.followup.send(blame_msg(user))

@bot.tree.command(name="ip",description="[🆓] Fake intrusion alert")
@app_commands.describe(user="Target")
async def ip(i,user:discord.Member):
 if not await blacklist_check(i):return
 await i.response.send_message(TROLL,ephemeral=True)
 ip=fake_ip();port=random.randint(1024,65535);mac=':'.join(['{:02x}'.format(random.randint(0,255)) for _ in range(6)]);trace=''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',k=8));ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
 embed=discord.Embed(title="⚠️ SYSTEM INTRUSION DETECTED",description=f"**Target:** {user.mention}\n**IP Address:** `{ip}`\n**Port:** `{port}`\n**MAC:** `{mac}`\n**Trace ID:** `#{trace}`\n**Timestamp:** `{ts}`\n\n```css\n[CRITICAL] Unauthorized access attempt logged.\n[ACTION] Monitoring initiated – further activity will be reported.\n```",color=discord.Color.dark_red()).set_footer(text="Simulated alert – no real data.")
 await i.followup.send(content=user.mention,embed=embed)

@bot.tree.command(name="say",description="[🆓] Make bot say something")
@app_commands.describe(message="Text")
async def say(i,message:str):
 if not await blacklist_check(i):return
 await i.response.send_message(TROLL,ephemeral=True)
 await i.followup.send(message)

@bot.tree.command(name="nitro",description="[🆓] Fake Nitro gift")
@app_commands.describe(user="(Optional) Target")
async def nitro(i,user:discord.Member=None):
 if not await blacklist_check(i):return
 await i.response.send_message(TROLL,ephemeral=True)
 target=user if user else i.user
 embed=discord.Embed(title="You've been gifted a subscription!",description=f"@{target.display_name} You Only Have 72h to earn it!",color=discord.Color.gold()).set_image(url="https://refillarena.com/_next/image?url=https%3A%2F%2Frefillarena.s3.amazonaws.com%2Fdiscord+nitro.png&w=640&q=75")
 await i.followup.send(content=target.mention,embed=embed,view=NitroView())

@bot.tree.command(name="checkraid",description="[🆓] Flash invite link")
async def checkraid(i):
 if not await blacklist_check(i):return
 await i.response.send_message(TROLL,ephemeral=True)
 msg=await i.followup.send("https://discord.gg/BjtRhW6VHN",ephemeral=False)
 await asyncio.sleep(1);await msg.delete()
 await i.followup.send("✅ Link flashed.",ephemeral=True)

@bot.tree.command(name="ad",description="[🆓] Show Exilon ad")
async def ad(i):
 if not await blacklist_check(i):return
 await i.response.send_message(TROLL,ephemeral=True)
 await i.followup.send(AD_TEXT)

def is_owner(i):return i.user.id in OWNER
def is_premium(i):return i.user.id in PREMIUM

@bot.tree.command(name="addpremium",description="[🔒] Grant premium (owner)")
@app_commands.describe(user="User")
async def addp(i,user:discord.Member):
 if not is_owner(i):await i.response.send_message("❌ Owner only.",ephemeral=True);return
 if user.id in PREMIUM:await i.response.send_message(f"{user.mention} already premium.",ephemeral=False);return
 PREMIUM.append(user.id);await i.response.send_message(f"{user.mention} [💎] Premium granted.",ephemeral=False)

@bot.tree.command(name="removepremium",description="[🔒] Remove premium (owner)")
@app_commands.describe(user="User")
async def remp(i,user:discord.Member):
 if not is_owner(i):await i.response.send_message("❌ Owner only.",ephemeral=True);return
 if user.id not in PREMIUM:await i.response.send_message(f"{user.mention} not premium.",ephemeral=False);return
 PREMIUM.remove(user.id);await i.response.send_message(f"{user.mention} [💎] Premium revoked.",ephemeral=False)

@bot.tree.command(name="blacklist",description="[🔒] Blacklist user (owner)")
@app_commands.describe(user="User")
async def bl(i,user:discord.Member):
 if not is_owner(i):await i.response.send_message("❌ Owner only.",ephemeral=True);return
 if user.id in BLACKLIST:await i.response.send_message(f"{user.mention} already blacklisted.",ephemeral=False);return
 BLACKLIST.append(user.id);await i.response.send_message(f"{user.mention} blacklisted.",ephemeral=False)

@bot.tree.command(name="unblacklist",description="[🔒] Unblacklist (owner)")
@app_commands.describe(user="User")
async def ubl(i,user:discord.Member):
 if not is_owner(i):await i.response.send_message("❌ Owner only.",ephemeral=True);return
 if user.id not in BLACKLIST:await i.response.send_message(f"{user.mention} not blacklisted.",ephemeral=False);return
 BLACKLIST.remove(user.id);await i.response.send_message(f"{user.mention} unblacklisted.",ephemeral=False)

@bot.tree.command(name="spam",description="[💎] Spam custom message")
@app_commands.describe(message="Text",total="Times (1-5)")
async def spam(i,message:str,total:int):
 if not await blacklist_check(i):return
 if not is_premium(i):await i.response.send_message("❌ Premium only.",ephemeral=True);return
 if total<1 or total>5:await i.response.send_message("❌ 1-5 only.",ephemeral=True);return
 await i.response.send_message(TROLL,ephemeral=True)
 for _ in range(total):await i.channel.send(message);await asyncio.sleep(.5)
 await i.followup.send(f"✅ Sent {total} times.",ephemeral=True)

@bot.tree.command(name="nsfw",description="[💎] Send 5 NSFW images")
async def nsfw(i):
 if not await blacklist_check(i):return
 if not is_premium(i):await i.response.send_message("❌ Premium only.",ephemeral=True);return
 await i.response.send_message(TROLL,ephemeral=True)
 urls=get_nsfw()
 if urls:
  for idx,u in enumerate(urls):
   try:
    async with aiohttp.ClientSession() as s:
     async with s.get(u) as r:
      if r.status!=200:await i.followup.send(f"⚠️ Failed image {idx+1}.",ephemeral=False);continue
      img=await r.read()
    ext=u.split('.')[-1].split('?')[0];ext=ext if ext.lower() in ['png','jpg','jpeg','gif','webp'] else 'png'
    await i.followup.send(file=discord.File(io.BytesIO(img),filename=f"nsfw_{idx+1}.{ext}"))
    await asyncio.sleep(.3)
   except:await i.followup.send(f"⚠️ Error image {idx+1}.",ephemeral=False)
 else:
  APIs=["https://api.waifu.pics/nsfw/waifu","https://api.waifu.pics/nsfw/neko","https://api.waifu.pics/nsfw/trap"]
  for attempt in range(5):
   success=False
   for api in APIs:
    try:
     async with aiohttp.ClientSession() as s:
      async with s.get(api) as r:
       if r.status!=200:continue
       data=await r.json();url=data.get("url")
       if not url:continue
       async with s.get(url) as img_r:
        if img_r.status!=200:continue
        img=await img_r.read()
       ext=url.split('.')[-1].split('?')[0];ext=ext if ext.lower() in ['png','jpg','jpeg','gif','webp'] else 'png'
       await i.followup.send(file=discord.File(io.BytesIO(img),filename=f"nsfw_{attempt+1}.{ext}"))
       success=True;break
    except:continue
   if not success:await i.followup.send(f"⚠️ Failed attempt {attempt+1}.",ephemeral=False)
   await asyncio.sleep(.3)

bot.run(os.getenv("DISCORD_TOKEN"))
