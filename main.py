import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "DEIN_BOT_TOKEN"

START_MESSAGES = [
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = random.choice(START_MESSAGES)
    await update.message.reply_text(message)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
