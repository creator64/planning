class TimeCounter:
    def __init__(self, hours=0, minutes=0):
        self.hours = hours
        self.minutes = minutes

    def __bool__(self):
        return self.hours or self.minutes

    def __str__(self):
        return f"{self.hours}h {self.minutes}m"

    def add_time(self, hours=0, minutes=0):
        self.add_hours(hours)
        self.add_minutes(minutes)

    def add_hours(self, hours=0):
        self.hours += hours

    def add_minutes(self, minutes=0):
        self.minutes += minutes
        self.do_minute_check()

    def do_minute_check(self):
        if self.minutes >= 60:
            self.hours += 1
            self.minutes -= 60
            self.do_minute_check()
