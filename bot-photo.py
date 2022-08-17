# Импорт переменных
import config, telebot, datetime

from telebot import types

# Добавление токена из файла
bot = telebot.TeleBot(token=config.TOKEN)

# Приветствие
@bot.message_handler(content_types=['text'])
def welcome(message):
    sti = open('/home/tbot/photo/static/miu-nyam-hello.webp','rb')
    # sti = open('e:\\Work\\tbot2\\static\\miu-nyam-hello.webp', 'rb'); #тестовый
    bot.send_sticker(message.chat.id, sti);
    bot.send_message(message.chat.id,"Добро пожаловать! Пожалуйста, назовите ваше ФИО.".format(message.from_user, bot.get_me()),parse_mode='html')
    bot.register_next_step_handler(message, get_fio);

def get_fio(message):
    global fio;
    fio = message.text;

    keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');  # кнопка «Да»
    keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    question = 'Вы  ' + fio + '? Всё верно?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        # код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Запомню : )');
        bot.send_message(call.message.chat.id, 'Добавьте ваше фото.');
        #@bot.message_handler(content_types=['photo']);
        #bot.register_next_step_handler(message, photo);
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Пожалуйста, назовите ваше ФИО.');  # переспрашиваем
        bot.register_next_step_handler(call, get_fio);


    #bot.send_message(message.chat.id,
    #                 "Добро пожаловать, {0.first_name}!\nДобавьте ваше фото.".format(message.from_user, bot.get_me()),
    #                parse_mode='html')


@bot.message_handler(content_types=['photo'])
def photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    #file_patch = "/home/tbot/photo/files/"
    file_patch = "e:\\Work\\tbot2\\photo\\"
    date = datetime.datetime.fromtimestamp(message.date).strftime('%Y%m%d%H%M%S')
    file_name = fio + '_' +  str(date) + '.jpg'
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_patch + file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.chat.id, 'Фото принято. Спасибо за участие!')
    #sti = open('/home/tbot/photo/static/miu-nyam-senks.webp', 'rb')
    sti = open('e:\\Work\\tbot2\\photo\\static\\miu-nyam-senks.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)


#   bot.send_message(message.chat.id, file_patch+file_name)

# Постоянная проверка сообщений
bot.polling(none_stop=True)
