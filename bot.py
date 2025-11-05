import telebot
from creds import get_bot_token
from config import MAX_USER_TTS_SYMBOLS, tokens, for_debug_code, num, tokeni
from speechkit import text_to_speech, speech_to_text
from yandex_gpt import ask_gpt, count_tokens, status_check
from database import create_database, add_messages, select_last_messages, count_all_limits, count_users

bot = telebot.TeleBot(get_bot_token())
create_database()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Бот поможет найти ответ на нужный вопрос и расшифровать текст в войсе или сделать голосовое сообщение из заданного текста.\nНажмите /help для просмотра команд')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '- /start - перезапуск бота\n- /stt - войс в текст\n- /tts - текст в войс\n- /help - помощь\n- /text - написать текстовое сообщение\n- /voice - записать войс\n- /debug - режим отладки')

@bot.message_handler(commands=['debug'])
def debug(message):
    with open('logs.txt', 'rb') as f:
        bot.send_document(message.chat.id, f)

@bot.message_handler(commands=['tts'])
def tts_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправь следующим сообщеним текст, чтобы я его озвучил!')
    bot.register_next_step_handler(message, tts)

def tts(message):
    global for_debug_code
    global tokeni
    global num
    num += 1
    user_id = message.from_user.id
    text = message.text
    if message.content_type != 'text':
        bot.send_message(user_id, 'Отправь текстовое сообщение')
        return
    status_code = status_check('a')
    for_debug_code += f'{num}) {str(status_code)}\n'
    status, content = text_to_speech(text)
    tokens.append(len(text))
    if status and sum(tokens) <= 250:
        bot.send_voice(user_id, content)
    else:
        bot.send_message(user_id, 'Вы израсходовали все токены')

@bot.message_handler(commands=['stt'])
def stt_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправь голосовое сообщение, чтобы я его распознал!')
    bot.register_next_step_handler(message, stt)

def stt(message):
    global num
    global for_debug_code
    global tokeni
    num += 1
    user_id = message.from_user.id
    if not message.voice:
        return
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)
    status_code = status_check('a')
    for_debug_code += f'{num}) {str(status_code)}\n'
    status, text = speech_to_text(file)
    tokens.append(len(text))
    if status and sum(tokens) <= 250:
        bot.send_message(user_id, text)
    else:
        bot.send_message(user_id, f'{text} Вы израсходовали все токены')

@bot.message_handler(commands=['text'])
def text_handler(message):
    bot.send_message(message.chat.id, 'Напишите запрос')
    bot.register_next_step_handler(message, text)
def text(message):
    global num
    global for_debug_code
    global tokeni
    num += 1
    status_code = status_check('a')
    for_debug_code += f'{num}) {str(status_code)}\n'
    result = ask_gpt(message.text)
    tokeni += count_tokens(message.text)
    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=['voice'])
def voice_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Отправь голосовое сообщение, чтобы я его распознал!')
    bot.register_next_step_handler(message, voice)

def voice(message):
    global num
    global for_debug_code
    global tokeni
    num += 1
    status_code = status_check('a')
    for_debug_code += f'{num}) {str(status_code)}\n'
    user_id = message.from_user.id
    if not message.voice:
        return
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)
    status, text = speech_to_text(file)
    tokens.append(len(text))
    result = ask_gpt(text)
    tokeni += count_tokens(text)
    status, content = text_to_speech(result)
    tokens.append(len(text))
    bot.send_voice(message.chat.id, content)

bot.infinity_polling()