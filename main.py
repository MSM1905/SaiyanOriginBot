from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from flask import Flask
import threading


from config import TOKEN


# 功能模块

from modules.menu import (
    start,
    button
)

from modules.welcome import (
    welcome_new_member
)

from modules.anti_spam import (
    anti_spam
)

from modules.admin import (
    ban,
    mute,
    unmute
)



# ======================
# Render 保活网页
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
# 机器人启动
# ======================

def main():

    print("⚡ 赛亚人起源机器人启动")


    app = Application.builder().token(TOKEN).build()



    # start菜单

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    # 按钮

    app.add_handler(
        CallbackQueryHandler(
            button
        )
    )


    # 新人欢迎

    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            welcome_new_member
        )
    )


    # 防广告

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            anti_spam
        )
    )


    # 管理命令

    app.add_handler(
        CommandHandler(
            "ban",
            ban
        )
    )


    app.add_handler(
        CommandHandler(
            "mute",
            mute
        )
    )


    app.add_handler(
        CommandHandler(
            "unmute",
            unmute
        )
    )


    print("✅ Bot运行中")


    app.run_polling()



# ======================
# 启动
# ======================

if __name__ == "__main__":


    threading.Thread(
        target=run_web,
        daemon=True
    ).start()


    main()
