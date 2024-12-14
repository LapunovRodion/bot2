from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters

# Стейты для диалога
GET_FIO, GET_PHONE, GET_REVIEW = range(3)

# Идентификатор чата
CHAT_FLUD = -1002427401226  # ID чата "Флуд"
THREAD_REVIEW = 100           # ID темы "Отзывы"

# Команда /start
async def start(update: Update, context):
    welcome_message = (
        "Добро пожаловать в кафе «Грюнвальд».\n\n"
        "Здесь вы можете оставить свои пожелания, предложения или замечания. "
        "Мы последовательно запросим ваши данные.\n\n"
        "Введите ваше ФИО:"
    )
    await update.message.reply_text(welcome_message)
    return GET_FIO

# Обработка ФИО
async def get_fio(update: Update, context):
    fio = update.message.text
    context.user_data['fio'] = fio
    await update.message.reply_text("Спасибо! Теперь введите ваш номер телефона:")
    return GET_PHONE

# Обработка номера телефона
async def get_phone(update: Update, context):
    phone = update.message.text
    context.user_data['phone'] = phone
    await update.message.reply_text("Отлично! Теперь оставьте ваш отзыв:")
    return GET_REVIEW

# Обработка отзыва
async def get_review(update: Update, context):
    review = update.message.text
    context.user_data['review'] = review

    # Формируем сообщение для отправки
    summary_message = (
        f"ФИО: {context.user_data['fio']}\n"
        f"Номер телефона: {context.user_data['phone']}\n"
        f"Отзыв: {review}"
    )

    # Отправляем сообщение в чат THREAD_REVIEW
    await send_to_review_chat(summary_message, context)
    await update.message.reply_text("Спасибо за ваш отзыв!")
    return ConversationHandler.END

# Функция отправки сообщений в чат THREAD_REVIEW
async def send_to_review_chat(message, context):
    await context.bot.send_message(chat_id=CHAT_FLUD, text=message, message_thread_id=THREAD_REVIEW)

# Завершение диалога
async def cancel(update: Update, context):
    await update.message.reply_text("Действие отменено.")
    return ConversationHandler.END

# Основная функция
def main():
    TOKEN = "7823692141:AAE8mz7hOrp3KxhPKys6JjiEpoY00IR7xfE"

    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Создание ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GET_FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fio)],
            GET_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            GET_REVIEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_review)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Регистрируем обработчики
    application.add_handler(conv_handler)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()