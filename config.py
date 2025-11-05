MAX_USERS = 3
MAX_GPT_TOKENS = 120

tokens = []
tokeni = 0

MAX_USER_STT_BLOCKS = 10
MAX_USER_TTS_SYMBOLS = 5000
MAX_USER_GPT_TOKENS = 2000

LOGS = f'logs.txt'
DB_FILE = f'messages.db'
IAM_TOKEN_PATH = f'creds/iam_token.txt'
FOLDER_ID_PATH = f'creds/folder_id.txt'
BOT_TOKEN_PATH = f'creds/bot_token.txt'

SYSTEM_PROMT = [{
    'role': 'system',
    'text': 'Ты весёлый собеседник. Общайся с пользователем на "ты". Общайся как человек и вежливо.'
}]

for_debug_message = '' 
for_debug_code = ''
num = 0