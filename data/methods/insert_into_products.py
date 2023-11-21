import asyncio
import aiomysql

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def insert_into_products(key, game_name, description, categories, images, videos, price):
    try:
        connection = await aiomysql.connect(user='root',
                                            password='as1234dflolGG',
                                            host='78.36.203.224',
                                            db='db')  # connection open

        cursor = await connection.cursor()

        await cursor.execute('USE db;')  # selecting db.db

        insert_query = """INSERT INTO products (key1, game_name, description, categories, images, videos, price, is_saled)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """

        dannie = (key, game_name, description, categories, images, videos, price, '0')
        # is_saled  устанавливается 0, т.е нет

        await cursor.execute(insert_query, dannie)

        await connection.commit()

    except aiomysql.Error as err:
        print(err)

    finally:
        await connection.close()

