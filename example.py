import sqlite3

conn = sqlite3.connect("mydatabase.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
# cursor.execute("""CREATE TABLE albums
#                   (title text, artist text, release_date text,
#                    publisher text, media_type text)
#                """)

# Вставляем данные в таблицу
# cursor.execute("""INSERT INTO albums
#                   VALUES ('Glow', 'Andy Hunter', '7/24/2012',
#                   'Xplore Records', 'MP3')"""
#                )

# # Сохраняем изменения
# conn.commit()

# Вставляем множество данных в таблицу используя безопасный метод "?"
# albums = [('Exodus', 'Andy Hunter', '7/9/2002', 'Sparrow Records', 'CD'),
#           ('Until We Have Faces', 'Red', '2/1/2011', 'Essential Records', 'CD'),
#           ('The End is Where We Begin', 'Thousand Foot Krutch', '4/17/2012', 'TFKmusic', 'CD'),
#           ('The Good Life', 'Trip Lee', '4/10/2012', 'Reach Records', 'CD')]

# cursor.executemany("INSERT INTO albums VALUES (?,?,?,?,?)", albums)
# conn.commit()

# new_albums = [('1', '2', '3', '4', '5'),
# ('1', '2', '3', '4', '5'),
# ('1', '2', '3', '4', '5')]

# cursor.executemany("INSERT INTO albums VALUES (?,?,?,?,?)", new_albums)
# conn.commit()

sql = "UPDATE albums SET artist = 'Rome' WHERE artist = '2'"
cursor.execute(sql)
conn.commit()

sql_delete = "DELETE FROM albums WHERE title = 'Exodus'"
cursor.execute(sql_delete)
conn.commit()

sql_request_one = "SELECT release_date FROM albums WHERE artist = ?"
cursor.execute(sql_request_one, [('Red')])
print(cursor.fetchall())
print(cursor.fetchone())

sql_request_two = "SELECT rowid, * FROM albums ORDER BY artist"
cursor.execute(sql_request_two)
for row in cursor.fetchall():
   for text in row:
      print(text, end=', ')
   print()
print('END')

sql_request_three = "SELECT * FROM albums WHERE artist LIKE '%e%'"
cursor.execute(sql_request_three)
for row in cursor.fetchall():
   for text in row:
      print(text, end=', ')
   print()
