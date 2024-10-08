import discord
import mysql.connector
import aiohttp
import os
import sys
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from config import DATABASE_CONFIG, LEVELS_DATABASE_CONFIG, AUTH_DATABASE_CONFIG, BOT_TOKEN, CHANNEL_IDS, CHANNEL_IDS1, ADMIN_CHANNEL_ID, BOT_CHANNEL_ID, ALLOWED_CHANNEL_ID, VOTE_SERVER_ID
from config import class_names, race_names, class_images, race_images

####################Подключение к базам##################
def get_db_connection():
    connection = mysql.connector.connect(
        host=DATABASE_CONFIG['host'],
        user=DATABASE_CONFIG['user'],
        password=DATABASE_CONFIG['password'],
        database=DATABASE_CONFIG['database']
    )
    return connection

def get_levels_db_connection():
    connection = mysql.connector.connect(
        host=LEVELS_DATABASE_CONFIG['host'],
        user=LEVELS_DATABASE_CONFIG['user'],
        password=LEVELS_DATABASE_CONFIG['password'],
        database=LEVELS_DATABASE_CONFIG['database']
    )
    return connection

def get_auth_db_connection():
    connection = mysql.connector.connect(
        host=AUTH_DATABASE_CONFIG['host'],
        user=AUTH_DATABASE_CONFIG['user'],
        password=AUTH_DATABASE_CONFIG['password'],
        database=AUTH_DATABASE_CONFIG['database']
    )
    return connection
#########################################################

####################Инизицализация бота##################
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
#########################################################

####################Запуск ивент бота####################
@bot.event
async def on_ready():
    print(f'Запущен бот {bot.user} (ID: {bot.user.id})')
    print('------')

    await bot.change_presence(activity=discord.Game(name='!cmd - для просмотра команд')) # СТАТУС БОТА
    #await bot.change_presence(activity=discord.Streaming(name='Стримим игру!', url='https://www.twitch.tv/streamer'))  # Потоковая активность
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='какую-то музыку'))  # Слушание
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='фильм'))  # Наблюдение
    bot_channel = bot.get_channel(BOT_CHANNEL_ID)  # ID канала администратора
    if bot_channel:
        await bot_channel.send(f'Бот {bot.user.name} готов к работе!')

    #spam_messages.start()  # Старт спам сообщения
    #spam_messages_2.start() # Старт спам сообщения
#########################################################

####################Спам сообщения#######################
# Первое сообщение
@tasks.loop(minutes=1)  # Промежуток отправки сообщения в минутах
async def spam_messages():
    image_url = "https://bnetcmsus-a.akamaihd.net/cms/blog_header/fl/FLGUSNTX461O1531423284391.jpg"  # Изображение спам-сообщения
    
    description = ("""@everyone это ежедневное сообщение!
вторая строка
третья
4
5
six
seven
IO""")
    for channel_id in CHANNEL_IDS:
        channel = bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(
                title="ТЕСТОВЫЙ СПАМ",
                description=description,
                color=discord.Color.blue()
            )
            embed.set_image(url=image_url)
            embed.set_footer(text="by null")
            await channel.send(embed=embed)

# Второе сообщение
@tasks.loop(minutes=2)  # Промежуток отправки сообщения в минутах
async def spam_messages_2():
    image_url_2 = "https://i.pinimg.com/originals/04/43/67/044367f5557f52ad51b79628c16d7545.jpg"  # Изображение спам-сообщения
    for channel_id in CHANNEL_IDS1:
        channel = bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(
                title="ДРУГОЕ СПАМ СООБЩЕНИЕ",
                description="Это другое сообщение, созданное для тестирования.",
                color=discord.Color.green()
            )
            embed.set_image(url=image_url_2)
            embed.set_footer(text="by null")
            await channel.send(embed=embed)
#########################################################

####################Команда !ping########################
import asyncio

