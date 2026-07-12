from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from flask import Flask
import threading


TOKEN = "8963882812:AAHrWlaMpZnXmwH5t4huisscec2Wlj9hT4I"


# ======================
# Telegram机器人部分
# ======================

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
    CommandHandler(
        "start",
        start
    )
)



# ======================
# Render网页端口部分
# ======================

web = Flask(__name__)


@web.route("/")
def home():

    return "SaiyanOriginBot Running"



def run_web():

    web.run(
        host="0.0.0.0",
        port=10000
    )



# 启动Flask网页
threading.Thread(
    target=run_web,
    daemon=True
).start()



# ======================
# 启动Telegram机器人
# ======================

print("⚡ 赛亚人起源机器人启动成功")

app.run_polling()
