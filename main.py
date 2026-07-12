from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from flask import Flask
import threading


TOKEN = "你的密钥"



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



# 开启网页端口
threading.Thread(
    target=run_web
).start()



# 启动机器人
app.run_polling()