@bot.command(name='ping', help="Пинг бота.")
async def ping(ctx):
    start_time = asyncio.get_event_loop().time()
    await ctx.send("🏓 Понг!")
    end_time = asyncio.get_event_loop().time()

    ping_time = (end_time - start_time) * 1000
    await ctx.send(f"🕒 Время отклика: {ping_time:.2f} мс")
#########################################################

####################Команда !info########################    
@bot.command(name='info', help="Информация о боте")
async def info(ctx):
    embed = discord.Embed(title="", color=discord.Color.blue())
    
    embed.add_field(name="", value=bot.user.name, inline=False)
    embed.add_field(name="Версия", value="1.9.1", inline=False)
    embed.add_field(name="Создатель", value="null", inline=False)
    embed.add_field(name="Отдельная благодарность", value="Linux, Thanos за помощь в разработке бота.", inline=False)
    embed.set_footer(text="by null")

    # Создание кнопки
    button = discord.ui.Button(label="Связаться с разработчиком", url="https://discord.com/users/416812391003586571")

    # Создание view и добавление кнопки в нее
    view = discord.ui.View()
    view.add_item(button)
    
    await ctx.send(embed=embed, view=view)
#########################################################

####################Команда !online######################
@bot.command(name='online', help="Выводит текущее количество онлайн игроков на сервере.")
async def online_players(ctx):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM characters WHERE online = 1")
    online_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT name FROM characters WHERE online = 1")
    online_players = cursor.fetchall()

    cursor.close()
    connection.close()

    if online_players:
        player_names = ', '.join(player[0] for player in online_players)
        await ctx.author.send(f'В настоящее время онлайн {online_count} игрок(ов) на сервере: {player_names}.')
    else:
        await ctx.author.send(f'В настоящее время онлайн {online_count} игрок(ов) на сервере, но игроков нет.')
#########################################################

####################Команда !cmd#########################
@bot.command(name='cmd', help="Выводит информацию о доступных командах.")
async def cmd_info(ctx):
    commands_list = [
        {
            "name": "!account",
            "description": "Отправляет информацию о состоянии аккаунта пользователя."
        },
        {
            "name": "!shop",
            "description": "Получить категории магазина."
        },
        {
            "name": "!vote",
            "description": "Проголосовать за наш сервер и получить монеты."
        },
        {
            "name": "!bind <account>",
            "description": "Привязывает ваш Discord аккаунт к аккаунту WoW."
        },
        {
            "name": "!checkbind",
            "description": "Проверяет, к какому WoW аккаунту привязан ваш Discord аккаунт."
        },
        {
            "name": "!unbind",
            "description": "Отвязывает ваш Discord аккаунт от WoW аккаунта."
        },
        {
            "name": "!characters",
            "description": "Показать персонажей, привязанных к вашему аккаунту WoW."
        },
        {
            "name": "!top",
            "description": "ТОП 5 участников сервера."
        },
        {
            "name": "!online",
            "description": "Выводит текущее количество онлайн игроков на сервере, в личные сообщения."
        },
        {
            "name": "!charinfo <character_name>",
            "description": "Вывод информации о персонаже по его имени."
        },
        {
            "name": "!gm",
            "description": "Показать персонажей администраторов, кто онлайн."
        },
        {
            "name": "!info",
            "description": "Информация о боте."
        },
        {
            "name": "!restart",
            "description": "Перезапускает бота."
        },
        {
            "name": "!cmd",
            "description": "Выводит информацию о доступных командах."
        }
    ]

    embed = discord.Embed(title="Доступные команды", color=discord.Color.blue())
    
    for command in commands_list:
        embed.add_field(name=command["name"], value=command["description"], inline=False)

    embed.set_footer(text="by null")
    
    await ctx.send(embed=embed)
#########################################################

