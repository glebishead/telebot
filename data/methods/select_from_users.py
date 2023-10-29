import asyncio
import aiomysql

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def select_from_users():
    try:
        db = await aiomysql.connect(user='root',
                                    password='as1234dflolGG',
                                    host='78.36.203.224',
                                    db='db')

        cursor = await db.cursor()

        await cursor.execute('USE db;')

        await cursor.execute("SELECT * FROM users;")
        return await cursor.fetchall()

    except aiomysql.Error as err:
        print(err)

    finally:
        db.close()

loop.run_until_complete(select_from_users())