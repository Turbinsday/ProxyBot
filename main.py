import os
from aiogram import types, Bot, Dispatcher, executor
from GetProxies import GetHTTP, GetHTTPS, GetSocks4
import threading

threds = []

bot = Bot('5231843045:AAG6fTCGBbmr_OuQ-n4VPTWsGclsqg-MMAw')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def StartMessage(message: types.Message):
    await message.reply('Здарова! Напиши команду /getproxy и получи бесплатные прокси')


@dp.message_handler(commands =['getproxy'])
async def SendProxy(message: types.Message):

    threading.Thread(target = GetHTTP(chatid=message.from_user.id))
    threading.Thread(target=GetHTTPS(chatid=message.from_user.id))
    threading.Thread(target=GetSocks4(chatid=message.from_user.id))
    await message.answer_document(open(f'{message.from_user.id}HTTP.txt', 'rb'), caption ='Твои HTTP прокси')
    await message.answer_document(open(f'{message.from_user.id}SOCKS4.txt', 'rb'), caption ='Твои Socks4 прокси')
    await message.answer_document(open(f'{message.from_user.id}HTTPS.txt', 'rb'), caption ='Твои HTTPs прокси')
    os.remove(f'{message.from_user.id}HTTP.txt')
    os.remove(f'{message.from_user.id}SOCKS4.txt')
    os.remove(f'{message.from_user.id}HTTPS.txt')


@dp.message_handler()
async def AddToWhiteList(message: types.Message):
    chat_id = str(message.from_user.id)
    with open('chat_ids_file.txt', "a+") as ids_file:
        ids_file.seek(0)
        ids_list = [line.split('\n')[0] for line in ids_file]
        if chat_id not in ids_list:
            ids_file.write(f'{chat_id}\n')
            ids_list.append(message.from_user.id)
            print(f'New chat_id saved: {chat_id}')
            await message.answer("Добро пожаловать! Пищи /getproxy")
        else:
            print(f'chat_id {chat_id} is already saved')
        if message.from_user.id == 1154294686:
            if 'ras' in message.text:
                msg = message.text
                pos = msg.find(' ')
                msgforusers = msg[pos + 1:]
                with open("chat_ids_file.txt", "r") as usids:
                    for line in usids:
                        try:
                            await bot.send_photo(line, photo=types.InputFile('photo.png'), caption=msgforusers,
                                                 parse_mode='html')
                        except:
                            await bot.send_message(line.strip(), msgforusers, parse_mode='html')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