####################Ивент активности#####################
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = message.author.id
    username = message.author.name
    connection = get_levels_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT experience, level, coins FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()

    if result:
        experience, level, coins = result
    else:
        cursor.execute("""
            INSERT INTO users (user_id, experience, level, coins, username) 
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, 0, 1, 0, username))
        experience, level, coins = 0, 1, 0

    experience += 10  # Сколько опыта получают за одно сообщение
    cursor.execute("UPDATE users SET experience = %s WHERE user_id = %s", (experience, user_id))

    cursor.execute("SELECT experience_needed FROM levels WHERE level_id = %s", (level,))
    level_info = cursor.fetchone()

    if level_info and experience >= level_info[0]:
        level += 1  # Поднимаем уровень
        coins += 1  # Начисляем 1 монету за повышение уровня
        cursor.execute("UPDATE users SET level = %s, coins = %s WHERE user_id = %s", (level, coins, user_id))

        # Уведомление о повышении уровня
        embed = discord.Embed(title="Поздравляем!", description=f"{message.author.mention}, вы достигли уровня {level}! Теперь у вас {coins} монет(а).", color=discord.Color.gold())
        embed.set_thumbnail(url=message.author.avatar.url)  # Иконка пользователя
        
        # Загрузить изображение/gif
        embed.set_image(url='https://i.pinimg.com/originals/04/43/67/044367f5557f52ad51b79628c16d7545.jpg')

        await message.channel.send(embed=embed)

    connection.commit()
    cursor.close()
    connection.close()

    await bot.process_commands(message)
#########################################################

####################Команда !account#####################
@bot.command(name='account', help="Отправляет информацию о состоянии аккаунта пользователя.")
async def account_info(ctx):
    user_id = ctx.author.id
    connection = get_levels_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT experience, level, coins FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()

    if result:
        experience, level, coins = result
        
        cursor.execute("SELECT experience_needed FROM levels WHERE level_id = %s", (level,))
        level_info = cursor.fetchone()

        if level_info:
            experience_needed = level_info[0]

            account_info_list = [
                {
                    "name": "Уровень",
                    "value": f"**{level}**"
                },
                {
                    "name": "Текущий опыт",
                    "value": f"**{experience}**"
                },
                {
                    "name": "Опыт, необходимый для следующего уровня",
                    "value": f"**{experience_needed}**"
                },
                {
                    "name": "Монеты",
                    "value": f"**{coins}**"
                },
            ]

            embed = discord.Embed(title="Информация о вашем аккаунте:", color=discord.Color.blue())
            for info in account_info_list:
                embed.add_field(name=info["name"], value=info["value"], inline=False)

        else:
            message = "Не удалось получить информацию о следующем уровне."
            embed = discord.Embed(title="Ошибка", description=message, color=discord.Color.red())

    else:
        embed = discord.Embed(title="Ошибка", description="Вы не зарегистрированы в системе. Пожалуйста, пишите сообщения, чтобы активироваться.", color=discord.Color.red())

    await ctx.author.send(embed=embed)
    cursor.close()
    connection.close()
#########################################################

####################Команда !shop########################
@bot.command(name='shop', help="Показывает доступные товары для покупки.")
async def shop(ctx):
    user_id = ctx.author.id
    connection = get_levels_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()

    view = discord.ui.View()

    cursor.execute("SELECT wow_account_name FROM discord_bindings WHERE discord_user_id = %s", (user_id,))
    result = cursor.fetchone()

    if result:
        wow_account_name = result[0]

        auth_connection = get_auth_db_connection()
        auth_cursor = auth_connection.cursor()

        auth_cursor.execute("SELECT id FROM account WHERE username = %s", (wow_account_name,))
        account_result = auth_cursor.fetchone()

        if account_result:
            account_id = account_result[0]

            char_connection = get_db_connection()
            char_cursor = char_connection.cursor()

            char_cursor.execute("SELECT name FROM characters WHERE account = %s", (account_id,))
            characters = char_cursor.fetchall()

            char_cursor.close()
            char_connection.close()

            if characters:
                character_options = [discord.SelectOption(label=char[0]) for char in characters]
            else:
                await ctx.author.send("На вашем WoW аккаунте нет персонажей.")
                return
        else:
            await ctx.author.send("Не удалось найти ваш аккаунт WoW.")
            return
    else:
        await ctx.author.send("Ваш Discord аккаунт не привязан к аккаунту WoW.")
        return

    for category_id, category_name in categories:
        button = discord.ui.Button(label=category_name, style=discord.ButtonStyle.primary)

        async def button_callback(interaction, category_id=category_id):
            await show_items(interaction, category_id, character_options)

        button.callback = button_callback
        view.add_item(button)

    await ctx.author.send("Выберите категорию товаров:", view=view)

    cursor.close()
    connection.close()


async def show_items(interaction, category_id, character_options):
    user_id = interaction.user.id
    connection = get_levels_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, price FROM items WHERE category_id = %s", (category_id,))
    items = cursor.fetchall()

    if not items:
        await interaction.response.send_message("В этой категории нет доступных товаров.", ephemeral=True)
        return

    item_view = discord.ui.View()

    for item_id, item_name, item_price in items:
        button_label = f"{item_name} - {item_price} монет"
        button = discord.ui.Button(label=button_label, style=discord.ButtonStyle.secondary)

        async def buy_callback(interaction, item_id=item_id):
            await select_character(interaction, item_id, character_options)

        button.callback = buy_callback
        item_view.add_item(button)

    await interaction.response.send_message("Выберите товар для покупки:", view=item_view, ephemeral=True)

    cursor.close()
    connection.close()

async def select_character(interaction, item_id, character_options):
    select = discord.ui.Select(placeholder="Выберите персонажа...", options=character_options)
    
    async def select_callback(interaction):
        selected_character = select.values[0]
        await buy(interaction, item_id, selected_character)

    select.callback = select_callback
    view = discord.ui.View()
    view.add_item(select)

    await interaction.response.send_message("Выберите персонажа для покупки:", view=view)
#########################################################

####################Функция покупки######################
async def buy(interaction, item_id: int, character_name: str):
    user_id = interaction.user.id
    connection = get_levels_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT name, price FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()

    if not item:
        await interaction.response.send_message("Товар не найден.", ephemeral=True)
        cursor.close()
        connection.close()
        return

    item_name, item_price = item

    cursor.execute("SELECT coins FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()

    if not user or user[0] < item_price:
        await interaction.response.send_message("У вас недостаточно монет для покупки этого товара.", ephemeral=True)
        cursor.close()
        connection.close()
        return

    new_coin_balance = user[0] - item_price
    cursor.execute("UPDATE users SET coins = %s WHERE user_id = %s", (new_coin_balance, user_id))

    admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)

    if admin_channel:
        try:
            await admin_channel.send(f"{interaction.user.name} купил(а) {item_name} за {item_price} монет для персонажа: **{character_name}**.")
            print(f"Уведомление отправлено в канал: {item_name} для {character_name}.")
        except discord.Forbidden:
            print(f"Не удалось отправить сообщение в канал с ID {admin_channel.id}. Возможно, у бота нет прав на отправку сообщений в этот канал.")
    else:
        print(f"Канал с ID не найден. Проверьте ID канала.")

    await interaction.response.send_message(f"Вы успешно купили {item_name} за {item_price} монет для {character_name}.", ephemeral=True)

    connection.commit()
    cursor.close()
    connection.close()
#########################################################

####################Команда !vote########################
@bot.command(name='vote', help="Проголосовать за наш сервер и получить монеты.")
async def vote(ctx):
    user_id = ctx.author.id
    username = ctx.author.name
    connection = get_levels_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT last_vote FROM votes WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()

    if result:
        last_vote = result[0]
        if last_vote and datetime.now() < last_vote + timedelta(hours=24):
            button = discord.ui.Button(label="Вы уже проголосовали", style=discord.ButtonStyle.secondary, disabled=True)
            view = discord.ui.View()
            view.add_item(button)
            await ctx.author.send("Вы уже голосовали, повторное голосование доступно через 24 часа.", view=view)
            cursor.close()
            connection.close()
            return

    if result:
        cursor.execute("UPDATE votes SET last_vote = %s WHERE user_id = %s", (datetime.now(), user_id))
    else:
        cursor.execute("INSERT INTO votes (user_id, username, last_vote) VALUES (%s, %s, %s)",
                       (user_id, username, datetime.now()))

    cursor.execute("UPDATE users SET coins = coins + 5 WHERE user_id = %s", (user_id,))  # Начисляем 5 монет
    connection.commit()

    voting_url = f"https://wow.mmotop.ru/servers/{VOTE_SERVER_ID}"

    button = discord.ui.Button(label="Проголосовать здесь!", url=voting_url, style=discord.ButtonStyle.link)
    
    view = discord.ui.View()
    view.add_item(button)

    await ctx.author.send("Спасибо за поддержку! Нажмите кнопку ниже, чтобы проголосовать:", view=view)

    cursor.close()
    connection.close()
#########################################################

####################Команда !top#########################
@bot.command(name='top', help="ТОП 5 участников сервера.")
async def top_users(ctx):
    connection = get_levels_db_connection()
    cursor = connection.cursor()

    # Получаем топ-5 участников по опыту
    cursor.execute("""
        SELECT username, level, experience, coins FROM users 
        ORDER BY experience DESC 
        LIMIT 5
    """)
    top_users = cursor.fetchall()

    cursor.close()
    connection.close()

    if top_users:
        embed = discord.Embed(title="ТОП 5 участников сервера", color=discord.Color.gold())
        
        for idx, (username, level, experience, coins) in enumerate(top_users, start=1):
            embed.add_field(name=f"{idx}. {username}", value=f"Уровень: {level}, Опыт: {experience}, Монеты: {coins}", inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send("Нет доступных пользователей для отображения.")
#########################################################

####################Команда !bind########################
@bot.command(name='bind', help="Привязывает ваш Discord аккаунт к аккаунту WoW.")
async def bind_account(ctx, username: str):
    if ctx.guild:
        await ctx.send("Эта команда доступна только в личных сообщениях.")
        return

    user_id = ctx.author.id
    discord_username = ctx.author.name
    connection = get_auth_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT username FROM account WHERE username = %s", (username,))
    if cursor.fetchone() is None:
        await ctx.send(f"Аккаунт WoW с именем **{username}** не найден.")
        cursor.close()
        connection.close()
        return

    cursor.close()

    connection = get_levels_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM discord_bindings WHERE discord_user_id = %s", (user_id,))
    existing_binding = cursor.fetchone()

    if existing_binding:
        await ctx.send("Ваш Discord аккаунт уже привязан к аккаунту WoW.")
        cursor.close()
        connection.close()
        return

    cursor.execute("SELECT * FROM discord_bindings WHERE wow_account_name = %s", (username,))
    if cursor.fetchone() is not None:
        await ctx.send(f"Аккаунт WoW **{username}** уже привязан к другому Discord аккаунту.")
        cursor.close()
        connection.close()
        return

    cursor.execute(
        "INSERT INTO discord_bindings (discord_user_id, wow_account_name, discord_username) VALUES (%s, %s, %s)",
        (user_id, username, discord_username)
    )
    connection.commit()
    await ctx.send(f"Ваш Discord аккаунт успешно привязан к аккаунту WoW: **{username}**.")

    cursor.close()
    connection.close()
#########################################################

####################Команда !checkbind###################
@bot.command(name='checkbind', help="Проверяет, к какому WoW аккаунту привязан ваш Discord аккаунт.")
async def check_bind(ctx):
    if ctx.guild:
        await ctx.send("Эта команда доступна только в личных сообщениях.")
        return

    user_id = ctx.author.id
    connection = get_levels_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT wow_account_name FROM discord_bindings WHERE discord_user_id = %s", (user_id,))
    result = cursor.fetchone()

    if result:
        wow_account_name = result[0]
        await ctx.send(f"Ваш Discord аккаунт привязан к аккаунту WoW: **{wow_account_name}**.")
    else:
        await ctx.send("Ваш Discord аккаунт не привязан к аккаунту WoW.")

    cursor.close()
    connection.close()
#########################################################

####################Команда !unbind######################
@bot.command(name='unbind', help="Отвязывает ваш Discord аккаунт от WoW аккаунта.")
async def unbind_account(ctx):
    if ctx.guild:
        await ctx.send("Эта команда доступна только в личных сообщениях.")
        return

    user_id = ctx.author.id
    connection = get_levels_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM discord_bindings WHERE discord_user_id = %s", (user_id,))
    result = cursor.fetchone()

    if not result:
        await ctx.send("Ваш Discord аккаунт не привязан к аккаунту WoW.")
    else:
        cursor.execute("DELETE FROM discord_bindings WHERE discord_user_id = %s", (user_id,))
        connection.commit()
        await ctx.send("Ваш Discord аккаунт успешно отвязан от аккаунта WoW.")

    cursor.close()
    connection.close()
#########################################################

####################Команда !characters##################
@bot.command(name='characters', help="Показать персонажей, привязанных к вашему аккаунту WoW.")
async def show_characters(ctx):
    user_id = ctx.author.id
    connection = get_levels_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT wow_account_name FROM discord_bindings WHERE discord_user_id = %s", (user_id,))
    result = cursor.fetchone()

    if result:
        wow_account_name = result[0]

        auth_connection = get_auth_db_connection()
        auth_cursor = auth_connection.cursor()

        auth_cursor.execute("SELECT id FROM account WHERE username = %s", (wow_account_name,))
        account_result = auth_cursor.fetchone()

        if account_result:
            account_id = account_result[0]

            char_connection = get_db_connection()
            char_cursor = char_connection.cursor()

            char_cursor.execute("SELECT name, level, race, class FROM characters WHERE account = %s", (account_id,))
            characters = char_cursor.fetchall()

            if characters:
                embed = discord.Embed(title="Ваши персонажи", color=discord.Color.blue())

                for character in characters:
                    name, level, race_id, class_id = character
                    race_name = race_names.get(race_id, "Неизвестная раса")
                    class_name = class_names.get(class_id, "Неизвестный класс")

                    embed.add_field(name=f"{name}", value=f"Уровень: {level}, Раса: {race_name}, Класс: {class_name}", inline=False)

                await ctx.author.send(embed=embed)
            else:
                await ctx.author.send("На вашем WoW аккаунте нет персонажей.")

            char_cursor.close()
            char_connection.close()
        else:
            await ctx.author.send("Не удалось найти ваш аккаунт WoW.")

        auth_cursor.close()
        auth_connection.close()
    else:
        await ctx.author.send("Ваш Discord аккаунт не привязан к аккаунту WoW.")

    cursor.close()
    connection.close()
#########################################################

####################Команда !charinfo####################
@bot.command()
async def charinfo(ctx, character_name: str):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            c.name, 
            c.level, 
            c.race, 
            c.class, 
            c.gender, 
            c.totalHonorPoints,
            c.arenaPoints,
            c.totalKills,
            (SELECT g.name FROM guild_member gm JOIN guild g ON gm.guildId = g.guildId WHERE gm.guid = c.guid) AS guild_name
        FROM 
            characters c
        WHERE 
            c.name = %s
    """, (character_name,))

    character_info = cursor.fetchone()

    cursor.close()
    connection.close()

    if character_info:
        name, level, race_id, class_id, gender, totalHonorPoints, arenaPoints, totalKills, guild_name = character_info
        gender_str = "Мужчина" if gender == 0 else "Женщина"

        class_image_url = class_images.get(class_id, "https://localhost/default_class.png")
        image_url = race_images.get((race_id, gender), "https://localhost/default.png")

        embed = discord.Embed(title=f"Информация о персонаже: **{name}**", color=discord.Color.blue())
        embed.add_field(name="Уровень", value=f"**{level}**", inline=True)
        #embed.add_field(name="Гендер", value=f"**{gender_str}**", inline=True)
        embed.add_field(name="Гильдия", value=f"**{guild_name if guild_name else 'Нет гильдии'}**", inline=True)
        embed.add_field(name="Хонор", value=f"**{totalHonorPoints}**", inline=False)
        embed.add_field(name="Арена", value=f"**{arenaPoints}**", inline=False)
        embed.add_field(name="Убийств", value=f"**{totalKills}**", inline=False)
        embed.set_thumbnail(url=image_url)  # Изображение расы

        async with aiohttp.ClientSession() as session:
            async with session.get(class_image_url) as resp_race:
                if resp_race.status == 200:
                    embed.set_image(url=class_image_url)  # Изображение класса
                else:
                    embed.set_footer(text="Не удалось загрузить изображение класса.")

        await ctx.send(embed=embed)
    else:
        await ctx.send(f'Упс.. Персонаж {character_name} не найден.')
