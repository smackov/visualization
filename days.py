"""
    MODUL FOR CREATING LIST OF DATES. 
"""
import datetime

date = datetime.date(year=2020, month=1, day=1) #random date, it's necessary more than current date of request

days = []
delta_day = datetime.timedelta(days=1)

while date.year == 2020:
    number_of_day = date.toordinal() - datetime.date(date.year, 1, 1).toordinal() + 1
    full_date = date.isoformat()
    number_of_week = date.strftime('%V')
    days.append((number_of_day, full_date, number_of_week))
    print(number_of_day, full_date, number_of_week)
    date += delta_day




