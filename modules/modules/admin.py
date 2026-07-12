from telegram import Update
from telegram.ext import ContextTypes


# ======================
# 判断管理员
# ======================

async def check_admin(update: Update):

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

async def ban(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await check_admin(update):
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

async def mute(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await check_admin(update):
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

async def unmute(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await check_admin(update):
        return


    if not update.message.reply_to_message:

        await update.message.reply_text(
            "请回复目标用户消息后使用 /unmute"
        )

        return


    user = update.message.reply_to_message.from_user


    await update.effective_chat.restrict_member(
        user.id,
        permissions={
            "can_send_messages": True,
            "can_send_media_messages": True
        }
    )


    await update.message.reply_text(
        f"🔊 已解除禁言 {user.first_name}"
    )