#########################################################

####################Повышение прав#######################
@bot.command(name='promt', help="Назначает роль пользователю.") # !promt @роль @участник
@commands.has_permissions(administrator=True)
async def assign_role(ctx, role: discord.Role, member: discord.Member = None):
    if member is None:
        member = ctx.author

    try:
        await member.add_roles(role)
        await ctx.send(f"Роль **{role.name}** назначена {member.mention}.")
    except discord.Forbidden:
        await ctx.send("У меня недостаточно прав для назначения этой роли.")
    except discord.HTTPException:
        await ctx.send("Произошла ошибка при назначении роли.")
    except Exception as e:
        await ctx.send(f"Произошла ошибка: {str(e)}")
#########################################################

####################Команда !coins#######################
@bot.command(name='coins', help="Начисляет или удаляет монеты у пользователя. Используйте: !coins @пользователь <количество>")
@commands.has_permissions(administrator=True)
async def modify_coins(ctx, member: discord.Member, amount: int):
    connection = get_levels_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT coins FROM users WHERE user_id = %s", (member.id,))
    result = cursor.fetchone()

    if result:
        current_coins = result[0]
        new_coins = current_coins + amount
        cursor.execute("UPDATE users SET coins = %s WHERE user_id = %s", (new_coins, member.id))
        connection.commit()
        await ctx.send(f"{amount} монет(а) {'добавлено' if amount > 0 else 'удалено'} у {member.mention}. Теперь у него {new_coins} монет.")
    else:
        await ctx.send(f"Не удалось найти пользователя {member.mention}; убедитесь, что он зарегистрирован.")
    
    cursor.close()
    connection.close()
