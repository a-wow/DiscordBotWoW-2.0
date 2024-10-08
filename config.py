####################Конфиг персонажей####################
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'base_characters'
}
#########################################################

####################Конфиг дискорд#######################
LEVELS_DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'discord'
}
#########################################################

####################Конфиг сервера#######################
AUTH_DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'base_auth'
}
#########################################################

####################Настройка############################
BOT_TOKEN = 'TOKEN'  # ТОКЕН
CHANNEL_IDS = [1037300019952373773, 1089650230162636992]  # Каналы спамов для первого сообщения, можно добавлять
CHANNEL_IDS1 = [1087440192685740052] # Каналы спамов для второго сообщения, можно добавлять
ADMIN_CHANNEL_ID = 1292829220518629407 # Канал ведомления в канал амдинистрации о покупке предмета
BOT_CHANNEL_ID = 1292818625023049728 # Канал уведомления о включении бота
ALLOWED_CHANNEL_ID = 1292822822414188608 # Канал для разработчиков, с использованием команды !source
VOTE_SERVER_ID = 'ID' # ID mmotop сервера
#########################################################

####################Данные###############################
class_names = {
    1: 'Воин',
    2: 'Паладин',
    3: 'Охотник',
    4: 'Разбойник',
    5: 'Жрец',
    6: 'Рыцарь Смерти',
    7: 'Шаман',
    8: 'Ман',
    9: 'Чернокнижник',
    11: 'Друид',
}

race_names = {
    1: 'Человек',
    2: 'Орк',
    3: 'Дворф',
    4: 'Ночной Эльф',
    5: 'Нежить',
    6: 'Таурен',
    7: 'Гном',
    8: 'Троль',
    10: 'Эльф Крови',
    11: 'Дреней',
}

class_images = {
    1: 'http://alterac-pvp.ru/images/classes/1.png',
    2: 'http://alterac-pvp.ru/images/classes/2.png',
    3: 'http://alterac-pvp.ru/images/classes/3.png',
    4: 'http://alterac-pvp.ru/images/classes/4.png',
    5: 'http://alterac-pvp.ru/images/classes/5.png',
    6: 'http://alterac-pvp.ru/images/classes/6.png',
    7: 'http://alterac-pvp.ru/images/classes/7.png',
    8: 'http://alterac-pvp.ru/images/classes/8.png',
    9: 'http://alterac-pvp.ru/images/classes/9.png',
    11: 'http://alterac-pvp.ru/images/classes/11.png',
}

race_images = {
    (1, 0): 'http://alterac-pvp.ru/images/race/1-0.png',
    (1, 1): 'http://alterac-pvp.ru/images/race/1-1.png',
    (2, 0): 'http://alterac-pvp.ru/images/race/2-0.png',
    (2, 1): 'http://alterac-pvp.ru/images/race/2-1.png',
    (3, 0): 'http://alterac-pvp.ru/images/race/3-0.png',
    (3, 1): 'http://alterac-pvp.ru/images/race/3-1.png',
    (4, 0): 'http://alterac-pvp.ru/images/race/4-0.png',
    (4, 1): 'http://alterac-pvp.ru/images/race/4-1.png',
    (5, 0): 'http://alterac-pvp.ru/images/race/5-0.png',
    (5, 1): 'http://alterac-pvp.ru/images/race/5-1.png',
    (6, 0): 'http://alterac-pvp.ru/images/race/6-0.png',
    (6, 1): 'http://alterac-pvp.ru/images/race/6-1.png',
    (7, 0): 'http://alterac-pvp.ru/images/race/7-0.png',
    (7, 1): 'http://alterac-pvp.ru/images/race/7-1.png',
    (8, 0): 'http://alterac-pvp.ru/images/race/8-0.png',
    (8, 1): 'http://alterac-pvp.ru/images/race/8-1.png',
    (10, 0): 'http://alterac-pvp.ru/images/race/10-0.png',
    (10, 1): 'http://alterac-pvp.ru/images/race/10-1.png',
    (11, 0): 'http://alterac-pvp.ru/images/race/11-0.png',
    (11, 1): 'http://alterac-pvp.ru/images/race/11-1.png',
}
#########################################################
