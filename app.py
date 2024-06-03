import telebot
from config import unit, TOKEN
from extensions import APIException, ExchangeRate

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_start(message: telebot.types.Message):
    """Обработчик сообщений, содержащих команды /start или /help. Отправляет приветствие и инструкции к боту"""
    text = (f'Приветствую, {message.chat.username}!\nЧтобы начать работу введите команду в следующем формате:\n<стартовая валюта>\
    <желаемая валюта>\
    <количество валюты>\nПосмотреть список всех доступных валют можно по команде: /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    """Обработчик сообщений, содержащих команду /values. Отправляет список доступных валют"""
    text = 'Доступные валюты:'
    for key in unit.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    """Обработчик сообщений, содержащих текст запроса. Отправляет результат конвертации валют"""
    try:
        result = message.text.lower()
        values = result.split(' ')

        if len(values) != 3:
            raise APIException('Введено некорректное количество параметров.')

        base, target, amount = values
        total_target = ExchangeRate.get_prise(base, target, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду.\n{e}")
    else:
        text = f'Цена {amount} {base} в {target} - {total_target}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
