import sqlite3
 
connection = sqlite3.connect("Tracking.db") # или :memory: чтобы сохранить в RAM

cursor = connection.cursor()
 
# Создание таблицы
cursor.execute("""CREATE TABLE countDays (
  day int NOT NULL AUTO_INCREMENT,
  date date DEFAULT NULL,
  number_week int DEFAULT NULL,
  PRIMARY KEY (day)
) 
               """)