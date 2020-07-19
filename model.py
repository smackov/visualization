import mysql.connector
import datetime


class Database():

  date = datetime.date.today()

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
  
  @staticmethod
  def toFixed(numObj, digits=0):
  # Fixed number of float digits after point 
    return f"{numObj:.{digits}f}"

  @staticmethod
  def return_day_if_it_is_none(day):
    if day == None:
      return date.toordinal() - datetime.date(date.year, 1, 1).toordinal() + 1
    return day

  @staticmethod
  def return_number_week_if_it_is_none(number_week):
    if number_week == None:
      return date.strftime('%V')
    return number_week

  def insert_in_tracking(self, task, rate, duration, day = None):
    # Insert in database one completed task
    day = __class__.return_day_if_it_is_none(day)
    query = "INSERT INTO tracking (day, task, rate, duration) VALUES (%s, %s, %s, %s)"
    self.cursor.execute(query, [day, task, rate, duration])
    print('Data has been added!')

  def show_week_full_information(self, number_week=None):
    # Return full information about each day in selected week
    number_week = __class__.return_number_week_if_it_is_none(number_week)
    query = '''SELECT countdays.date, listtasks.name, tracking.duration 
                FROM tracking 
                LEFT JOIN listtasks on tracking.task = listtasks.id 
                LEFT JOIN countdays on tracking.day = countdays.day 
                WHERE countdays.number_week = %s
                ORDER BY countdays.date, tracking.duration DESC;'''
    self.cursor.execute(query, [number_week])
    self.print_infromation_of_days_per(week=number_week, response=self.cursor.fetchall())
   
  def print_infromation_of_days_per(self, week, response):
    # Prints number of week and its duration.
    # For example: 'Number week: 25 -  15 June - 21 June 2020'
    print(f'\n  Week #{week}: {self.get_week_duration(week)}\n')
    # Prints tasks of day with its durations
    number_day, day = response[0][0], []
    for row in response:
      if row[0] == number_day:
        day.append(row)
      else:
        self.print_infromation_of_day(day)
        number_day = row[0]
        day = []
        day.append(row)
  
  @staticmethod
  def print_infromation_of_day(day):
    print(day[0][0].strftime('%A %d %B'), ':')
    index = 1
    total_worked_time = 0
    for task in day:
      print(index, task[1], ':', task[2], 'minutes')
      index += 1
      total_worked_time += task[2]
    print(f'Total time: {total_worked_time // 60} hours {total_worked_time - total_worked_time // 60 * 60} min \n')

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
      print(f'Procantage: {__class__.toFixed(procantage, 0)}% \n')

  # ADDITIONAL FUCTIONS 
  def get_first_day_of_week(self, number_week):
    # Return first day of week like datatime.date instance
    query = '''select date from countdays  
    where number_week = (%s) order by day asc limit 1'''
    self.cursor.execute(query, [(number_week)])
    day = self.cursor.fetchone()
    first_day = day[0]
    return first_day

  def get_week_duration(self, number_week):
    # Return duration of week in format '06 July - 12 July 2020'
    first_day = self.get_first_day_of_week(number_week)
    last_day = first_day + datetime.timedelta(days=6)
    duration_of_week = f'{first_day.strftime("%d %B")} - {last_day.strftime("%d %B %Y")}'
    return duration_of_week

  