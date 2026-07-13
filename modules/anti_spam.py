import re
from telegram import Update
from telegram.ext import ContextTypes


BAD_WORDS = [
    "赌博",
    "博彩",
    "刷单",
    "诈骗",
    "加微信",
    "裸聊",
    "兼职赚钱",
    "贷款"
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



async def anti_spam(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return


    if is_ad(update.message.text):

        try:

            await update.message.delete()


            await update.message.chat.send_message(
                "🚫 检测到广告，消息已删除"
            )


        except Exception:

            pass
