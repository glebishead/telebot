import asyncio
import aiomysql

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def edit_users(user_id, is_admin):
    try:
        connection = await aiomysql.connect(user='root',
                                            password='as1234dflolGG',
                                            host='78.36.203.224',
                                            db='db')  # connection open

        cursor = await connection.cursor()

        await cursor.execute('USE db;')  # selecting db.db

        insert_query = """UPDATE users SET is_admin = %s WHERE user_id = %s;"""

        dannie = (is_admin, user_id)

        await cursor.execute(insert_query, dannie)

        await connection.commit()

    except aiomysql.Error as err:
        print(err)

    finally:
        await connection.close()

