import telebot
from telebot import types
from parsingGenius import find_lyrics_song, get_popularity_songs, find_top_artists
import config
from parsingSpotify import top_artists, top_tracks, greeting
import app
import time

bot = telebot.TeleBot(config.TOKEN_TG)


@bot.message_handler(commands=['start'])
def welcome(message):

    sticker = open('static/welcome_stricker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Your Spotify 🎼")
    item2 = types.KeyboardButton("Lyrics 🎼")
    item3 = types.KeyboardButton("Charts 📊")

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id,
                     "Hi, *" + message.from_user.first_name + "*!\nI am *MusicGeek* bot which can analize your music on Spotify.\n"+
                     "Also I can give you a text of needed song.\nWhat do you want to do?",
                     parse_mode='Markdown',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.chat.type == 'private':
        if message.text == "Your Spotify 🎼":
            global is_user_authorized
            is_user_authorized = False

            # проверка на прохождение пользователем авторизации
            if not is_user_authorized:
                murkup = types.InlineKeyboardMarkup()
                button = types.InlineKeyboardButton(text='Authorize Spotify', url='http://127.0.0.1:5000/')
                murkup.add(button)
                bot.send_message(message.chat.id, "🔑 To do this, let Spotify access your data 🔑", reply_markup=murkup)
                
                is_user_authorized = True

                # инициализирую файл с получением информации об авторизации
                with open("is_finished.txt", 'w') as file:
                    file.write('0')

                # пока пользователь не перейдет по ссылке, бот продолжать работу не будет
                while True:
                    res = ''
                    with open("is_finished.txt", 'r') as file:
                        for line in file:
                            res += line
                    print(res)
                    if res == '1':
                        break

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("〽️ Top artists 〽️")
            item2 = types.KeyboardButton("〽️ Top tracks 〽️")
            markup.add(item1, item2)

            bot.send_message(message.from_user.id, "✅ Authorization was finished successfully! ✅\n\n" + greeting() + "\n\nWhat do you want to do?", reply_markup=markup)
            bot.register_next_step_handler(message, spotify_handler)

        elif message.text == "Lyrics 🎼":
            a = types.ReplyKeyboardRemove()
            bot.send_message(message.from_user.id, '👇 Enter the name of artist 👇', reply_markup=a)
            bot.register_next_step_handler(message, get_artist_song)

        elif message.text == "Charts 📊":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            but2_1 = types.KeyboardButton('Artists Ratings 👨🏼‍🎤')
            but2_2 = types.KeyboardButton('Top songs 🔝')
            markup.add(but2_1, but2_2)

            bot.send_message(message.chat.id,
                             "Here you can watch artists ratings or the most popular songs of any artist.",
                             reply_markup=markup)
            bot.register_next_step_handler(message, genius_top_handler)

        else:
            bot.send_message(message.chat.id, "Incorrect input ❌")

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Your Spotify 🎼")
            item2 = types.KeyboardButton("Lyrics 🎼")
            item3 = types.KeyboardButton("Charts 📊")

            bot.register_next_step_handler(message, start)

    markup.add(item1, item2, item3)

def spotify_handler(message):
    if message.text == '〽️ Top artists 〽️':

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        item1 = types.KeyboardButton("Small 🌑")
        item2 = types.KeyboardButton("Medium 🌓")
        item3 = types.KeyboardButton("Long 🌕")
        item4 = types.KeyboardButton("Back ⤴️")
        item5 = types.KeyboardButton("Main Menu 🏠")

        markup.add(item1, item2, item3, item4, item5)
        bot.send_message(message.chat.id, "Choose the time range: ", reply_markup=markup)
        bot.register_next_step_handler(message, sp_artists_top)
    elif message.text == '〽️ Top tracks 〽️':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        item1 = types.KeyboardButton("Small 🌑")
        item2 = types.KeyboardButton("Medium 🌓")
        item3 = types.KeyboardButton("Long 🌕")
        item4 = types.KeyboardButton("Back ⤴️")
        item5 = types.KeyboardButton("Main Menu 🏠")

        markup.add(item1, item2, item3, item4, item5)
        bot.send_message(message.chat.id, "Choose the time range: ", reply_markup=markup)
        bot.register_next_step_handler(message, sp_tracks_top)
    else:
        bot.send_message(message.chat.id, "Incorrect input, choose the correct one")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("〽️ Top artists 〽️")
        item2 = types.KeyboardButton("〽️ Top tracks 〽️")
        markup.add(item1, item2)

        bot.register_next_step_handler(message, spotify_handler)


def sp_artists_top(message):
    if message.text == "Small 🌑":
        res = top_artists('s')
        bot.send_message(message.chat.id, res)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        item1 = types.KeyboardButton("Small 🌑")
        item2 = types.KeyboardButton("Medium 🌓")
        item3 = types.KeyboardButton("Long 🌕")
        item4 = types.KeyboardButton("Back ⤴️")
        item5 = types.KeyboardButton("Main Menu 🏠")
        markup.add(item1, item2, item3, item4, item5)
        
        bot.send_message(message.chat.id, "What's next❔", reply_markup=markup)
        bot.register_next_step_handler(message, sp_artists_top)

    elif message.text == "Medium 🌓":
        res = top_artists('m')
        
        bot.send_message(message.chat.id, res)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        item1 = types.KeyboardButton("Small 🌑")
        item2 = types.KeyboardButton("Medium 🌓")
        item3 = types.KeyboardButton("Long 🌕")
        item4 = types.KeyboardButton("Back ⤴️")
        item5 = types.KeyboardButton("Main Menu 🏠")
        markup.add(item1, item2, item3, item4, item5)

        bot.send_message(message.chat.id, "What's next❔", reply_markup=markup)
        bot.register_next_step_handler(message, sp_artists_top)
        

    elif message.text == "Long 🌕":
        res = top_artists('l')

        bot.send_message(message.chat.id, res)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        item1 = types.KeyboardButton("Small 🌑")
        item2 = types.KeyboardButton("Medium 🌓")
        item3 = types.KeyboardButton("Long 🌕")
        item4 = types.KeyboardButton("Back ⤴️")
        item5 = types.KeyboardButton("Main Menu 🏠")
        markup.add(item1, item2, item3, item4, item5)

        bot.send_message(message.chat.id, "What's next❔", reply_markup=markup)
        bot.register_next_step_handler(message, sp_artists_top)

    elif message.text == "Back ⤴️":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        item1 = types.KeyboardButton("〽️ Top artists 〽️")
        item2 = types.KeyboardButton("〽️ Top tracks 〽️")
        markup.add(item1, item2)

        bot.send_message(message.chat.id, "What do you want to do ❔", reply_markup=markup)
        bot.register_next_step_handler(message, spotify_handler)

    elif message.text == "Main Menu 🏠":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Your Spotify 🎼")
        item2 = types.KeyboardButton("Lyrics 🎼")
        item3 = types.KeyboardButton("Charts 📊")

        markup.add(item1, item2, item3)

        bot.send_message(message.chat.id, "What do you want to do ❔", reply_markup=markup)
        bot.register_next_step_handler(message, start)

    else:
        bot.send_message(message.chat.id, "Incorrect input ❌")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        item1 = types.KeyboardButton("Small 🌑")
        item2 = types.KeyboardButton("Medium 🌓")
        item3 = types.KeyboardButton("Long 🌕")
        item4 = types.KeyboardButton("Back ⤴️")
        item5 = types.KeyboardButton("Main Menu 🏠")
        markup.add(item1, item2, item3, item4, item5)

        bot.send_message(message.chat.id, "What's next❔", reply_markup=markup)
        bot.register_next_step_handler(message, sp_artists_top)

def sp_tracks_top(message):
    if message.text == "Small 🌑":
        res = top_tracks('s')
        bot.send_message(message.chat.id, res)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        item1 = types.KeyboardButton("Small 🌑")
        item2 = types.KeyboardButton("Medium 🌓")
        item3 = types.KeyboardButton("Long 🌕")
        item4 = types.KeyboardButton("Back ⤴️")
        item5 = types.KeyboardButton("Main Menu 🏠")
        markup.add(item1, item2, item3, item4, item5)
        
        bot.send_message(message.chat.id, "What's next❔", reply_markup=markup)
        bot.register_next_step_handler(message, sp_tracks_top)

    elif message.text == "Medium 🌓":
        res = top_tracks('m')
        
        bot.send_message(message.chat.id, res)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        item1 = types.KeyboardButton("Small 🌑")
        item2 = types.KeyboardButton("Medium 🌓")
        item3 = types.KeyboardButton("Long 🌕")
        item4 = types.KeyboardButton("Back ⤴️")
        item5 = types.KeyboardButton("Main Menu 🏠")
        markup.add(item1, item2, item3, item4, item5)

        bot.send_message(message.chat.id, "What's next❔", reply_markup=markup)
        bot.register_next_step_handler(message, sp_tracks_top)
        

    elif message.text == "Long 🌕":
        res = top_tracks('l')

        bot.send_message(message.chat.id, res)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        item1 = types.KeyboardButton("Small 🌑")
        item2 = types.KeyboardButton("Medium 🌓")
        item3 = types.KeyboardButton("Long 🌕")
        item4 = types.KeyboardButton("Back ⤴️")
        item5 = types.KeyboardButton("Main Menu 🏠")
        markup.add(item1, item2, item3, item4, item5)

        bot.send_message(message.chat.id, "What's next❔", reply_markup=markup)
        bot.register_next_step_handler(message, sp_tracks_top)

    elif message.text == "Back ⤴️":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        item1 = types.KeyboardButton("〽️ Top artists 〽️")
        item2 = types.KeyboardButton("〽️ Top tracks 〽️")
        markup.add(item1, item2)

        bot.send_message(message.chat.id, "What do you want to do ❔", reply_markup=markup)
        bot.register_next_step_handler(message, spotify_handler)

    elif message.text == "Main Menu 🏠":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Your Spotify 🎼")
        item2 = types.KeyboardButton("Lyrics 🎼")
        item3 = types.KeyboardButton("Charts 📊")

        markup.add(item1, item2, item3)

        bot.send_message(message.chat.id, "What do you want to do ❔", reply_markup=markup)
        bot.register_next_step_handler(message, start)

    else:
        bot.send_message(message.chat.id, "Incorrect input ❌")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        item1 = types.KeyboardButton("Small 🌑")
        item2 = types.KeyboardButton("Medium 🌓")
        item3 = types.KeyboardButton("Long 🌕")
        item4 = types.KeyboardButton("Back ⤴️")
        item5 = types.KeyboardButton("Main Menu 🏠")
        markup.add(item1, item2, item3, item4, item5)

        bot.send_message(message.chat.id, "What's next❔", reply_markup=markup)
        bot.register_next_step_handler(message, sp_tracks_top)


def genius_top_handler(message):
    if message.text == 'Artists Ratings 👨🏼‍🎤':
        a = types.ReplyKeyboardRemove()
        result = find_top_artists()
        bot.send_message(message.from_user.id, result, reply_markup=a)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but_1 = types.KeyboardButton('Artists Ratings 👨🏼‍🎤')
        but_2 = types.KeyboardButton('Top songs 🔝')
        but_3 = types.KeyboardButton('Main Menu 🏠')

        markup.add(but_1, but_2, but_3)
        bot.send_message(message.from_user.id, 'What do you want to do next❔', reply_markup=markup)
        bot.register_next_step_handler(message, genius_top_handler)
    elif message.text == 'Top songs 🔝':
        a = types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, '👇 Enter the name of artist 👇', reply_markup=a)
        bot.register_next_step_handler(message, get_artist_top)
    elif message.text == 'Main Menu 🏠':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Your Spotify 🎼")
        item2 = types.KeyboardButton("Lyrics 🎼")
        item3 = types.KeyboardButton("Charts 📊")

        markup.add(item1, item2, item3)

        bot.send_message(message.from_user.id, 'Choose the button.', reply_markup=markup)
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, "Incorrect input ❌")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton('Artists Ratings 👨🏼‍🎤')
        but2 = types.KeyboardButton('Top songs 🔝')
        markup.add(but1, but2)

        bot.register_next_step_handler(message, genius_top_handler)


