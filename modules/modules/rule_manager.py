from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from database import add_rule, get_all_rules, delete_rule

# 定义对话状态
WAITING_KEYWORD, WAITING_DURATION = range(2)

async def start_add_rule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """管理员点击 /addrule 后，提示输入违禁词"""
    context.user_data.clear() # 清空上一次的状态
    await update.message.reply_text("📝 请发送您想要添加的【违禁词】：\n(支持包含空格的中文词组)")
    return WAITING_KEYWORD

async def receive_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """接收用户输入的违禁词，并展示惩罚类型按钮"""
    keyword = update.message.text.strip()
    context.user_data['keyword'] = keyword
    
    keyboard = [
        [InlineKeyboardButton("⚠️ 警告 (Warn)", callback_data="warn")],
        [InlineKeyboardButton("🤐 禁言 (Mute)", callback_data="mute")],
        [InlineKeyboardButton("🔨 封禁 (Ban)", callback_data="ban")]
    ]
    await update.message.reply_text(f"✅ 违禁词已记录：`{keyword}`\n\n请选择对应的惩罚力度：", 
                                    parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    return WAITING_DURATION

async def receive_penalty_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """用户点击惩罚类型后，判断是否需要输入时间"""
    query = update.callback_query
    await query.answer()
    
    penalty_type = query.data
    context.user_data['penalty_type'] = penalty_type
    
    if penalty_type == "ban":
        # 封禁不需要时间，直接入库
        add_rule(context.user_data['keyword'], penalty_type, 0)
        await query.edit_message_text(f"🎉 规则添加成功！\n违禁词: {context.user_data['keyword']}\n惩罚: 永久封禁")
        return ConversationHandler.END
    else:
        # 警告或禁言需要时间
        await query.edit_message_text("⏱️ 请输入惩罚时间（单位：秒）：\n例如：禁言1小时请输入 3600")
        return WAITING_DURATION

async def receive_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """接收时间并入库"""
    try:
        duration = int(update.message.text.strip())
        add_rule(context.user_data['keyword'], context.user_data['penalty_type'], duration)
        await update.message.reply_text(f"🎉 规则添加成功！\n违禁词: {context.user_data['keyword']}\n惩罚: {context.user_data['penalty_type']} ({duration}秒)")
    except ValueError:
        await update.message.reply_text("❌ 时间必须是纯数字！请重新发送秒数。")
        return WAITING_DURATION
        
    return ConversationHandler.END

async def cancel_add_rule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """取消添加"""
    context.user_data.clear()
    await update.message.reply_text("❌ 已取消添加规则。")
    return ConversationHandler.END

async def list_rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """查看规则列表"""
    rules = get_all_rules()
    if not rules:
        await update.message.reply_text("当前没有自定义规则。")
        return
    
    msg = "📜 **当前自定义规则列表：**\n\n"
    for r in rules:
        msg += f"🆔 ID: {r[0]} | 词: `{r[1]}` | 罚: {r[2]} ({r[3]}秒)\n"
    msg += "\n💡 删除规则请使用: /delrule <ID>"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def del_rule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """删除规则"""
    if not context.args:
        await update.message.reply_text("用法: /delrule <规则ID>")
        return
    try:
        delete_rule(int(context.args[0]))
        await update.message.reply_text("🗑️ 规则已删除。")
    except ValueError:
        await update.message.reply_text("ID必须是数字！")
