import asyncio
import aiomysql
import time

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def insert_into_users(user_id):

    datetime = (time.strftime(
        time.strftime("%Y-%m-%d", time.localtime())) + ' ' + time.strftime(
        time.strftime("%H:%M:%S", time.localtime())))

    try:
        connection = await aiomysql.connect(user='root',
                                            password='as1234dflolGG',
                                            host='78.36.203.224',
                                            db='db')  # connection open

        cursor = await connection.cursor()

        await cursor.execute('USE db;')  # selecting db.db

        insert_query = """INSERT INTO users (user_id, regdatetime, is_admin)
                                        VALUES (%s, %s, %s) """

        dannie = (user_id, datetime, '0')

        await cursor.execute(insert_query, dannie)

        await connection.commit()

    except aiomysql.Error as err:
        print(err)

    finally:
        connection.close()

