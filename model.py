import mysql.connector
import datetime
# import days
# import sys
# sys.path.append('/Users/admin/Developer/Python/Playground/Visual')
# import main

date = datetime.date.today()

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

class Database():

  def __init__(self, **config):
    self.db = mysql.connector.connect(**config)
    self.cursor = self.db.cursor()
    self.week_goal_hours = 30
    print('Init!')

  def close(self):
    self.db.close()
    print('Close!')

  def commit(self):
    self.db.commit()
    print('Commit!')

  def insert_in_tracking(self, task, rate, duration, day = None):
    query = "INSERT INTO tracking (day, task, rate, duration) VALUES (%s, %s, %s, %s)"
    if day == None:
      day = date.toordinal() - datetime.date(date.year, 1, 1).toordinal() + 1
    self.cursor.execute(query, [day, task, rate, duration])

  def show_week_full_information(self, number_week=None):
    if number_week == None:
      number_week = date.strftime('%V')
    query = '''SELECT countdays.date, listtasks.name, tracking.duration 
    FROM tracking 
    LEFT JOIN listtasks on tracking.task = listtasks.id 
    LEFT JOIN countdays on tracking.day = countdays.day 
    WHERE countdays.number_week = %s
    ORDER BY countdays.date, tracking.duration DESC;'''
    self.cursor.execute(query, [number_week])
    result = self.cursor.fetchall()

    week_duration = self.get_week_duration(number_week)
    print(f'\n  Week #{number_week}: {week_duration}\n')
    prior_day = datetime.date.min
    index = 1
    total_worked_time = 0
    total_worked_time_for_week = 0
    for record in result:
      if record[0] > prior_day:
        if total_worked_time != 0 :
          print(f'Total time: {total_worked_time // 60} hours {total_worked_time - total_worked_time // 60 * 60} min \n')
          total_worked_time_for_week += total_worked_time
          total_worked_time = 0
        current_day, prior_day = record[0], record[0]
        index = 1
        print(current_day.strftime('%A %d %B'), ':')
      print(index, record[1], ':', record[2], 'minutes')
      total_worked_time += record[2]
      index += 1
    print(f'Total time: {total_worked_time // 60} hours {total_worked_time - total_worked_time // 60 * 60} min \n')
    print(f'Total worked time for week: {total_worked_time_for_week/60} hours')

  def show_weeks_short_information(self):
    "show short information about weeks"
    query = '''SELECT countdays.number_week, SUM(tracking.duration) 
    FROM countdays RIGHT JOIN tracking
    ON countdays.day = tracking.day
    GROUP BY countdays.number_week'''
    self.cursor.execute(query)

    for week_parametrs in self.cursor.fetchall():
      number_week = week_parametrs[0]
      total_time = week_parametrs[1]/60
      procantage = total_time/self.week_goal_hours*100
      week_duration = self.get_week_duration(number_week)
      print(f'\n   Number week: {number_week} -  {week_duration}')
      print(f'Total work time: {total_time} hours')
      print(f'Procantage: {toFixed(procantage, 0)}% \n')



  # ADDITIONAL FUCTIONS 
  def get_first_day_of_week(self, number_week):
    query = '''select date from countdays  
    where number_week = (%s) order by day asc limit 1'''
    self.cursor.execute(query, [(number_week)])
    day = self.cursor.fetchone()
    first_day = day[0]
    return first_day
  
  def get_week_duration(self, number_week):
    first_day = self.get_first_day_of_week(number_week)
    last_day = first_day + datetime.timedelta(days=6)
    duration_of_week = f'{first_day.strftime("%d %B")} - {last_day.strftime("%d %B %Y")}'
    return duration_of_week

  