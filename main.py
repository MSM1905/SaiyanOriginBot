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


TOKEN = "你的密钥"


# ======================
# 主菜单
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🛡 群管理", callback_data="group")],
        [InlineKeyboardButton("🎮 娱乐中心", callback_data="game")],
        [InlineKeyboardButton("💎 VIP中心", callback_data="vip")],
        [InlineKeyboardButton("📊 数据统计", callback_data="data")]
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
# 菜单
# ======================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    if query.data == "group":

        keyboard = [
            [InlineKeyboardButton("👋 欢迎新人", callback_data="welcome")],
            [InlineKeyboardButton("🚫 防广告", callback_data="spam")],
            [InlineKeyboardButton("🔨 管理命令", callback_data="admin")],
            [InlineKeyboardButton("⬅ 返回", callback_data="back")]
        ]

        await query.edit_message_text(
            "🛡 群管理中心\n\n请选择功能：",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif query.data == "admin":

        await query.edit_message_text(
            """
🔨 管理命令

管理员可使用：

/ban 回复用户消息
/mute 回复用户消息
/unmute 回复用户消息

示例：

回复用户消息发送：
/ban
"""
        )


    elif query.data == "welcome":

        await query.edit_message_text(
            "👋 欢迎新人\n\n✅ 已开启"
        )


    elif query.data == "spam":

        await query.edit_message_text(
            "🚫 防广告\n\n✅ 自动检测开启"
        )


    elif query.data == "game":

        await query.edit_message_text(
            "🎮 娱乐中心\n\n开发中..."
        )


    elif query.data == "vip":

        await query.edit_message_text(
            "💎 VIP中心\n\n开发中..."
        )


    elif query.data == "data":

        await query.edit_message_text(
            "📊 数据统计\n\n开发中..."
        )


    elif query.data == "back":

        await start(update, context)



# ======================
# 欢迎新人
# ======================

async def welcome_new_member(update, context):

    for member in update.message.new_chat_members:

        await update.message.reply_text(
            f"""
⚡ 欢迎 {member.first_name} 加入赛亚人起源社区！

📌 请遵守群规：

1. 禁止广告
2. 禁止诈骗
3. 禁止刷屏
"""
        )



# ======================
# 防广告
# ======================

BAD_WORDS = [
    "赌博",
    "博彩",
    "刷单",
    "诈骗",
    "加微信",
    "裸聊",
    "兼职赚钱"
]


def is_ad(text):

    if not text:
        return False

    text = text.lower()

    for word in BAD_WORDS:
        if word in text:
            return True


    if re.search(
        r"(https?://|www\.|t\.me/)",
        text
    ):
        return True


    return False



async def anti_spam(update, context):

    if not update.message:
        return

    if is_ad(update.message.text):

        try:
            await update.message.delete()

            await update.message.chat.send_message(
                "🚫 检测到广告，消息已删除"
            )

        except:
            pass



# ======================
# 管理员检测
# ======================

async def is_admin(update):

    member = await update.effective_chat.get_member(
        update.effective_user.id
    )

    return member.status in [
        "administrator",
        "creator"
    ]



# ======================
# 封禁
# ======================

async def ban(update, context):

    if not await is_admin(update):
        return


    if not update.message.reply_to_message:
        await update.message.reply_text(
            "请回复目标用户消息后使用 /ban"
        )
        return


    user = update.message.reply_to_message.from_user


    await update.effective_chat.ban_member(
        user.id
    )


    await update.message.reply_text(
        f"🔨 已封禁 {user.first_name}"
    )



# ======================
# 禁言
# ======================

async def mute(update, context):

    if not await is_admin(update):
        return


    if not update.message.reply_to_message:
        await update.message.reply_text(
            "请回复目标用户消息后使用 /mute"
        )
        return


    user = update.message.reply_to_message.from_user


    await update.effective_chat.restrict_member(
        user.id,
        permissions={
            "can_send_messages": False
        }
    )


    await update.message.reply_text(
        f"🔇 已禁言 {user.first_name}"
    )



# ======================
# 解禁
# ======================

async def unmute(update, context):

    if not await is_admin(update):
        return


    if not update.message.reply_to_message:
        return


    user = update.message.reply_to_message.from_user


    await update.effective_chat.restrict_member(
        user.id,
        permissions={
            "can_send_messages": True
        }
    )


    await update.message.reply_text(
        f"🔊 已解除禁言 {user.first_name}"
    )



# ======================
# Flask
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


app.add_handler(CommandHandler("start", start))

app.add_handler(
    CallbackQueryHandler(button)
)


app.add_handler(
    MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        welcome_new_member
    )
)


app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        anti_spam
    )
)


app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))


print("⚡ 赛亚人起源机器人启动成功")


app.run_polling()
