from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_read = InlineKeyboardButton('Посмотреть список задач', callback_data='read_button')
button_ready = InlineKeyboardButton('Выполненные задачи', callback_data='read_ready_button')
button_update = InlineKeyboardButton('Обновить задачи', callback_data='update_button')
# button_website = InlineKeyboardButton('Сайт', url=WEBSITE_URL)
# button_help = InlineKeyboardButton('Помощь', callback_data='help_button')

# параматр one_time_keyboard=True прячет клавиатуру после того, как пользователь воспользовался ей один раз
client_kb = InlineKeyboardMarkup(resize_keyboard=True)
client_kb.add(button_read).row(button_ready).add(button_update)  # , button_website).add(button_help)
