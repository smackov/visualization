from model import Database


config = {
  'user': 'root',
  'password': 'root',
  'host': 'localhost',
  'database': 'MV'
}

db = Database(**config)

db.show_weeks_short_information()

print(db.show_week_full_information(28))

db.close()