import asyncio
import aiomysql
import time

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def insert_into_users(telegram_id, user_id):

    datetime = (time.strftime(
        time.strftime("%Y-%m-%d", time.localtime())) + ' ' + time.strftime(
        time.strftime("%H:%M:%S", time.localtime())))

    try:
        db = await aiomysql.connect(user='root',
                                    password='as1234dflolGG',
                                    host='78.36.203.224',
                                    db='db')  # connection open

        cursor = await db.cursor()

        await cursor.execute('USE db;')  # selecting db.db

        insert_query = """INSERT INTO users (telegram_id, user_id, regdatetime, is_admin) 
                                        VALUES (%s, %s, %s, %s) """

        dannie = (telegram_id, user_id, datetime , '0')

        await cursor.execute(insert_query, dannie)

        await db.commit()

    except aiomysql.Error as err:
        print(err)

    finally:
        db.close()  # connection close