def artist_name_handler(message):
    a = types.ReplyKeyboardMarkup()
    bot.send_message(message.from_user.id, '👇 Enter the name of artist 👇', reply_markup=a)
    bot.register_next_step_handler(message, get_artist_song)

def get_artist_top(message):
    artist = message.text
    bot.send_message(message.chat.id, 'Wait for a few seconds...')
    try:
        result = get_popularity_songs(artist)
    except Exception:
        print('ERROR')
    bot.send_message(message.chat.id, result)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    but1 = types.KeyboardButton('Top songs 🔝')
    but2 = types.KeyboardButton('Artists Ratings 👨🏼‍🎤')
    but3 = types.KeyboardButton('Main Menu 🏠')

    markup.add(but1, but2, but3)

    bot.send_message(message.chat.id, "What do you want to do next❔", reply_markup=markup)
    bot.register_next_step_handler(message, genius_top_handler)

def get_artist_song(message):
    global art
    art = message.text
    bot.send_message(message.chat.id, '👇 Enter the name of song 👇')
    bot.register_next_step_handler(message, get_genius_lyrics)

def get_genius_lyrics(message):
    song_ = message.text
    bot.send_message(message.chat.id, 'Wait a few seconds...')
    result = find_lyrics_song(art, song_)

    bot.send_message(message.chat.id, result)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    but1 = types.KeyboardButton("Your Spotify 🎼")
    but2 = types.KeyboardButton("Lyrics 🎼")
    but3 = types.KeyboardButton("Charts 📊")
            
    markup.add(but1, but2, but3)
    
    bot.send_message(message.chat.id, "What do you want to do next❔", reply_markup=markup)
    bot.register_next_step_handler(message, start)


# @bot.message_handler(commands=['stop'])
# def stop():
#     bot.polling(none_stop=False)

# RUN
bot.polling(none_stop=True)
