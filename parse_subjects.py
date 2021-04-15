# Designed to run OUTSIDE of conda environment.
import os
import sys
import datetime

root = '/Users/GeorginaTeague/PycharmProjects/CatzGym'
key = 'Book Catz Gym:'
cron_day = {
        'SU': 0, 'SUN': 0,
        'M': 1, 'MO': 1, 'MON': 1,
        'TU': 2, 'TUE': 2,
        'W': 3, 'WE': 3, 'WED': 3,
        'TH': 4, 'THU': 4,
        'F': 5, 'FR': 5, 'FRI': 5,
        'SA': 6, 'SAT': 6,
    }


class CronTime():
    def __init__(self, minute, hour, day_of_month, month, day_of_week):
        self.minute = minute
        self.hour = hour
        self.day_of_month = day_of_month
        self.month = month
        self.day_of_week = day_of_week

    def __str__(self):
        parts = [self.minute, self.hour, self.day_of_month, self.month, self.day_of_week]
        return ' '.join(['*' if x is None else str(x) for x in parts])


def job_command(script, sender):
    return f'conda activate CatzGym && python3 ~/PycharmProjects/CatzGym/{script} {sender} && conda deactivate'


def log(text):
    with open(f'{root}/log.txt', 'a') as f:
        f.write(f'\n{datetime.datetime.now()}: {text}')


def parse_subjects(subject_filename):
    log(f'Parsing subjects: {subject_filename}')
    with open(f'{root}/subject_files/{subject_filename}', 'r') as subject_file:
        lines = subject_file.readlines()
        (subjects, senders) = ([x.upper for x in lines[::2]], lines[1::2])
        for (subject, sender) in zip(subjects, senders):
            key_start = subject.find(key.upper())
            if key_start != -1:
                data = subject[key_start + len(key):].strip()
                [date, time, duration] = [x.strip() for x in data.split(',')]
                schedule_jobs(date, time, duration, sender.strip())


def schedule_jobs(date, time, duration, sender):
    log(f'Scheduling jobs: {date}, {time}, {duration}, {sender}')
    try:
        booking_time = datetime.datetime.strptime(f'{date} {time}', '%d/%m/%Y %H:%M')
        job_minute = (booking_time.minute + 30 - 1)
        cron_date = (booking_time - datetime.timedelta(days=7))
        cron_time = CronTime(job_minute, booking_time.hour, cron_date.day, cron_date.month, None)
    except ValueError:
        booking_time = datetime.datetime.strptime(time, '%H:%M')
        job_minute = (booking_time.minute + 30 - 1)
        days = ','.join([str(cron_day[x.strip().upper()]) for x in date.split(' ')])
        cron_time = CronTime(job_minute, booking_time.hour, None, None, days)
    duration = int(duration)

    # Always book for 30 mins first:
    log(f'Scheduling 30 min job...')
    command = job_command('half_hour.py', sender)
    log(f'Cron command: {command}')
    add_cron_job(command, cron_time)

    # Then extend to one hour if necessary
    if duration == 60:
        log(f'Extending to 60 min job...')
        cron_time.minute = (job_minute + 30) % 60
        if booking_time.minute != 0:
            cron_time.hour += 1
        command = job_command('hour.py', sender)
        log(f'Cron command: {command}')
        add_cron_job(command, cron_time)


def add_cron_job(command, cron_time):
    os.system(f'(crontab -l && echo "{str(cron_time)} {command}") | crontab -')


try:
    parse_subjects(sys.argv[1])
except Exception as e:
    log(str(e))
