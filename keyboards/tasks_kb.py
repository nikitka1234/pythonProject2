from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_add = InlineKeyboardButton('Добавить задачу', callback_data='add_button')
button_transform = InlineKeyboardButton('Изменить задачу', callback_data='transform_button')
button_delete = InlineKeyboardButton('Удалить задачу', callback_data='delete_button')
button_mark = InlineKeyboardButton('Отметить выполненную задачу', callback_data='mark_button')
# button_website = InlineKeyboardButton('Сайт', url=WEBSITE_URL)
# button_help = InlineKeyboardButton('Помощь', callback_data='help_button')

# параматр one_time_keyboard=True прячет клавиатуру после того, как пользователь воспользовался ей один раз
tasks_kb = InlineKeyboardMarkup(resize_keyboard=True)
tasks_kb.add(button_add).row(button_transform, button_delete).add(button_mark)
