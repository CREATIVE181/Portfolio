import payments
from default import bot, dp, conn, cursor, bt, owner

from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@dp.message_handler(Command(['start', 'help'], prefixes='!/.', ignore_case=True), chat_type='private')
async def start(message: types.Message):
    if message.from_user.id != owner:
        await message.answer('''
Hello! I'm a test project - a key store for the Steam marketplace.

My work is based on the following modules:
<i>Aiogram</i>
<i>pyQiwiP2P</i>
<i>sqlite3</i>
    
To see the range of products, type /shop''')
    else:
        await message.answer("""
Available commands:

1) /shop - open a shop;
2) /add *game* *price* {enter} *key1|key2|...* – add a product to the catalog;
3) /del *game* – delete a product from the catalog.""")


@dp.message_handler(Command(['shop'], prefixes='!/.', ignore_case=True), chat_type='private')
async def shop(message: types.Message):
    res = bt.page_default(message.from_user.id)
    await message.answer(f'Page {res[0]}/{res[1]}.\nChoose a game:', reply_markup=res[2])


@dp.callback_query_handler(Text(startswith='Pages_'))
async def buttons_tracking(callback: types.CallbackQuery):
    data = callback.data.split('Pages_')[1]
    if data == '➡':
        res = bt.page_up(callback.from_user.id)
        if res is False:
            return await callback.answer()
        await callback.message.edit_text(f'Page {res[0]}/{res[1]}.\nChoose a game:', reply_markup=res[2])
    elif data == '⬅':
        res = bt.page_down(callback.from_user.id)
        if res is False:
            return await callback.answer()
        await callback.message.edit_text(f'Page {res[0]}/{res[1]}.\nChoose a game:', reply_markup=res[2])
    elif data == 'Cancel':
        res = bt.page_return(callback.from_user.id)
        if res is False:
            return await callback.answer()
        await callback.message.edit_text(f'Page {res[0]}/{res[1]}.\nChoose a game:', reply_markup=res[2])
    elif data == 'Remove_buttons':
        bt.page_delete(callback.from_user.id)
        await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(Text(startswith='Game_'))
async def game_buttons(callback: types.CallbackQuery):
    data = callback.data.split('Game_')[1]
    if data == '❌':
        return await callback.answer()
    keys, price = cursor.execute(f'SELECT keys, price FROM games WHERE game = "{data}"').fetchone()
    if keys == '' or keys is None:
        await callback.answer('Sorry, unfortunately, all keys for this game are sold out(', show_alert=True)
        return await callback.answer()
    buttons = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text='Yes', callback_data=f'Conf_Yes_{data}_{keys}_{price}'),
        InlineKeyboardButton(text='No', callback_data=f'Conf_No_{data}_{keys}_{price}'))
    await callback.message.edit_text(f'Are you sure you want to buy <b>{data}</b>?\nThis game costs <b>{price}₽</b>',
                                     reply_markup=buttons)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='Conf_'))
async def purchase_confirmation(callback: types.CallbackQuery):
    zero, data, game, keys, price = callback.data.split("_")
    if data == 'No':
        res = bt.page_return(callback.from_user.id)
        if res is False:
            return await callback.answer()
        await callback.message.edit_text(f'Page {res[0]}/{res[1]}.\nChoose a game:', reply_markup=res[2])
    elif data == 'Yes':
        buttons = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text='QIWI', callback_data=f'Payment_QIWI_{game}_{keys}_{price}'),
            InlineKeyboardButton(text='WebMoney', callback_data=f'Payment_WebMoney_{game}_{keys}_{price}'),
            InlineKeyboardButton(text='PayPal', callback_data=f'Payment_PayPal_{game}_{keys}_{price}'),
            InlineKeyboardButton(text='Cryptocurrency', callback_data=f'Payment_Cryptocurrency_{game}_{keys}_{price}'),
            InlineKeyboardButton(text='Cancel', callback_data=f'Pages_Cancel'))
        await callback.message.edit_text('Select a Payment Method:', reply_markup=buttons)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='Payment_'))
async def payment(callback: types.CallbackQuery):
    zero, data, game, keys, price = callback.data.split("_")
    chat_id = callback.message.chat.id
    result = False
    if data == 'QIWI':
        result = await payments.qiwi(callback, int(price))
    elif data == 'WebMoney':
        await callback.answer('Sorry, while this payment system does not work(\nChoose another payment method!',
                              show_alert=True)
    elif data == 'PayPal':
        await callback.answer('Sorry, while this payment system does not work(\nChoose another payment method!',
                              show_alert=True)
    elif data == 'Cryptocurrency':
        await callback.answer('Sorry, while this payment system does not work(\nChoose another payment method!',
                              show_alert=True)
    if result:
        key, keys = keys.split('|', maxsplit=1)
        cursor.execute(f'UPDATE games SET keys = "{keys}" WHERE game = "{game}"')
        conn.commit()
        bt.page_restart()
        await bot.send_message(chat_id, f"""
Payment was successful!
Here is the key to your game:
<code>{key}</code>""")


@dp.message_handler(Command(['add'], prefixes='!/.', ignore_case=True), chat_type='private')
async def add_product(message: types.Message):
    if message.from_user.id != owner:
        return
    command = message.get_args().split("\n", maxsplit=1)
    res = bt.page_add(command)
    if res is False:
        return await message.answer("Such products are already in the catalog!")
    bt.page_restart()
    await message.answer("Adding to the directory was successful!")


@dp.message_handler(Command(['del'], prefixes='!/.', ignore_case=True), chat_type='private')
async def del_product(message: types.Message):
    if message.from_user.id != owner:
        return
    bt.page_del(message.get_args())
    await message.answer("Removal completed successfully!")


executor.start_polling(dp, skip_updates=True)
