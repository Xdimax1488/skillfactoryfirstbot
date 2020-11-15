import telebot

from config import TOKEN, keys

from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите боту команду в формате:\n<имя валюты>' \
           ' <имя валюты в которую конвертируем> ' \
           '<количество исходной валюты>'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def start_help(message: telebot.types.Message):
    text = 'Доступные: \n'
    for key in keys.keys():
        text = text + str(key) + '\n'
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def start_help(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Некорректный ввод параметров')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'ошибка пользователя\n {e}')

    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду\n {e}')
    else:
        total_base = round(total_base, 4)
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)




bot.polling()
