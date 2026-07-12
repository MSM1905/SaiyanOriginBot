from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters
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
            InlineKeyboardButton(
                "🛡 群管理",
                callback_data="group"
            )
        ],
        [
            InlineKeyboardButton(
                "🎮 娱乐中心",
                callback_data="game"
            )
        ],
        [
            InlineKeyboardButton(
                "💎 VIP中心",
                callback_data="vip"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 数据统计",
                callback_data="data"
            )
        ]
    ]

    text = """
⚡ 赛亚人起源·布罗利

请选择功能：
"""

    markup = InlineKeyboardMarkup(keyboard)

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
# 菜单按钮处理
# ======================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


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
                    "⬅ 返回主页",
                    callback_data="back"
                )
            ]
        ]


        await query.edit_message_text(
            """
🛡 群管理中心

请选择功能：
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif query.data == "game":

        await query.edit_message_text(
            """
🎮 娱乐中心

功能开发中...
"""
        )


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


    elif query.data == "welcome":

        await query.edit_message_text(
            """
👋 欢迎新人

状态：开发完成

机器人已支持新人欢迎功能。
"""
        )


    elif query.data == "clean":

        await query.edit_message_text(
            """
🧹 自动清理

功能开发中...
"""
        )


    elif query.data == "spam":

        await query.edit_message_text(
            """
🚫 防广告

功能开发中...
"""
        )


    elif query.data == "back":

        await start(update, context)



# ======================
# 新人欢迎功能
# ======================

async def welcome_new_member(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    for member in update.message.new_chat_members:

        name = member.first_name

        text = f"""
⚡ 欢迎 {name} 加入赛亚人起源社区！

📌 群规：

1️⃣ 禁止广告
2️⃣ 禁止诈骗
3️⃣ 禁止刷屏
4️⃣ 文明交流

祝你体验愉快！
"""

        await update.message.reply_text(text)



# ======================
# Flask 保活(Render)
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
    CallbackQueryHandler(
        button
    )
)


app.add_handler(
    MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        welcome_new_member
    )
)


print("⚡ 赛亚人起源机器人启动成功")


app.run_polling()
