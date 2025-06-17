from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
import logging


TOKEN = "7491927850:AAEhqhwu1s94zjIi9MeYyCLWrZNLQXOUJIo"

logging.basicConfig(level=logging.INFO)

# Хранилище настроек пользователей
user_settings = {}

# Главное меню
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🔧 Настройка автопокупки", callback_data="settings")],
        [InlineKeyboardButton("👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton("🛒 Купить/Продать NFT", callback_data="nft")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Подменю автопокупки
def get_settings_menu():
    keyboard = [
        [InlineKeyboardButton("💰 Лимит цены", callback_data="set_price_limit")],
        [InlineKeyboardButton("🎁 Лимит подарков", callback_data="set_gift_limit")],
        [InlineKeyboardButton("🔁 Циклы покупки", callback_data="set_cycles")],
        [InlineKeyboardButton("✅ Установить и начать", callback_data="start_autobuy")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_price_limit_menu():
    values = [10, 50, 100, 200, 500, 1000]
    keyboard = [[InlineKeyboardButton(f"⭐ {v}", callback_data=f"price_{v}") for v in values[i:i+2]] for i in range(0, len(values), 2)]
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="settings")])
    return InlineKeyboardMarkup(keyboard)

def get_gift_limit_menu():
    values = [500, 1000, 1500, 2000, 3000, 10000]
    keyboard = [[InlineKeyboardButton(f"🎁 {v}", callback_data=f"gift_{v}") for v in values[i:i+2]] for i in range(0, len(values), 2)]
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="settings")])
    return InlineKeyboardMarkup(keyboard)

def get_cycle_menu():
    values = [1, 2, 5, 10, 20, 50]
    keyboard = [[InlineKeyboardButton(f"🔁 {v}", callback_data=f"cycle_{v}") for v in values[i:i+2]] for i in range(0, len(values), 2)]
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="settings")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_settings[update.effective_user.id] = {"price": None, "gift": None, "cycle": None}
    await update.message.reply_text("👋 Привет! Добро пожаловать в бота!", reply_markup=get_main_menu())

async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    await query.answer()

    if data == "settings":
        await query.edit_message_text("⚙️ Настройки автопокупки:", reply_markup=get_settings_menu())

    elif data == "set_price_limit":
        await query.edit_message_text("💰 Выбери лимит цены:", reply_markup=get_price_limit_menu())

    elif data == "set_gift_limit":
        await query.edit_message_text("🎁 Выбери лимит подарков:", reply_markup=get_gift_limit_menu())

    elif data == "set_cycles":
        await query.edit_message_text("🔁 Выбери количество циклов:", reply_markup=get_cycle_menu())

    elif data == "start_autobuy":
        settings = user_settings.get(user_id, {})
        text = (
            f"✅ Запуск автопокупки!\n\n"
            f"⭐ Лимит цены: {settings.get('price')}\n"
            f"🎁 Лимит подарков: {settings.get('gift')}\n"
            f"🔁 Циклы: {settings.get('cycle')}"
        )
        await query.edit_message_text(text, reply_markup=get_main_menu())

    elif data.startswith("price_"):
        value = int(data.split("_")[1])
        user_settings[user_id]["price"] = value
        await query.edit_message_text(f"⭐ Лимит цены установлен: {value}", reply_markup=get_settings_menu())

    elif data.startswith("gift_"):
        value = int(data.split("_")[1])
        user_settings[user_id]["gift"] = value
        await query.edit_message_text(f"🎁 Лимит подарков установлен: {value}", reply_markup=get_settings_menu())

    elif data.startswith("cycle_"):
        value = int(data.split("_")[1])
        user_settings[user_id]["cycle"] = value
        await query.edit_message_text(f"🔁 Циклы установлены: {value}", reply_markup=get_settings_menu())

    elif data == "back_to_main":
        await query.edit_message_text("🏠 Главное меню", reply_markup=get_main_menu())

    elif data == "profile":
        await query.edit_message_text("👤 Ваш профиль пока пуст.", reply_markup=get_main_menu())

    elif data == "nft":
        await query.edit_message_text("🛍 Функция торговли NFT скоро будет доступна.", reply_markup=get_main_menu())

# Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_query))
    app.run_polling()

if __name__ == "__main__":
    main()
