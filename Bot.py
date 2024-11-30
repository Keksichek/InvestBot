from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

# Приветственное сообщение
WELCOME_MESSAGE = (
    "Здравствуй, дорогой инвестор! Этот бот поможет тебе реализовать все твои инвесторские мечты! "
    "Напиши /help, чтобы узнать, как я могу помочь."
)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_MESSAGE)

# Обработчик команды /help
# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Кнопки для помощи
    keyboard = [
        [InlineKeyboardButton("Часто задаваемые вопросы", callback_data="faq")],
        [InlineKeyboardButton("Хочу получить стратегию", callback_data="get_strategy")],
        [InlineKeyboardButton("Хочу отправить запрос на оценку целей", callback_data="send_request")],
        [InlineKeyboardButton("Хочу увидеть Dash", url="http://127.0.0.1:8050/")],  # Добавлена кнопка
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите один из вариантов ниже:", reply_markup=reply_markup)

# Обработчик кнопок из команды /help
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Определение нажатой кнопки
    if query.data == "faq":
        await query.edit_message_text("❓ **Часто задаваемые вопросы:**\n\n(Добавьте текст FAQ здесь.)")
    elif query.data == "get_strategy":
        # Кнопки для выбора срока инвестирования
        strategy_keyboard = [
            [InlineKeyboardButton("На 1 год (Краткосрочная стратегия)", callback_data="short_term")],
            [InlineKeyboardButton("На 1–3 года (Среднесрочная стратегия)", callback_data="mid_term")],
            [InlineKeyboardButton("На 3–5 лет (Долгосрочная стратегия)", callback_data="long_term")],
            [InlineKeyboardButton("На 5+ лет (Высокодоходная долгосрочная стратегия)", callback_data="very_long_term")],
        ]
        reply_markup = InlineKeyboardMarkup(strategy_keyboard)
        await query.edit_message_text(
            "Выберите срок инвестирования, чтобы получить подходящую стратегию:",
            reply_markup=reply_markup
        )
    elif query.data == "send_request":
        # Сообщение с просьбой ввести текст запроса
        await query.edit_message_text("✍️ Пожалуйста, отправьте ваш запрос в текстовом виде.")
        # Сохраняем состояние пользователя
        context.user_data["awaiting_request"] = True

# Обработчик текстовых сообщений (пользователь отправляет запрос)
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Проверяем, ожидается ли запрос
    if context.user_data.get("awaiting_request"):
        # Получаем текст запроса от пользователя
        user_request = update.message.text
        # Обрабатываем запрос (здесь можно добавить логику, например, отправить на почту или в базу данных)
        print(f"Получен запрос: {user_request}")  # Вывод в консоль для проверки

        # Ответ пользователю
        await update.message.reply_text("✉️ Ваш запрос принят! Мы свяжемся с вами в ближайшее время.")
        # Сбрасываем состояние
        context.user_data["awaiting_request"] = False
    else:
        # Если текст отправлен вне контекста
        await update.message.reply_text("Не понимаю, что вы имеете в виду. Напишите /help для списка доступных команд.")

# Стратегии для ответа
STRATEGIES = {
    "short_term": (
        "📈 **Краткосрочная стратегия (до 1 года):**\n\n"
        "Цель: Сохранение капитала с минимальными рисками и получение небольшой доходности.\n\n"
        "Рекомендации:\n"
        "Инструменты:\n"
        "- Депозиты в банках с высокой надежностью (доходность 3–6% годовых).\n"
        "- ОФЗ (облигации федерального займа) с коротким сроком до погашения.\n"
        "- Высоколиквидные ETF на денежный рынок или краткосрочные облигации.\n\n"
        "Риски: Минимальные.\n\n"
        "Портфель:\n"
        "- 60% — банковский депозит.\n"
        "- 30% — краткосрочные облигации.\n"
        "- 10% — ETF на денежный рынок."
    ),
    "mid_term": (
        "📈 **Среднесрочная стратегия (1–3 года):**\n\n"
        "Цель: Умеренное увеличение капитала с относительно низким уровнем риска.\n\n"
        "Рекомендации:\n"
        "Инструменты:\n"
        "- Корпоративные облигации инвестиционного уровня.\n"
        "- Сбалансированные ETF (акции + облигации).\n"
        "- Дивидендные акции крупных компаний (например, «голубые фишки»).\n\n"
        "Риски: Умеренные.\n\n"
        "Портфель:\n"
        "- 40% — корпоративные облигации.\n"
        "- 40% — дивидендные акции.\n"
        "- 20% — сбалансированные ETF."
    ),
    "long_term": (
        "📈 **Долгосрочная стратегия (3–5 лет):**\n\n"
        "Цель: Увеличение капитала за счет стабильного роста рынка.\n\n"
        "Рекомендации:\n"
        "Инструменты:\n"
        "- Индексные фонды (ETF) на акции развивающихся и развитых рынков.\n"
        "- Корпоративные облигации с более высоким риском (но высокой доходностью).\n"
        "- Паи в фондах недвижимости (REITs).\n\n"
        "Риски: Средние.\n\n"
        "Портфель:\n"
        "- 60% — индексные ETF на широкий рынок.\n"
        "- 30% — корпоративные облигации.\n"
        "- 10% — фонды недвижимости."
    ),
    "very_long_term": (
        "📈 **Долгосрочная стратегия (более 5 лет):**\n\n"
        "Цель: Максимизация доходности за счет инвестиций в активы с высоким потенциалом роста.\n\n"
        "Рекомендации:\n"
        "Инструменты:\n"
        "- Акции компаний роста (технологические компании, стартапы).\n"
        "- ETF на рынки с высоким потенциалом (например, Азии или технологий).\n"
        "- Альтернативные инвестиции (золото, криптовалюты — до 5%).\n\n"
        "Риски: Высокие.\n\n"
        "Портфель:\n"
        "- 70% — акции компаний роста.\n"
        "- 20% — ETF на рынки с потенциалом роста.\n"
        "- 10% — золото или другие альтернативные инвестиции."
    ),
}

# Обработчик выбора стратегии
async def strategy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Получение стратегии по ключу
    strategy_key = query.data
    strategy = STRATEGIES.get(strategy_key, "Стратегия не найдена. Попробуйте ещё раз.")
    await query.edit_message_text(strategy, parse_mode="Markdown")

# Основной код
def main():
    # Создаем экземпляр Application с вашим токеном
    application = Application.builder().token("8026798915:AAGGljh6MXg43HKjHEJU_xQGYKq7JPsae6M").build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Регистрация обработчиков кнопок
    application.add_handler(CallbackQueryHandler(button_handler, pattern="^(faq|get_strategy|send_request)$"))
    application.add_handler(CallbackQueryHandler(strategy_handler, pattern="^(short_term|mid_term|long_term|very_long_term)$"))

    # Регистрация обработчика текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