#########################################################

####################Команда !level#######################
@bot.command(name='level', help="Увеличивает или уменьшает уровень у пользователя. Используйте: !level @пользователь <уровень>")
@commands.has_permissions(administrator=True)
async def modify_level(ctx, member: discord.Member, level_change: int):
    connection = get_levels_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT level, experience, coins FROM users WHERE user_id = %s", (member.id,))
    result = cursor.fetchone()

    if result:
        current_level, experience, coins = result
        new_level = current_level + level_change

        if new_level < 1:
            new_level = 1

        cursor.execute("UPDATE users SET level = %s WHERE user_id = %s", (new_level, member.id))
        
        if new_level < current_level:
            new_coins = coins - 1
            if new_coins < 0:
                new_coins = 0
            cursor.execute("UPDATE users SET coins = %s WHERE user_id = %s", (new_coins, member.id))

            await member.send(f"Внимание! Ваш уровень был понижен до {new_level}. У вас теперь {new_coins} монет.")
        elif new_level > current_level:
            new_coins = coins + 1
            cursor.execute("UPDATE users SET coins = %s WHERE user_id = %s", (new_coins, member.id))
            embed = discord.Embed(
                title="Поздравляем!", 
                description=f"{member.mention}, вы достигли уровня {new_level}! Теперь у вас {new_coins} монет(а).", 
                color=discord.Color.gold()
            )
            embed.set_thumbnail(url=member.avatar.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Уровень у {member.mention} остался прежним на уровне {current_level}.")

        connection.commit()
        await ctx.send(f"Уровень у {member.mention} {'повышен' if level_change > 0 else 'понижен'} на {abs(level_change)}. Теперь его уровень {new_level}.")
    else:
        await ctx.send(f"Не удалось найти пользователя {member.mention}; убедитесь, что он зарегистрирован.")

    cursor.close()
    connection.close()
#########################################################

####################Команда !say#########################
@bot.command(name='say', help="Бот повторяет сообщение. Используйте: !say <сообщение>")
@commands.has_permissions(administrator=True)
async def say(ctx, *, message: str):
    await ctx.send(message)

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У вас недостаточно прав для использования этой команды.")
#########################################################

####################Команда !uptime######################
@bot.command(name='uptime', help="Показывает время работы сервера.")
async def uptime(ctx):
    connection = get_auth_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT uptime, maxplayers, starttime FROM uptime ORDER BY starttime DESC LIMIT 1")
    result = cursor.fetchone()

    if result:
        uptime, maxplayers, starttime = result

        uptime_formatted = f"{uptime // 3600}h {(uptime % 3600) // 60}m {uptime % 60}s"
        
        starttime_formatted = datetime.fromtimestamp(starttime).strftime("%Y-%m-%d %H:%M:%S")

        embed = discord.Embed(title="Статистика сервера", color=discord.Color.blue())
        embed.add_field(name="Время работы", value=uptime_formatted, inline=False)
        embed.add_field(name="Максимальное количество игроков", value=maxplayers, inline=False)
        embed.add_field(name="Время запуска", value=starttime_formatted, inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send("Не удалось получить информацию о времени работы сервера.")

    cursor.close()
    connection.close()
#########################################################

####################Команда !restart#####################
@bot.command(name='restart', help="Перезапускает бота.")
@commands.has_permissions(administrator=True)
async def restart_bot(ctx):
    await ctx.send("Перезапуск бота через 5 секунд...")
    await asyncio.sleep(5)
    os.execv(sys.executable, ['python'] + sys.argv)
#########################################################

####################Команда !gm##########################
@bot.command(name='gm', help="Показать персонажей администраторов, кто онлайн.")
async def gm(ctx):
    admin_character_names = ["Alterac", "AdminChar2", "AdminChar3"]  # Имена ГМ персонажей

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM characters WHERE name IN ({}) AND online = 1".format(
        ', '.join(['%s'] * len(admin_character_names))
    ), tuple(admin_character_names))

    online_admin_characters = cursor.fetchall()

    cursor.close()
    connection.close()

    if online_admin_characters:
        online_character_names = ', '.join(char[0] for char in online_admin_characters)
        await ctx.send(f"Сейчас в игре следующие администраторы: {online_character_names}")
    else:
        await ctx.send("В данный момент ни один из администраторов не онлайн.")
