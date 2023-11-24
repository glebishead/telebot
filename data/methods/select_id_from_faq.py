import asyncio
import aiomysql

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def select_from_faq(id):
    try:
        db = await aiomysql.connect(user='root',
                                    password='as1234dflolGG',
                                    host='78.36.203.224',
                                    db='db')

        cursor = await db.cursor()

        await cursor.execute('USE db;')

        insert_query = """SELECT questiontext, answertext FROM faq WHERE questionID = '%s';"""

        await cursor.execute(insert_query, id)
        lis = await cursor.fetchall()
        li = lis[0]
        return li

    except aiomysql.Error as err:
        print(err)

    finally:
        db.close()

# print(loop.run_until_complete(select_from_faq(2)))