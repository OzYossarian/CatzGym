import urllib
import rooms
import datetime

from users import get_user
from utils import sleep_until, next_week

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


duration_indices = {
    30: 0,
    60: 1,
}

actions = {
    'edit': 'edit_entry.php?',
    'view': 'view_entry.php?',
    'index': 'index.php?',
}

base_url = 'https://mrbs.stcatz.ox.ac.uk/mrbs/'
url_params = {
    'view': 'day',
    'year': None,
    'month': None,
    'day': None,
    'area': 3,
    'room': None,
    'hour': None,
    'minute': None,
}


def gym_url(date_time, action, room):
    params = {
        'view': 'day',
        'year': date_time.year,
        'month': date_time.month,
        'day': date_time.day,
        'area': 3,
    }
    if action == 'edit':
        params['room'] = room.url_id
        params['hour'] = date_time.hour
        params['minute'] = date_time.minute
    return f'{base_url}{actions[action]}{urllib.parse.urlencode(params)}'


def login(browser, user):
    username_input = browser.find_element_by_id('username')
    username_input.send_keys(user.username)
    password_input = browser.find_element_by_id('password')
    password_input.send_keys(user.password)
    log_in_button = browser.find_element_by_xpath('//*[@id="logon"]//input[@type="submit"]')
    log_in_button.click()


def book_gym(booking_time, duration, save_time, sender, room=rooms.one, user=None):
    if user is None:
        user = get_user(sender, booking_time)

    with webdriver.Chrome() as browser:
        wait = WebDriverWait(browser, 10)
        browser.get((gym_url(booking_time, 'edit', room)))
        login(browser, user)

        description_input = wait.until(EC.presence_of_element_located((By.ID, 'name')))
        description_input.send_keys(user.description())
        end_selection = Select(browser.find_element_by_id('end_seconds'))
        end_selection.select_by_index(duration_indices[duration])

        save_button = browser.find_element_by_name('save_button')
        if save_time is not None:
            sleep_until(save_time)
        save_button.click()


def extend_booking(booking_time, duration, save_time, sender, room=rooms.one, user=None):
    if user is None:
        user = get_user(sender, booking_time)

    with webdriver.Chrome() as browser:
        wait = WebDriverWait(browser, 10)
        browser.get((gym_url(booking_time, 'index', room)))
        login(browser, user)

        total_seconds = booking_time.hour * 60 * 60 + booking_time.minute * 60
        xpath = f'//th[@data-seconds={total_seconds}]/../td[{room.column}]//a'
        booking = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        booking.click()

        xpath = f'//input[@value="Edit Entry"]'
        edit_button = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        edit_button.click()

        end_selection = Select(wait.until(EC.presence_of_element_located((By.ID, 'end_seconds'))))
        end_selection.select_by_index(duration_indices[duration])

        save_button = browser.find_element_by_name('save_button')
        if save_time is not None:
            sleep_until(save_time)
        save_button.click()


def book_gym_now(sender):
    duration = 30
    now = datetime.datetime.now()
    booking_minute = 0 if 0 <= now.minute < 30 else 30
    booking_time = next_week().replace(minute=booking_minute, second=0, microsecond=0)
    save_time = booking_time + datetime.timedelta(days=-7, minutes=duration, microseconds=50)
    book_gym(booking_time, duration, save_time, sender)


def extend_booking_now(sender):
    duration = 60
    now = datetime.datetime.now()
    (booking_minute, booking_hour) = (30, now.hour - 1) if 0 <= now.minute < 30 else (0, now.hour)
    booking_time = next_week().replace(hour=booking_hour, minute=booking_minute, second=0, microsecond=0)
    save_time = booking_time + datetime.timedelta(days=-7, minutes=duration, microseconds=50)
    extend_booking(booking_time, duration, save_time, sender)
