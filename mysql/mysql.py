import asyncio
import aiomysql
import time

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def database(telegramid, userid):

    y = (time.strftime(time.strftime("%Y-%m-%d", time.localtime())) + ' ' + time.strftime(time.strftime("%H:%M:%S", time.localtime())))

    try:
        db = await aiomysql.connect(user='root',
                                    password='as1234dflolGG',
                                    host='78.36.203.224',
                                    db='telegrambot') # прошу не смотрите на мои пороли ((((

        cursor = await db.cursor()

        await cursor.execute('USE telegrambot;')

        insert_query = """INSERT INTO users (telegaid, userid, regdatetime, isconsumer, isadmin) 
                                        VALUES (%s, %s, %s, %s, %s) """ # не обращайте внимания что тут все желтое так нужно


        dannie = (telegramid, userid, y , '1', '0') # на переменные тоже внимание не обращайте


        await cursor.execute(insert_query, dannie)

        await db.commit() # просто обязательная штука здесь

        cursor.close # вот я хз почему оно желтым горит, но это сука не важно главное работает

    except aiomysql.Error as err: # а это вообще никогда не должно выполняться желательно
        print(err)

    finally:
        db.close() # хз выполняется ли эта строчка, должна закрывать коннект



#loop.run_until_complete(database("14881337", "glebislove"))



# добавить в бд нового пользователя с параметром 2 в isconsumer
# параметр 2 означает (пока что) что пользователь не consumer и не prodavec
