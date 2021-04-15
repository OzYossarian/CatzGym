from main import *
import sys

duration = 30
sender = sys.argv[1]
now = datetime.datetime.now()
booking_minute = 0 if 0 <= now.minute < 30 else 30
booking_time = next_week().replace(minute=booking_minute, second=0, microsecond=0)
save_time = booking_time + datetime.timedelta(days=-7, minutes=duration, microseconds=50)
book_gym(booking_time, duration, save_time, sender)