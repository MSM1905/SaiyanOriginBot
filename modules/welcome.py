from telegram import Update
from telegram.ext import ContextTypes


# ======================
# 新人欢迎
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
