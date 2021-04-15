import datetime
import time

root = '/Users/GeorginaTeague/PycharmProjects/CatzGym'


def next_week():
    return datetime.datetime.now() + datetime.timedelta(days=7)


def sleep_until(date_time):
    sleep_time = date_time - datetime.datetime.now()
    time.sleep(sleep_time.total_seconds())


def log(text):
    with open(f'{root}/log.txt', 'a') as f:
        f.write(f'\n{datetime.datetime.now()}: {text}')