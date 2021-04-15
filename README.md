# How to use

Send an email to my **outlook account** `alex.townsend-teague@outlook.com` whose **subject** is of one of the following two forms, to be explained in more detail below:

`Book Catz Gym: dd/mm/yyyy, HH:MM, duration`

for a one-off booking, or

`Book Catz Gym: days, HH:MM, duration` 

for a booking that repeats on certain days of every week. Some examples:

`Book Catz Gym: 22/04/2021, 09:00, 30`    (one-off booking from 9am-9:30am on 22nd April)

`Book Catz Gym: 29/04/2021, 17:00, 60`    (one-off booking from 5pm-6pm on 29th April)

`Book Catz Gym: Su We Fr, 17:00, 30`      (repeated booking every Sunday, Wednesday and Friday from 5pm-5:30pm)

The first part `Book Catz Gym:` is not case-sensitive, but **the super important thing is the colon at the end**. In the remaining part, **the commas are the important thing**. If you forget either the colon or the commas it won’t work :)))))

If setting up a repeat booking, `days` should be a **space-separated** list of the first two letters of the days of the week you want. e.g. `Mo Tu Fr` for Monday, Tuesday and Friday, or `Sa Su` for the weekend warriors. **If you put a comma or something between these days then your booking will fail**.

The time part `HH:MM` is when you want your booking to **start**, and should be **in 24-hour format**. Only times ending in :00 or :30 will work. 

The duration is the length you want your booking to be **in minutes**. Only accepted values are 30 and 60.

Some examples of shit that won’t fly:

`Book Catz Gym 22/04/2021, 09:00, 30`     (no colon after ‘Book Catz Gym')

`Book Catz Gym: 29/04/2021 17:00 60`      (no commas between date/days, time, duration)

`Book Catz Gym: Su, We, Fr, 17:00, 30`    (commas between days you want the bookings)


# Developer notes

The .applescript file needs to go in the right folder - namely `~/Library/Application Scripts/com.apple.mail/`. Mail needs to have full disk access (scary!). Have also given full disk access to cron, crontab and Terminal - don't think all of these are necessary though.

Added the lines:
```
SHELL=/bin/bash
BASH_ENV=~/.bash_profile_conda
PATH=$PATH:/usr/local/bin
```

to the start of the crontab file. Also created the file `.bash_profile_conda` and put conda's spiel from `.bash_profile` into it. (This is so that `conda activate` actually works).  
