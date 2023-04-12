from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.create_bot import bot
from keyboards import client_kb, tasks_kb

from GoogleSheets import quickstart

import bot.settings as settings


class RangeNames(StatesGroup):
    add_task = State()
    transform_task = State()
    delete_task = State()
    mark_task = State()


# --- Чтение задач

async def inline_read(message: types.Message):
    g = quickstart.GoogleSheets()
    rows = g.get_tasks()

    if rows:
        rows = [f'{str(index)}.   {task}' for index, task in enumerate(rows, 1)]
        rows = '\n'.join(rows)
    else:
        rows = "Текущих задач нет!\n\nВы можете добавить новую"

    await bot.send_message(chat_id=message.from_user.id, text=rows, reply_markup=client_kb.client_kb)


async def inline_ready_read(message: types.Message):
    g = quickstart.GoogleSheets()

    rows = g.get_ready_tasks()

    if rows:
        rows = [f'{str(index)}.   {task}' for index, task in enumerate(rows, 1)]
        rows = '\n'.join(rows)
    else:
        rows = "Выполненных задач нет!\n\nВы можете переместить задачу из текущих в выполенные"

    await bot.send_message(chat_id=message.from_user.id, text=rows, reply_markup=client_kb.client_kb)


async def inline_tasks(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="Выберите что вы хотите сделать",
                           reply_markup=tasks_kb.tasks_kb)


# --- Добавление новой задачи

async def inline_add(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=callback_query.from_user.id, text="Введите название для задачи")
    await state.set_state(RangeNames.add_task.state)


async def add_answer(message: types.Message, state: FSMContext):
    g = quickstart.GoogleSheets()
    res = g.add_task(range_name=f'A{len(g.get_tasks()) + 2}', _values=[[message.text]])

    await bot.send_message(chat_id=message.from_user.id, text="Задача успешно добавлена!",
                           reply_markup=client_kb.client_kb)
    await state.finish()


# -- Изменение задачи

async def inline_transform(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=callback_query.from_user.id, text="Введите номер задачи, которую хотите"
                                                                     "изменить и новое название через запятую")
    await state.set_state(RangeNames.transform_task.state)


async def transform_answer(message: types.Message, state: FSMContext):
    g = quickstart.GoogleSheets()
    ind, name = message.text.split(',')
    print(ind, name)
    res = g.add_task(range_name=f'A{int(ind) + 1}', _values=[[name]])

    await bot.send_message(chat_id=message.from_user.id, text="Задача успешно изменена!",
                           reply_markup=client_kb.client_kb)
    await state.finish()


# -- Удаление задачи

async def inline_delete(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=callback_query.from_user.id, text="Введите номер задачи, которую хотите"
                                                                     "удалить")
    await state.set_state(RangeNames.delete_task.state)


async def delete_answer(message: types.Message, state: FSMContext):
    g = quickstart.GoogleSheets()
    ind = int(message.text)
    res = g.add_task(range_name=f'A{ind + 1}', _values=[['']])
    rows = g.get_tasks() + ['']
    print(rows)
    res = g.add_task(range_name=f'A{ind + 1}:A{len(rows) + 1}', _values=[[i] for i in g.get_tasks()[ind - 1:]])

    await bot.send_message(chat_id=message.from_user.id, text="Задача успешно удалена!",
                           reply_markup=client_kb.client_kb)
    await state.finish()


def register_inline_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(inline_read, lambda c: c.data == 'read_button')
    dp.register_callback_query_handler(inline_ready_read, lambda c: c.data == 'read_ready_button')
    dp.register_callback_query_handler(inline_tasks, lambda c: c.data == 'update_button')

    dp.register_callback_query_handler(inline_add, lambda c: c.data == 'add_button', state='*')
    dp.register_message_handler(add_answer, state=RangeNames.add_task)

    dp.register_callback_query_handler(inline_transform, lambda c: c.data == 'transform_button', state='*')
    dp.register_message_handler(transform_answer, state=RangeNames.transform_task)

    dp.register_callback_query_handler(inline_delete, lambda c: c.data == 'delete_button', state='*')
    dp.register_message_handler(delete_answer, state=RangeNames.delete_task)
