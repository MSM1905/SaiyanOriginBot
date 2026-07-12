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
import re


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
# 菜单处理
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


    elif query.data == "welcome":

        await query.edit_message_text(
            """
👋 欢迎新人

状态：

✅ 已开启
"""
        )


    elif query.data == "spam":

        await query.edit_message_text(
            """
🚫 防广告系统

状态：

✅ 自动检测开启

检测内容：

- 网站链接
- Telegram邀请链接
- 微信广告
- 赌博广告
- 刷单广告
"""
        )


    elif query.data == "clean":

        await query.edit_message_text(
            """
🧹 自动清理

功能开发中...
"""
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
⭐ 高级过滤
⭐ 数据统计

开发中...
"""
        )


    elif query.data == "data":

        await query.edit_message_text(
            """
📊 数据统计

暂无数据

后续支持：

- 消息统计
- 违规记录
- 用户排行
"""
        )


    elif query.data == "back":

        await start(update, context)



# ======================
# 欢迎新人
# ======================

async def welcome_new_member(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    for member in update.message.new_chat_members:

        await update.message.reply_text(
            f"""
⚡ 欢迎 {member.first_name} 加入赛亚人起源社区！

📌 群规：

1️⃣ 禁止广告
2️⃣ 禁止诈骗
3️⃣ 禁止刷屏
4️⃣ 文明交流

祝你体验愉快！
"""
        )



# ======================
# 防广告系统
# ======================

BAD_WORDS = [
    "赌博",
    "博彩",
    "刷单",
    "兼职赚钱",
    "贷款",
    "色情",
    "裸聊",
    "诈骗",
    "加微信",
    "微信赚钱"
]


def is_ad(text):

    if not text:
        return False


    text = text.lower()


    # 检测关键词

    for word in BAD_WORDS:

        if word in text:
            return True


    # 检测网址

    url_pattern = r"(https?://|www\.|t\.me/|telegram\.me/)"

    if re.search(url_pattern, text):

        return True


    return False



async def anti_spam(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return


    text = update.message.text


    if is_ad(text):

        try:

            await update.message.delete()


            warn = await update.message.chat.send_message(
                f"""
🚫 检测到广告内容

用户：
{update.message.from_user.first_name}

消息已删除。
"""
            )


        except Exception:

            pass



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
# 启动
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


# 防广告监听文字消息

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        anti_spam
    )
)



print("⚡ 赛亚人起源机器人启动成功")


app.run_polling()
