from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import json, os

TOKEN = "7491927850:AAEhqhwu1s94zjIi9MeYyCLWrZNLQXOUJIo"
SETTINGS_FILE = "user_settings.json"

# Загружаем настройки из файла
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        user_settings = json.load(f)
else:
    user_settings = {}

# Сохраняем настройки в файл
def save_settings():
    with open(SETTINGS_FILE, "w") as f:
        json.dump(user_settings, f)

# Главное меню
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton("⚙ Настройка автопокупки", callback_data="autobuy_settings")]
    ])

# Меню автопокупки
def autobuy_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Лимит цены", callback_data="set_price_limit")],
        [InlineKeyboardButton("🎁 Лимит количества", callback_data="set_quantity_limit")],
        [InlineKeyboardButton("🔄 Кол-во циклов", callback_data="set_cycles")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
    ])

# Подменю лимитов
price_limits = [5, 10, 22, 50, 100, 160, 300, 500, 1000, 1500, 2000, 2500, 5000, 10000, 15000, 20000, 30000]
def price_limit_menu():
    keyboard = [[InlineKeyboardButton(f"⭐ {val}", callback_data=f"price_{val}") for val in price_limits[i:i+3]] for i in range(0, len(price_limits), 3)]
    keyboard.append([InlineKeyboardButton("⭐ Убрать лимит", callback_data="remove_price_limit")])
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="autobuy_settings")])
    return InlineKeyboardMarkup(keyboard)

quantity_limits = [500, 1000, 1500, 1999, 2000, 3000, 5000, 7500, 10000, 15000, 25000, 50000, 100000, 250000]
def quantity_limit_menu():
    keyboard = [[InlineKeyboardButton(f"{val}", callback_data=f"quantity_{val}") for val in quantity_limits[i:i+2]] for i in range(0, len(quantity_limits), 2)]
    keyboard.append([InlineKeyboardButton("⭐ Убрать лимит", callback_data="remove_quantity_limit")])
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="autobuy_settings")])
    return InlineKeyboardMarkup(keyboard)

cycle_limits = [1, 2, 3, 5, 10, 20, 30, 50, 75, 100]
def cycle_limit_menu():
    keyboard = [[InlineKeyboardButton(str(val), callback_data=f"cycle_{val}") for val in cycle_limits[i:i+3]] for i in range(0, len(cycle_limits), 3)]
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="autobuy_settings")])
    return InlineKeyboardMarkup(keyboard)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Это бот!", reply_markup=main_menu())

# Обработка кнопок
async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)

    if user_id not in user_settings:
        user_settings[user_id] = {}

    data = query.data

    if data == "back_to_main":
        await query.edit_message_text("Главное меню:", reply_markup=main_menu())

    elif data == "profile":
        settings = user_settings.get(user_id, {})
        text = f"Ваш профиль:\n\n"
        text += f"Лимит цены: ⭐ {settings.get('price_limit', 'не задан')}\n"
        text += f"Лимит подарков: 🎁 {settings.get('quantity_limit', 'не задан')}\n"
        text += f"Циклов автопокупки: 🔄 {settings.get('cycles', 'не задан')}"
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]]))

    elif data == "autobuy_settings":
        await query.edit_message_text("Настройка автопокупки:", reply_markup=autobuy_menu())

    elif data == "set_price_limit":
        await query.edit_message_text("Выбери лимит цены:", reply_markup=price_limit_menu())

    elif data.startswith("price_"):
        price = int(data.split("_")[1])
        user_settings[user_id]["price_limit"] = price
        save_settings()
        await query.edit_message_text(f"Установлен лимит цены: ⭐ {price}", reply_markup=autobuy_menu())

    elif data == "remove_price_limit":
        user_settings[user_id].pop("price_limit", None)
        save_settings()
        await query.edit_message_text("Лимит цены удалён.", reply_markup=autobuy_menu())

    elif data == "set_quantity_limit":
        await query.edit_message_text("Выбери лимит количества подарков:", reply_markup=quantity_limit_menu())

    elif data.startswith("quantity_"):
        quantity = int(data.split("_")[1])
        user_settings[user_id]["quantity_limit"] = quantity
        save_settings()
        await query.edit_message_text(f"Установлен лимит подарков: 🎁 {quantity}", reply_markup=autobuy_menu())

    elif data == "remove_quantity_limit":
        user_settings[user_id].pop("quantity_limit", None)
        save_settings()
        await query.edit_message_text("Лимит подарков удалён.", reply_markup=autobuy_menu())

    elif data == "set_cycles":
        await query.edit_message_text("Выбери количество циклов автопокупки:", reply_markup=cycle_limit_menu())

    elif data.startswith("cycle_"):
        cycles = int(data.split("_")[1])
        user_settings[user_id]["cycles"] = cycles
        save_settings()
        await query.edit_message_text(f"Установлено количество циклов: 🔄 {cycles}", reply_markup=autobuy_menu())

# Запуск приложения (для Render)
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_query))

if __name__ == "__main__":
    app.run_polling()
