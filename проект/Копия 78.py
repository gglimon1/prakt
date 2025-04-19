import logging
import sqlite3
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, \
    ConversationHandler

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
NAME_STEP = 0
STEP_1, STEP_2, STEP_3, STEP_4, STEP_5 = range(1, 6)  # Шаги обучения инвестора
AWAITING_SUBSCRIPTION = 6

# ID канала для подписки (замените на настоящий ID вашего канала)
CHANNEL_ID = "@loxpidor21"  # например "@your_channel_username"

# URL мини-приложения (замените на URL вашего размещенного приложения)
WEBAPP_URL = "https://your-webapp-url.com"


# Инициализация базы данных
def init_db():
    """Инициализирует базу данных для хранения информации о пользователях"""
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        click_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()
    logger.info("База данных инициализирована")


# Сохранение пользователя в базу данных
def save_user_to_db(user_id, username, first_name, last_name):
    """Сохраняет информацию о пользователе в базу данных"""
    conn = sqlite3.connect('bot_users.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT OR IGNORE INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)',
        (user_id, username, first_name, last_name)
    )
    conn.commit()
    conn.close()
    logger.info(f"Пользователь {user_id} сохранен в базе данных")


async def check_subscription(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
    """Проверяет, подписан ли пользователь на канал"""
    try:
        chat_member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return chat_member.status in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.CREATOR]
    except Exception as e:
        logging.error(f"Ошибка при проверке подписки: {e}")
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    save_user_to_db(user.id, user.username, user.first_name, user.last_name)

    keyboard = [
        [
            InlineKeyboardButton("УМЕЮ", callback_data='can_do'),
            InlineKeyboardButton("ОБУЧЕНИЕ", callback_data='training'),
            InlineKeyboardButton("СТАТЬ ИНВЕСТОРОМ", callback_data='become_investor')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Добро пожаловать, {user.first_name}! Выберите действие:",
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()

    if query.data == 'can_do':
        # Кнопка УМЕЮ - проверяем подписку на канал
        is_subscribed = await check_subscription(context, query.from_user.id)

        if not is_subscribed:
            # Если не подписан, предлагаем подписаться
            keyboard = [
                [InlineKeyboardButton("Подписаться на канал", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")],
                [InlineKeyboardButton("Я подписался", callback_data='check_subscription_can_do')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                text="Для использования этой функции необходимо подписаться на наш канал.",
                reply_markup=reply_markup
            )

            # Сохраняем информацию о том, какую функцию пользователь хотел использовать
            context.user_data['after_subscription'] = 'can_do'
            return AWAITING_SUBSCRIPTION
        else:
            # Если подписан, открываем мини-приложение
            keyboard = [
                [InlineKeyboardButton("ОТКРЫТЬ ПРИЛОЖЕНИЕ", web_app=WebAppInfo(url=WEBAPP_URL))],
                [InlineKeyboardButton("← Назад", callback_data='back_to_main')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                text="Нажмите кнопку ниже, чтобы открыть приложение для инвесторов:",
                reply_markup=reply_markup
            )

    elif query.data == 'training':
        # Кнопка ОБУЧЕНИЕ
        keyboard = [
            [InlineKeyboardButton("ОТКРЫТЬ ПРИЛОЖЕНИЕ", web_app=WebAppInfo(url=WEBAPP_URL))],
            [InlineKeyboardButton("Начать обучение", callback_data='start_training')],
            [InlineKeyboardButton("← Назад", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="Вы можете сразу открыть приложение или пройти обучение для начинающих инвесторов:",
            reply_markup=reply_markup
        )

    elif query.data == 'start_training':
        # Начало обучения инвестора
        keyboard = [
            [InlineKeyboardButton("Далее →", callback_data='step_2')],
            [InlineKeyboardButton("← Назад", callback_data='training')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="Шаг 1 из 5: Базовые понятия инвестирования.\n\n"
                 "Инвестирование - это вложение денег с целью получения прибыли. "
                 "Основные термины, которые вам нужно знать: акции, облигации, фонды, дивиденды и т.д.",
            reply_markup=reply_markup
        )
        return STEP_1

    elif query.data == 'step_2':
        keyboard = [
            [InlineKeyboardButton("Далее →", callback_data='step_3')],
            [InlineKeyboardButton("← Назад", callback_data='start_training')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="Шаг 2 из 5: Типы инвестиционных инструментов.\n\n"
                 "Существуют различные инструменты для инвестирования: акции, облигации, "
                 "ETF, недвижимость, криптовалюта и другие. Каждый имеет свой риск и потенциальную доходность.",
            reply_markup=reply_markup
        )
        return STEP_2

    elif query.data == 'step_3':
        keyboard = [
            [InlineKeyboardButton("Далее →", callback_data='step_4')],
            [InlineKeyboardButton("← Назад", callback_data='step_2')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="Шаг 3 из 5: Стратегии инвестирования.\n\n"
                 "Разные стратегии подходят для разных целей: долгосрочное инвестирование, "
                 "пассивное инвестирование, активная торговля, диверсификация портфеля и т.д.",
            reply_markup=reply_markup
        )
        return STEP_3

    elif query.data == 'step_4':
        keyboard = [
            [InlineKeyboardButton("Далее →", callback_data='step_5')],
            [InlineKeyboardButton("← Назад", callback_data='step_3')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="Шаг 4 из 5: Управление рисками.\n\n"
                 "Инвестирование всегда связано с риском. Важно понимать свой риск-профиль, "
                 "диверсифицировать вложения и иметь подушку безопасности.",
            reply_markup=reply_markup
        )
        return STEP_4

    elif query.data == 'step_5':
        keyboard = [
            [InlineKeyboardButton("ОТКРЫТЬ ПРИЛОЖЕНИЕ", web_app=WebAppInfo(url=WEBAPP_URL))],
            [InlineKeyboardButton("← Назад", callback_data='step_4')],
            [InlineKeyboardButton("В главное меню", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="Шаг 5 из 5: Начало инвестирования.\n\n"
                 "Теперь вы готовы начать! Выберите брокера, откройте счет и начните с небольших сумм. "
                 "Продолжайте обучаться и анализировать свои решения.\n\n"
                 "Поздравляем с завершением базового обучения! Теперь вы можете открыть приложение и начать практиковаться.",
            reply_markup=reply_markup
        )
        return STEP_5

    elif query.data == 'become_investor':
        # Кнопка СТАТЬ ИНВЕСТОРОМ
        is_subscribed = await check_subscription(context, query.from_user.id)

        if not is_subscribed:
            # Если не подписан, предлагаем подписаться
            keyboard = [
                [InlineKeyboardButton("Подписаться на канал", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")],
                [InlineKeyboardButton("Я подписался", callback_data='check_subscription_investor')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                text="Для того чтобы стать инвестором, необходимо подписаться на наш канал.",
                reply_markup=reply_markup
            )

            # Сохраняем информацию о том, какую функцию пользователь хотел использовать
            context.user_data['after_subscription'] = 'become_investor'
            return AWAITING_SUBSCRIPTION
        else:
            # Форма для заполнения имени
            keyboard = [
                [InlineKeyboardButton("← Назад", callback_data='back_to_main')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                text="Для регистрации в качестве инвестора, введите ваше имя:",
                reply_markup=reply_markup
            )
            return NAME_STEP

    elif query.data.startswith('check_subscription_'):
        # Обработка проверки подписки
        type_after_subscription = query.data.replace('check_subscription_', '')

        is_subscribed = await check_subscription(context, query.from_user.id)

        if is_subscribed:
            # Если пользователь подписался, выполняем нужное действие
            if type_after_subscription == 'can_do' or context.user_data.get('after_subscription') == 'can_do':
                keyboard = [
                    [InlineKeyboardButton("ОТКРЫТЬ ПРИЛОЖЕНИЕ", web_app=WebAppInfo(url=WEBAPP_URL))],
                    [InlineKeyboardButton("← Назад", callback_data='back_to_main')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await query.edit_message_text(
                    text="Спасибо за подписку! Теперь вы можете использовать все возможности бота.",
                    reply_markup=reply_markup
                )
            elif type_after_subscription == 'investor' or context.user_data.get(
                    'after_subscription') == 'become_investor':
                keyboard = [
                    [InlineKeyboardButton("← Назад", callback_data='back_to_main')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await query.edit_message_text(
                    text="Для регистрации в качестве инвестора, введите ваше имя:",
                    reply_markup=reply_markup
                )
                return NAME_STEP
        else:
            # Если пользователь все еще не подписался
            keyboard = [
                [InlineKeyboardButton("Подписаться на канал", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")],
                [InlineKeyboardButton("Я подписался", callback_data=f'check_subscription_{type_after_subscription}')],
                [InlineKeyboardButton("← Назад", callback_data='back_to_main')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                text="Вы все еще не подписаны на наш канал. Пожалуйста, подпишитесь для продолжения.",
                reply_markup=reply_markup
            )
            return AWAITING_SUBSCRIPTION

    elif query.data == 'back_to_main':
        # Возврат в главное меню
        keyboard = [
            [
                InlineKeyboardButton("УМЕЮ", callback_data='can_do'),
                InlineKeyboardButton("ОБУЧЕНИЕ", callback_data='training'),
                InlineKeyboardButton("СТАТЬ ИНВЕСТОРОМ", callback_data='become_investor')
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="Главное меню. Выберите действие:",
            reply_markup=reply_markup
        )
        return ConversationHandler.END


async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ввода имени"""
    name = update.message.text
    user_id = update.effective_user.id

    # Здесь можно сохранить имя пользователя в базу данных или context
    context.user_data['investor_name'] = name

    keyboard = [
        [InlineKeyboardButton("ОТКРЫТЬ ПРИЛОЖЕНИЕ", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("В главное меню", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Спасибо, {name}! Вы успешно зарегистрированы как инвестор.\n"
        f"Теперь вы можете открыть приложение и начать инвестировать!",
        reply_markup=reply_markup
    )
    return ConversationHandler.END


def main() -> None:
    """Запуск бота"""
    # Инициализация базы данных
    init_db()

    # Создание Application
    application = Application.builder().token("7779673246:AAH9iSDfkC2NLNeDebyvgMhUquhnhcQrEcs").build()

    # Создание ConversationHandler для обработки диалогов
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CallbackQueryHandler(button_handler)
        ],
        states={
            NAME_STEP: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name),
                CallbackQueryHandler(button_handler)
            ],
            STEP_1: [CallbackQueryHandler(button_handler)],
            STEP_2: [CallbackQueryHandler(button_handler)],
            STEP_3: [CallbackQueryHandler(button_handler)],
            STEP_4: [CallbackQueryHandler(button_handler)],
            STEP_5: [CallbackQueryHandler(button_handler)],
            AWAITING_SUBSCRIPTION: [CallbackQueryHandler(button_handler)],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    application.add_handler(conv_handler)

    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()