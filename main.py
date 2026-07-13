from flask import Flask
import threading
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler
)

from config import TOKEN
from database import init_db
from modules.menu import start, button
from modules.welcome import welcome_new_member
from modules.anti_spam import anti_spam
from modules.admin import ban, mute, unmute
from modules.rule_manager import (
    start_add_rule,
    receive_keyword,
    receive_penalty_type,
    receive_duration,
    cancel_add_rule,
    list_rules_command,
    del_rule_command,
    WAITING_KEYWORD,
    WAITING_DURATION
)


# ======================
# Flask 保活端口
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


# ======================
# Telegram机器人
# ======================
app = Application.builder().token(TOKEN).build()


# 基础菜单
app.add_handler(CommandHandler("start", start))


# 按钮
app.add_handler(CallbackQueryHandler(button))


# 新人欢迎
app.add_handler(
    MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        welcome_new_member
    )
)


# 自动反广告
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        anti_spam
    )
)


# 管理命令
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))


# 自定义规则管理
app.add_handler(CommandHandler("listrules", list_rules_command))
app.add_handler(CommandHandler("delrule", del_rule_command))

# 多轮对话：添加规则
add_rule_conv = ConversationHandler(
    entry_points=[CommandHandler("addrule", start_add_rule)],
    states={
        WAITING_KEYWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_keyword)],
        WAITING_DURATION: [
            CallbackQueryHandler(receive_penalty_type),
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_duration)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel_add_rule)],
)
app.add_handler(add_rule_conv)


# ======================
# 启动
# ======================
if __name__ == "__main__":
    init_db()

    threading.Thread(
        target=run_web,
        daemon=True
    ).start()

    print("SaiyanOriginBot Started")
    app.run_polling()
