import os
import telebot
import requests
import json
from telebot import types 

bot_id = str(os.getenv('bot'))
API = str(os.getenv('API'))

bot = telebot.TeleBot(bot_id)

Lang = None
message_text = None
city = None
counter = 0
counter_1 = 0

@bot.message_handler(commands=['start', 'settings'])
def main (message):
  global message_text
  global counter 
  counter = 0
  message_text = message.text.strip().lower()
  markup = types.InlineKeyboardMarkup()
  bt1 = types.InlineKeyboardButton('Russia',callback_data='ru')
  bt2 = types.InlineKeyboardButton('English',callback_data='en')
  markup.row(bt1, bt2)
  bot.send_message (message.chat.id, 'Select a language:', reply_markup=markup)
  
  
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callaback):
  global message_text
  global Lang
  
  if callaback.data == 'ru':
    Lang = 'ru'
    bot.delete_message(callaback.message.chat.id, callaback.message.message_id - 1)
    bot.delete_message(callaback.message.chat.id, callaback.message.message_id)
    
  elif callaback.data == 'en':
    Lang = 'en'
    bot.delete_message(callaback.message.chat.id, callaback.message.message_id - 1)
    bot.delete_message(callaback.message.chat.id, callaback.message.message_id)
    
  if Lang == 'ru':
      bot.send_message (callaback.message.chat.id, 'Введите город:')
  elif Lang == 'en':
      bot.send_message (callaback.message.chat.id, 'Enter a city:')
      
      
@bot.message_handler(content_types='text')
def get_weather (message):
  global city
  global counter
  
  markup = types.ReplyKeyboardMarkup()
  if Lang == 'ru':  
    markup.add(types.KeyboardButton('Погода'))
  elif Lang == 'en':
    markup.add(types.KeyboardButton('Weather'))
  
  
  if counter == 0:
    city = message.text.strip()
    counter = 1
  res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
  if res.status_code == 200:
    data = json.loads(res.text)
    if Lang == 'ru':  
      bot.send_message(message.chat.id, f"Погода в городе {city}:\n Температура {data['main']['temp']} °C \n Ощущается как {data['main']['feels_like']} °C \n Ветер {data['wind']['speed']} м/с", reply_markup=markup)
    elif Lang == 'en':
      bot.send_message(message.chat.id, f"Weather in the city {city}:\n Temperature {data['main']['temp']} °C \n It feels like {data['main']['feels_like']} °C \n The Wind {data['wind']['speed']} m/sec", reply_markup=markup)
  else:
    if message.text.lower() != 'погода' or message.text.lower() != 'weather':
      bot.delete_message(message.chat.id, message.message_id)
    if Lang == 'ru':  
      bot.send_message(message.chat.id, "Город указан не верно")
    elif Lang == 'en':
      bot.send_message(message.chat.id, "The city is not listed correctly")
    
if __name__ == '__main__':
  bot.polling(non_stop=True)