#########################################################

####################Команда !server######################
@bot.command(name='server', help="Выводит топ 10 персонажей сервера по уровню из каждой расы.")
async def server_top(ctx):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT name, race, class, level 
        FROM characters 
        WHERE level = 80 
        ORDER BY race, level DESC
    """)
    top_characters = cursor.fetchall()
    
    race_groups = {}
    
    for name, race_id, class_id, level in top_characters:
        if race_id not in race_groups:
            race_groups[race_id] = []
        race_groups[race_id].append((name, class_id))

    embed_list = []
    
    for race_id, characters in race_groups.items():
        race_name = race_names.get(race_id, "Неизвестная раса")
        
        top_characters_of_race = characters[:1] # Генерация по 1 персанжу с каждой расы

        embed = discord.Embed(title=f"Топ {race_name}", color=discord.Color.blue())
        
        for name, class_id in top_characters_of_race:
            class_image_url = class_images.get(class_id, "https://localhost/default_class.png")
            image_url = race_images.get((race_id, 0), "https://localhost/default.png") 

            embed.add_field(name=name, value=" ", inline=False)
            embed.set_thumbnail(url=image_url)  # Изображение расы
            embed.set_image(url=class_image_url)  # Изображение класса

        embed_list.append(embed)

    for embed in embed_list:
        await ctx.send(embed=embed)

    cursor.close()
    connection.close()
#########################################################


bot.run(BOT_TOKEN)
