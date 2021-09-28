from plannings.time.timedicts import *

def timestr_with_weekday(date):
    return f"{DayDict[date.weekday()]} {date.day} {MonthDict[date.month]}"
