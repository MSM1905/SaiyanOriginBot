import threading
import signal
import sys
from flask import Flask
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler

from config import TOKEN
from database import init_db
from modules.menu import start, button
from modules.welcome import welcome_new_member
from modules.anti_spam import anti_spam
from modules.admin import ban, mute, unmute
from modules.rule_manager import (
    start_add_rule, receive_keyword, receive_penalty_type, 
    receive_duration, cancel_add_rule, list_rules_command, 
    del_rule_command, WAITING_KEYWORD, WAITING_DURATION
)

# ======================
# Flask 保活服务
# ======================
web = Flask(__name__)

@web.route("/")
def home():
    return "SaiyanOriginBot Running"

def run_web():
    # 关闭 Flask 的默认日志，防止干扰 Telegram 报错日志
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    web.run(host="0.0.0.0", port=10000, use_reloader=False)

# ======================
# Telegram 机器人初始化
# ======================
app = Application.builder().token(TOKEN).build()

# 基础功能
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_spam))

# 管理命令
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))

# 规则管理命令
app.add_handler(CommandHandler("listrules", list_rules_command))
app.add_handler(CommandHandler("delrule", del_rule_command))

# 添加规则的多轮对话
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
    per_message=True,
    allow_reentry=True
)
app.add_handler(add_rule_conv)

# ======================
# 启动入口与优雅退出
# ======================
if __name__ == "__main__":
    # 1. 初始化数据库
    init_db()
    
    # 2. 启动 Flask 保活线程
    threading.Thread(target=run_web, daemon=True).start()
    print("SaiyanOriginBot Started")
    
    # 3. 捕获系统中断信号，确保 Render 重启时能干净地释放 Token
    def signal_handler(sig, frame):
        print("Shutting down bot gracefully...")
        app.stop()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 4. 启动机器人长轮询
    app.run_polling()
