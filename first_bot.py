# -*- coding: utf-8 -*-
import telebot
from telebot import types
from mysql import sql_db
from user import User
import config

user_dict = {}
setting_dict = config.load_settings()

API_TOKEN = setting_dict['api_token']
host = setting_dict['host']
user = setting_dict['user']
password = setting_dict['passwd'] 
db = setting_dict['db']

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def start(message):
    msg = f"Привет, {message.from_user.first_name}!\n Я маленький робот. Только-только делаю первые шаги. Пока могу регистрировать пользователей. Поэтому пиши /reg и я тебя запомню. Может быть..."
    bot.send_message(message.from_user.id, msg);
   
   
@bot.message_handler(commands=['select'])
def start(message):
    select_all_user = sql_db(host, user, password, db).select_all()
    
    msg = select_all_user
    bot.send_message(message.from_user.id, msg);


@bot.message_handler(content_types=['text'])
def reg(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?");
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')
   

def get_name(message): #получаем фамилию
    try:    
        from_user_id = message.from_user.id
        name = message.text
        user = User(name)
        user_dict[from_user_id] = user
        bot.send_message(from_user_id, 'Какая у тебя фамилия?')
        bot.register_next_step_handler(message, get_surname)
    except Exception as e:
        bot.reply_to(message, f'oooops. Error: {e}')

def get_surname(message):
    try:
        from_user_id = message.from_user.id
        surname = message.text
        user = user_dict[from_user_id]
        user.surname = surname
        bot.send_message(from_user_id, 'Сколько тебе лет?')
        bot.register_next_step_handler(message, get_age)
    except Exception as e:
        bot.reply_to(message, f'oooops. Error: {e}')

def get_age(message):
    try:
        from_user_id = message.from_user.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Цифрами, пожалуйста. Сколько тебе лет?')
            bot.register_next_step_handler(msg, get_age)
            return
        user = user_dict[from_user_id]
        user.age = age
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True) #наша клавиатура
        keyboard.add("Да", "Нет")
        question = f'Тебе {str(user.age)} лет, тебя зовут {user.name} {user.surname}?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)            
        bot.register_next_step_handler(message, write_bd)

    except Exception as e:
        bot.reply_to(message, f'oooops. Error: {e}')     

def write_bd(message):
    # try:  
    from_user_id = message.chat.id
    msg = message.text      
    if (msg == u"Да"):            
        user = user_dict[from_user_id]
        sql_db(host, user, password, db).insert_user(user.name, user.surname, user.age)
        bot.send_message(from_user_id, 'Запомнил :)')
    elif (msg == u"Нет"):   
        bot.send_message(from_user_id, 'Не буду запоминать :)')
    else:
        print('Error in definions yes/no')
        raise Exception()
    # except Exception as e:
        # bot.reply_to(message, f'oooops. Error: {e}') 
        
bot.polling(none_stop=True, interval=0)  


if __name__ == '__main__':
    init()