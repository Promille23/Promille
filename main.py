import json
import random
from datetime import datetime, time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7328230261:AAG1v58gRgFWl9f6uUd4IM2mAyfJnPn1-RI"
WEBHOOK_URL = "https://promillebot.onrender.com"  # hier deine Render-URL

PORT = 443
POINTS_FILE = "points.json"
CHATS_FILE = "chats.json"

# Beispiel-Listen (du kannst hier deine eigenen Inhalte reinpacken)
GOGGINS_MESSAGES = [
    "💀 Aufstehen, du Schwächling! Niemand rettet dich. MACH. DEN. JOB.",
    "🔥 Dein innerer Schweinehund schreit? Schrei lauter, Bro! Keiner wird dich jemals bemitleiden.",
    "💪 Jeder Tag ist Krieg. DU entscheidest, ob du Opfer oder Killer bist."
]

MORNING_QUESTIONS = [
    "💬 Was ist dein Ziel für heute?",
    "⚡ Was machst du heute besser als gestern?",
    "🔥 Worauf bist du heute besonders fokussiert?"
]

SPORT_CODES = [
    "🐶 Hundeapfel",
    "🧹 Besenfurz",
    "🍴 Gabelschiene"
]

def load_points():
    try:
        with open(POINTS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_points(points):
    with open(POINTS_FILE, "w") as f:
        json.dump(points, f)

def load_chats():
    try:
        with open(CHATS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_chats(chats):
    with open(CHATS_FILE, "w") as f:
        json.dump(chats, f)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.lower()
    now = datetime.now().time()
    points = load_points()
    chats = load_chats()

    if user.id not in chats:
        chats.append(user.id)
        save_chats(chats)

    if text == "moin":
        if time(5, 0) <= now <= time(6, 0):
            user_id = str(user.id)
            if user_id not in points:
                points[user_id] = {"name": user.first_name, "score": 0}
            points[user_id]["score"] += 1
            save_points(points)

            goggins_msg = random.choice(GOGGINS_MESSAGES)
            question = random.choice(MORNING_QUESTIONS)
            sport_code = random.choice(SPORT_CODES)
            response = f"{goggins_msg}\n\n{question}\n\n🤪 Code des Tages: {sport_code}"
            await update.message.reply_text(response)
        else:
            await update.message.reply_text("❌ Zu spät, Bro! Zwischen 5:00 und 6:00 Uhr heißt Disziplin. Versuch’s morgen wieder!")

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    points = load_points()
    if not points:
        await update.message.reply_text("Noch keine Einträge, Bro! Sei der Erste, der Disziplin zeigt!")
        return
    ranking = sorted(points.items(), key=lambda x: x[1]["score"], reverse=True)
    text = "🏆 Disziplin-Ranking:\n"
    for i, (user_id, data) in enumerate(ranking, start=1):
        text += f"{i}. {data['name']} – {data['score']} Punkte\n"
    await update.message.reply_text(text)

async def reset_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_points({})
    await update.message.reply_text("🧨 Punkte wurden zurückgesetzt, Bro! Neue Runde, neues Spiel!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("resetpoints", reset_points))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )
