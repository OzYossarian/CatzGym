class User:
    def __init__(self, username, password, name, address):
        self.username = username
        self.password = password
        self.name = name
        self.address = address

    def description(self):
        return f'{self.name} ({self.address})'


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
