from main import *
import sys

duration = 60
sender = sys.argv[1]
now = datetime.datetime.now()
(booking_minute, booking_hour) = (30, now.hour - 1) if 0 <= now.minute < 30 else (0, now.hour)
booking_time = next_week().replace(hour=booking_hour, minute=booking_minute, second=0, microsecond=0)
save_time = booking_time + datetime.timedelta(days=-7, minutes=duration, microseconds=50)
extend_booking(booking_time, duration, save_time, sender)
