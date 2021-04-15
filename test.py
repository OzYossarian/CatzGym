import booking
import datetime
import rooms
import users

book_time = datetime.datetime(2021, 4, 22, 16, 30)
booking.book_gym(book_time, 30, None, None, rooms.two, users.teague)
booking.extend_booking(book_time, 60, None, None, rooms.two, users.teague)
