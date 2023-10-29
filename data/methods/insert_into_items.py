import asyncio
import aiomysql

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def databaseitems(ItemID, key, game_name, description, categories, images, videos, price):
    try:
        db = await aiomysql.connect(user='root',
                                    password='as1234dflolGG',
                                    host='78.36.203.224',
                                    db='db') #connection open

        cursor = await db.cursor()

        await cursor.execute('USE db;') # selecting db.db

        insert_query = """INSERT INTO items (ItemID, key1, game_name, description, categories, images, videos, price, is_saled) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """


        dannie = (ItemID, key, game_name, description, categories, images, videos, price, '0') #is_saled  устанавливается 0, т.е нет


        await cursor.execute(insert_query, dannie)

        await db.commit()

    except aiomysql.Error as err:
        print(err)

    finally:
        db.close() #connection close



#   loop.run_until_complete(databaseitems("4483gdfgdg42422", "ключ228", "названиеredalert3", "описание текстовое", "категорияхз111", "изображение111", "видео111", "15000.99"))

