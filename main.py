import logging
from aiogram import Bot, Dispatcher, executor, types
from sql import SQL
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token='5106843735:AAHjnxzTjxn8ia7noAShsJg-q_OlvGDXSVU')#Обьект бота
storage = MemoryStorage()#Создание хранилища
dp = Dispatcher(bot, storage=storage)#Диспетчер бота
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(filemode='test.log', level=logging.INFO)

#Главное меню
@dp.message_handler(commands='start')
async def keyboard(message: types.message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    text = ['Баланс', 'Зарабатывать']
    keyboard.add(*text)
    await message.answer('test',reply_markup=keyboard)
    sql.add_sql(message.from_user.id, message.from_user.username, connect)

    @dp.message_handler(lambda message: message.text == 'Зарабатывать')
    async def many(message: types.message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = ['Подписаться', 'Просмотры', 'Спам жалобы']
        keyboard.add(*text)
        await message.answer('test1',reply_markup=keyboard)
        #Вывод на экран описание и дальнейшее добавление жалобы
        @dp.message_handler(lambda message: message.text == 'Спам жалобы')
        async def commentar(message: types.message):
            await  MyDialog.answer.set()
            await message.answer('Напишите свою жалобу')
            await  MyDialog.answer.set()
            #Добавление комментария
            @dp.message_handler(state=MyDialog.answer, content_types=types.ContentTypes.TEXT)
            async def add_commentar(message: types.message, state: FSMContext):
                async with state.proxy() as data:
                    data['text'] = message.text
                    user_message = data['text']
                    sql.add_commentar(message.from_user.id, message.from_user.first_name, user_message, connect)
                    await  state.finish()








    #Вывод баланса пользователю
    @dp.message_handler(lambda message: message.text == "Баланс")
    async def balance (message: types.Message):
        balance = sql.balance(message.from_user.id, connect)
        await message.answer(f'Ваш баланс: {balance}')












if __name__ == '__main__':
    class MyDialog(StatesGroup):
        answer = State()
    print("БОТ работает")
    sql = SQL()
    connect = sql.connector()#Соединение с БД #Создать обработку ошибки
    executor.start_polling(dp, skip_updates=True)
