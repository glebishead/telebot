import asyncio
import aiomysql

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def database():
    db = await aiomysql.connect(user='root', password='as1234dflolGG', host='78.36.203.224', db='telegrambot')

    cursor = await db.cursor()

    await cursor.execute('USE telegrambot;')

    await cursor.execute("DESCRIBE users;")
    print(await cursor.fetchall())


    await cursor.execute("SELECT * FROM users;")
    print(await cursor.fetchall())
    await cursor.close()
    try:
        db.close()
        print("connection closed successfully")
    except aiomysql.Error as e:
        print(e)

loop.run_until_complete(database())
