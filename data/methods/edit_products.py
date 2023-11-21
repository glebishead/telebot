import asyncio
import aiomysql

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# leave 0 if nothing should be changed
# все кроме is_saled будет изменено, насчет is_saled я еще подумаю как сделать лучше


async def edit_products(Item_ID, key1, game_name, description, categories, images, videos, price, is_saled):
    try:
        lis = [key1, game_name, description, categories, images, videos, price]
        lis1 = ['key1', 'game_name', 'description', 'categories', 'images', 'videos', 'price']
        li = []
        if Item_ID == "0":
            exit("Why Item_ID = 0???")
        n = 0
        for i in lis:
            if lis[n] == '0':
                li.append(n)
            n += 1
        li.reverse()
        n = 0
        for i in li:
            lis.pop(li[n])
            n += 1
        n = 0
        for i in li:
            lis1.pop(li[n])
            n += 1

        connection = await aiomysql.connect(user='root',
                                            password='as1234dflolGG',
                                            host='78.36.203.224',
                                            db='db')  # connection open

        cursor = await connection.cursor()

        await cursor.execute('USE db;')  # selecting db.db

        n = 0
        l = []
        for i in lis1:
            if lis[-1] == lis[n]:
                insert = lis1[n] + " = " + "'" + lis[n] + "'"
                l.append(insert)
                n += 1
            else:
                insert = lis1[n] + " = " + "'" + lis[n] + "'" + ","
                l.append(insert)
                n += 1

        curso = """UPDATE products SET """ + " ".join(l) + """ WHERE `ItemID` = """ + Item_ID + """;"""
        print(curso)
        await cursor.execute(curso)

        await connection.commit()

    except aiomysql.Error as err:
        print(err)

    finally:
        connection.close()

#loop.run_until_complete(edit_products("7",
# "key121", "0", 'desc5435345', "0", 'imagegfgf', 'video000', '15000.99', '0'))