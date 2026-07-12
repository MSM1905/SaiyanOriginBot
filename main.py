from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


TOKEN = "8963882812:AAHrWlaMpZnXmwH5t4huisscec2Wlj9hT4I"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
⚡ 赛亚人起源·布罗利

请选择：

🛡 群管理
🎮 娱乐中心
💎 VIP中心
📊 数据统计
"""

    await update.message.reply_text(text)


app = Application.builder().token(TOKEN).build()


app.add_handler(
    CommandHandler("start", start)
)


app.run_polling()
