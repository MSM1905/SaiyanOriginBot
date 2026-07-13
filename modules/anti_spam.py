import re
from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from database import get_all_rules

# ======================
# 1. 默认的硬编码违禁词库 (保留你原有的设定)
# ======================
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
    """
    检测消息是否包含硬编码违禁词或外部链接
    """
    if not text:
        return False

    text_lower = text.lower()

    # 检查硬编码违禁词
    for word in BAD_WORDS:
        if word in text_lower:
            return True

    # 检查外部链接 (http, https, www, t.me)
    if re.search(r"(https?://|www\.|t\.me/)", text_lower):
        return True

    return False

# ======================
# 2. 核心反垃圾模块
# ======================
async def anti_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    自动检测广告和自定义违禁词，并执行删除与惩罚
    """
    if not update.message or not update.message.text:
        return

    message_text = update.message.text
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    is_violation = False
    violation_keyword = ""
    penalty_type = "mute"  # 默认惩罚类型
    penalty_duration = 60  # 默认惩罚时长(秒)

    # --- 第一步：检查硬编码违禁词和链接 ---
    if is_ad(message_text):
        is_violation = True
        violation_keyword = "广告/外部链接"
        # 硬编码词库默认执行禁言60秒
        penalty_type = "mute"
        penalty_duration = 60

    # --- 第二步：检查数据库中的自定义规则 ---
    # (如果前面已经命中硬编码，这里就不需要再查数据库了)
    if not is_violation:
        rules = get_all_rules()
        for rule in rules:
            rule_id, keyword, p_type, p_duration = rule
            if keyword.lower() in message_text.lower():
                is_violation = True
                violation_keyword = keyword
                penalty_type = p_type
                penalty_duration = p_duration
                break  # 命中一条规则后立即跳出，避免重复惩罚

    # --- 第三步：如果命中违规，执行惩罚 ---
    if is_violation:
        try:
            # 1. 删除违规消息
            try:
                await update.message.delete()
            except Exception:
                pass  # 如果机器人没有删消息权限，忽略此错误

            # 2. 执行对应的惩罚
            if penalty_type == "warn":
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"⚠️ **警告**\n用户 [{user_name}](tg://user?id={user_id})，"
                         f"您的发言包含违禁词 `{violation_keyword}`，请注意群规！",
                    parse_mode="Markdown"
                )
                
            elif penalty_type == "mute":
                await context.bot.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=update.message.date.timestamp() + penalty_duration
                )
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"🤐 **禁言通知**\n用户 [{user_name}](tg://user?id={user_id}) "
                         f"因触发违禁词 `{violation_keyword}`，已被禁言 {penalty_duration} 秒。",
                    parse_mode="Markdown"
                )
                
            elif penalty_type == "ban":
                await context.bot.ban_chat_member(
                    chat_id=chat_id,
                    user_id=user_id
                )
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"🔨 **封禁通知**\n用户 [{user_name}](tg://user?id={user_id}) "
                         f"因触发违禁词 `{violation_keyword}`，已被永久封禁。",
                    parse_mode="Markdown"
                )

        except Exception as e:
            # 捕获权限错误，防止机器人崩溃
            print(f"执行惩罚失败，请确保机器人在群内是管理员且拥有相应权限！错误信息: {e}")

            await update.message.chat.send_message(
                "🚫 检测到广告，消息已删除"
            )


        except Exception:

            pass
