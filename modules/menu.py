from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


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


    await update.message.reply_text(
        """
⚡ 赛亚人起源·布罗利

请选择功能：
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



# ======================
# 按钮处理
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
                    "🚫 防广告",
                    callback_data="spam"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔨 管理功能",
                    callback_data="admin"
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
            "🛡 群管理中心",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif query.data == "back":

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


        await query.edit_message_text(
            "⚡ 赛亚人起源·布罗利\n\n请选择功能：",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    else:

        await query.edit_message_text(
            f"{query.data} 功能开发中..."
        )
