import json
import random
from datetime import datetime, time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7328230261:AAHk1T0_v1yO3fvR3_aEOGkjPQK01ay3tEw"
POINTS_FILE = "points.json"

GOGGINS_MESSAGES = [
    "💀 Aufstehen, du Schwächling! Niemand rettet dich. MACH. DEN. JOB.",
    "🔥 Dein innerer Schweinehund schreit? Schrei lauter, Bro! Keiner wird dich jemals bemitleiden.",
    "💪 Jeder Tag ist Krieg. DU entscheidest, ob du Opfer oder Killer bist.",
    "🚀 Niemand interessiert sich, wie du dich fühlst. AUFSTEHEN. TRAINIEREN. LIEFERN.",
    "⏰ 5 Uhr? Kinderspiel. Zeig mir, dass du ein verdammtes Tier bist.",
    "🥂 Während andere schlafen, baust du deine Legende. KEEP HAMMERING, MOTHERF*CKER.",
    "⚡ Schmerz ist temporär. Aufgeben ist für immer. Also BEISS, Bro!",
    "🏆 Du willst Resultate? Dann hör auf zu labern und fang an zu SCHINDEN.",
    "🔥 Heute killst du die Ausreden. Heute killst du die Limits. Heute killst du dein altes Ich.",
    "💥 Hör auf zu warten. Niemand wird kommen, dich zu retten. Es liegt an DIR, BRO."
]

MORNING_QUESTIONS = [
    "💬 Was ist dein Ziel für heute?",
    "💭 Wie hast du geschlafen?",
    "⚡ Was machst du heute besser als gestern?",
    "🔥 Worauf bist du heute besonders fokussiert?",
    "🏆 Wie wirst du heute über dich hinauswachsen?",
    "🤔 Was würdest du tun, wenn du wüsstest, du kannst heute nicht scheitern?",
    "💥 Wer bist du heute: der Jäger oder die Beute?",
    "🚀 Was bringt dich heute 1 % näher an dein großes Ziel?",
    "😈 Welche Ausrede killst du heute?",
    "👊 Wenn du heute nur eine Sache zu 110 % erledigst – was ist es?",
    "🏋️ Was ist heute dein härtester mentaler oder körperlicher Test?",
    "🎯 Wer würde stolz auf dich sein, wenn er/sie heute zuschaut?",
    "💡 Welcher Gedanke motiviert dich gerade am meisten?",
    "📈 Welche kleine Challenge setzt du dir zusätzlich heute?",
    "🎤 Was schreist du dir heute innerlich selbst zu, um dich zu pushen?",
    "🕶️ Wenn du dich heute wie ein Champion verhältst – wie sieht das aus?",
    "🌊 Wo gehst du heute gegen den Strom, um stärker zu werden?",
    "🚦 Welches Hindernis packst du heute direkt als Erstes an?",
    "🔥 Wie machst du heute klar, dass du die Kontrolle hast?",
    "🧠 Welche Gewohnheit baust du heute bewusst ein?"
]

SPORT_CODES = [
    "🐶 Hundeapfel",
    "🧹 Besenfurz",
    "🍴 Gabelschiene",
    "🍌 Bananenbieger",
    "🐟 Fischschlürfer",
    "🚀 Raketenmurmel",
    "🦄 Einhorngurke",
    "🍕 Pizzahantel",
    "🎩 Zauberbohne",
    "🛸 Ufo-Tapser",
    "🐸 Froschpfeife",
    "🍩 Donut-Schleuder",
    "🦆 Ententango",
    "💼 Aktenkoffer-Roller",
    "📦 Paketwackler",
    "🧽 Schwammbooster",
    "🔧 Schraubenschwung",
    "🌭 Würstchensprinter",
    "🐘 Elefantenflüsterer",
    "🍿 Popcorntrommel"
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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.lower()
    now = datetime.now().time()
    points = load_points()

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
    app.add_handler(CommandHandler("resetpoints", reset_points))  # Nur für den KING!

    app.run_polling()
