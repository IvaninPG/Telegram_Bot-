import telebot
from config import keys, TOKEN
from extensions import ConvertionException, СurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_halp(message: telebot.types.Message):
    text = 'Отправьте сообщение Боту в формате: \n ' \
           '<имя валюты, цену которой хотите узнать>\n' \
           ' <имя валюты, в которой надо узнать цену первой валюты>\n' \
           ' <количество первой валюты>\n' \
           'Пример: Доллар Рубль 10\n'\
           'Список всех доступных валют: /currency'
    bot.reply_to(message, text)

@bot.message_handler(commands=['currency'])
def currency(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n - '.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неправильное количества параметров')

        from_, to_, amount = values
        total_base = СurrencyConverter.convert(from_, to_, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Бот не может обработать команду\n{e}')
    else:
        text = f'Цена {amount} {from_} в {to_} - {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)

