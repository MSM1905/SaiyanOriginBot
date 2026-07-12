from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)

from flask import Flask
import threading


TOKEN = "8963882812:AAHrWlaMpZnXmwH5t4huisscec2Wlj9hT4I"


# ======================
# 主菜单
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("🛡 群管理", callback_data="group")
        ],
        [
            InlineKeyboardButton("🎮 娱乐中心", callback_data="game")
        ],
        [
            InlineKeyboardButton("💎 VIP中心", callback_data="vip")
        ],
        [
            InlineKeyboardButton("📊 数据统计", callback_data="data")
        ]
    ]

    markup = InlineKeyboardMarkup(keyboard)

    text = """
⚡ 赛亚人起源·布罗利

请选择功能：
"""

    if update.message:
        await update.message.reply_text(
            text,
            reply_markup=markup
        )

    else:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=markup
        )


# ======================
# 按钮处理
# ======================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


    # 群管理
    if query.data == "group":

        keyboard = [
            [
                InlineKeyboardButton(
                    "👋 欢迎新人",
                    callback_data="welcome"
                )
            ],
            [
                InlineKeyboardButton(
                    "🧹 自动清理",
                    callback_data="clean"
                )
            ],
            [
                InlineKeyboardButton(
                    "🚫 防广告",
                    callback_data="spam"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ 返回",
                    callback_data="back"
                )
            ]
        ]

        await query.edit_message_text(
            "🛡 群管理\n\n请选择功能：",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # 娱乐
    elif query.data == "game":

        await query.edit_message_text(
            "🎮 娱乐中心\n\n开发中..."
        )


    # VIP
    elif query.data == "vip":

        await query.edit_message_text(
            """
💎 VIP中心

高级功能：

⭐ AI审核
⭐ 高级防广告
⭐ 数据统计
⭐ 自动运营

开发中...
"""
        )


    # 数据
    elif query.data == "data":

        await query.edit_message_text(
            """
📊 数据统计

当前暂无数据。

后续支持：

- 群活跃统计
- 删除记录
- 用户排行
"""
        )


    # 群管理功能占位

    elif query.data == "welcome":

        await query.edit_message_text(
            "👋 欢迎新人\n\n功能开发中..."
        )


    elif query.data == "clean":

        await query.edit_message_text(
            "🧹 自动清理\n\n功能开发中..."
        )


    elif query.data == "spam":

        await query.edit_message_text(
            "🚫 防广告\n\n功能开发中..."
        )


    # 返回

    elif query.data == "back":

        await start(update, context)



# ======================
# Flask 保活
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



threading.Thread(
    target=run_web,
    daemon=True
).start()



# ======================
# 启动机器人
# ======================

app = Application.builder().token(TOKEN).build()


app.add_handler(
    CommandHandler(
        "start",
        start
    )
)


app.add_handler(
    CallbackQueryHandler(button)
)


print("⚡ 赛亚人起源机器人启动成功")


app.run_polling()
app.run_polling()
