
import discord
from discord.ext import commands
from flask import Flask
import threading
import os
from datetime import date

# ------------ Flask Health Check ------------ #
app = Flask(__name__)

@app.route("/")
def home():
    return "ok"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run_flask).start()

# ------------ Discord Bot ------------ #
intents = discord.Intents.default()
intents.members = True       # מאפשר לבוט לקרוא רשימת משתמשים ו-roles
intents.messages = True      # מאפשר לקרוא ולשלוח הודעות
bot = commands.Bot(command_prefix="!", intents=intents)

items = {
    "פיל": -1000,
    "פרה": -12,
    "אריה": 50,
    "חמור": 20
}

DAILY_LIMIT_FREE = 5
DAILY_LIMIT_PREMIUM = 50
user_usage = {}
usage_date = date.today()

@bot.event
async def on_ready():
    print(f"מחובר בתור {bot.user}")

@bot.command()
async def כמה(ctx, *, שם_פריט):
    global usage_date, user_usage
    today = date.today()
    user_id = ctx.author.id

    if today != usage_date:
        user_usage = {}
        usage_date = today

    if user_id not in user_usage:
        user_usage[user_id] = 0

    is_premium = False
    for role in ctx.author.roles:
        if role.name.lower() == "premium":
            is_premium = True
            break

    limit = DAILY_LIMIT_PREMIUM if is_premium else DAILY_LIMIT_FREE

    if user_usage[user_id] >= limit:
        await ctx.send(f"הגעת למגבלת הבקשות היומית שלך ({limit})")
        return

    user_usage[user_id] += 1

    שם_פריט = שם_פריט.strip()
    if שם_פריט in items:
        await ctx.send(f"הערך של {שם_פריט} הוא {items[שם_פריט]}")
    else:
        await ctx.send("ערך לא תקין")

bot.run(os.environ["DISCORD_TOKEN"])
