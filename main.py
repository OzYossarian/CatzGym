import datetime
import urllib
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


class User:
    def __init__(self, username, password, name, address):
        self.username = username
        self.password = password
        self.name = name
        self.address = address

    def description(self):
        return f'{self.name} ({self.address})'


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
    'room': 144,
    'hour': None,
    'minute': None,
}


def gym_url(date_time, action):
    params = url_params.copy()
    params['year'] = date_time.year
    params['month'] = date_time.month
    params['day'] = date_time.day
    if action == 'edit':
        params['hour'] = date_time.hour
        params['minute'] = date_time.minute
    return f'{base_url}{actions[action]}{urllib.parse.urlencode(params)}'


teague = User('scat7459', '7756+GGsp-', 'Teague', 'Crown Street')
elise = User('scat7495', '8519-DPnw-', 'Elise', 'Crown Street')
will = User('scat7381', 'Charlesws7', 'Will', 'Crown Street')
users = {
    'alex.townsend-teague@outlook.com': teague,
    'alexander.teague@stcatz.ox.ac.uk': teague,
    'william.staunton@stcatz.ox.ac.uk': will,
}


def get_user(sender, booking_time):
    user = users[sender]
    if user == teague and booking_time.day % 2 == 0:
        user = elise
    return user


def login(browser, user):
    username_input = browser.find_element_by_id('username')
    username_input.send_keys(user.username)
    password_input = browser.find_element_by_id('password')
    password_input.send_keys(user.password)
    log_in_button = browser.find_element_by_xpath('//*[@id="logon"]//input[@type="submit"]')
    log_in_button.click()


def book_gym(booking_time, duration, save_time, sender):
    user = get_user(sender, booking_time)

    with webdriver.Chrome() as browser:
        wait = WebDriverWait(browser, 10)
        browser.get((gym_url(booking_time, 'edit')))
        login(browser, user)

        description_input = wait.until(EC.presence_of_element_located((By.ID, 'name')))
        description_input.send_keys(user.description())
        end_selection = Select(browser.find_element_by_id('end_seconds'))
        end_selection.select_by_index(duration_indices[duration])

        save_button = browser.find_element_by_name('save_button')
        sleep_until(save_time)
        save_button.click()


def extend_booking(booking_time, duration, save_time, sender):
    user = get_user(sender, booking_time)
    with webdriver.Chrome() as browser:
        wait = WebDriverWait(browser, 10)
        browser.get((gym_url(booking_time, 'index')))
        login(browser, user)

        total_seconds = booking_time.hour * 60 * 60 + booking_time.minute * 60
        xpath = f'//th[@data-seconds={total_seconds}]/../td[3]//a'
        booking = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        booking.click()

        xpath = f'//input[@value="Edit Entry"]'
        edit_button = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        edit_button.click()

        end_selection = Select(wait.until(EC.presence_of_element_located((By.ID, 'end_seconds'))))
        end_selection.select_by_index(duration_indices[duration])

        save_button = browser.find_element_by_name('save_button')
        sleep_until(save_time)
        save_button.click()


def next_week():
    return datetime.datetime.now() + datetime.timedelta(days=7)


def sleep_until(date_time):
    sleep_time = date_time - datetime.datetime.now()
    time.sleep(sleep_time.total_seconds())

print('Book Catz Gym: 04/04/2021, 14:00, 30'.upper())