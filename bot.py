import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = os.environ['TELEGRAM_TOKEN']

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📦 Каталог", callback_data='catalog')],
        [InlineKeyboardButton("💬 Поддержка", callback_data='support')]
    ]
    update.message.reply_text(
        '🛍️ Добро пожаловать в магазин!\n\n'
        'Выберите раздел:',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def catalog(update: Update, context: CallbackContext):
    query = update.callback_query
    products = [
        {"id": 1, "name": "📱 iPhone 13", "price": "1000 руб"},
        {"id": 2, "name": "💻 MacBook Air", "price": "2000 руб"}
    ]
    
    keyboard = []
    for product in products:
        keyboard.append([InlineKeyboardButton(
            f"{product['name']} - {product['price']}", 
            callback_data=f"product_{product['id']}"
        )])
    
    query.edit_message_text(
        "🏪 Наш каталог:\nВыберите товар:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    
    if data == 'catalog':
        catalog(update, context)
    elif data == 'support':
        query.edit_message_text("📞 Напишите нам: @your_support")
    elif data.startswith('product_'):
        product_id = data.split('_')[1]
        query.edit_message_text(f"✅ Товар {product_id} добавлен в заказ!\nМенеджер свяжется с вами.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    
    PORT = int(os.environ.get('PORT', 8443))
    WEBHOOK_URL = os.environ.get('RAILWAY_STATIC_URL', '') + f'/{TOKEN}'
    
    if WEBHOOK_URL:
        updater.start_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=WEBHOOK_URL
        )
    else:
        updater.start_polling()
    
    print("Бот запущен!")
    updater.idle()

if __name__ == '__main__':
    main()
