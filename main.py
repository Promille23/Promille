import random
from datetime import datetime, time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7328230261:AAHk1T0_v1yO3fvR3_aEOGkjPQK01ay3tEw"

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
    "🏆 Wie wirst du heute über dich hinauswachsen?"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now().time()
    if time(5, 0) <= now <= time(6, 0):
        goggins_msg = random.choice(GOGGINS_MESSAGES)
        question = random.choice(MORNING_QUESTIONS)
        response = f"{goggins_msg}\n\n{question}"
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("❌ Zu spät, Bro! Zwischen 5:00 und 6:00 Uhr heißt Disziplin. Versuch’s morgen wieder!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
