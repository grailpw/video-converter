import psycopg2

def saveToPostgres(video):
    try:
        connection = psycopg2.connect(user="postgres", password="123",
                                host="127.0.0.1", port="5432",
                                database="grailpw-video-converter")
    except psycopg2.Error as e:
        return [False, 'Unable to connect!']#print("Ошибка при инициализации PostgreSQL", error)
    #return [True]
    cursor = connection.cursor()
    try:
        insert_query = f'''INSERT INTO videos(name, descr) VALUES('{video.title}', '{video.desc}');'''
        cursor.execute(insert_query)
        connection.commit()
        cursor.close()
        connection.close()
    except psycopg2.Error as e:
        return [False, str(e)]
    return [True]