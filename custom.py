import datetime

now = datetime.datetime.now()

if now.hour < 18:
    delta = datetime.timedelta(hours=-18)
    yesterday = now + delta
    url = f"https://www.espn.com/mens-college-basketball/scoreboard/_/date/{now.year}{now.month}{yesterday.day}/group/50"
else:
    url = f"https://www.espn.com/mens-college-basketball/scoreboard/_/date/{now.year}{now.month}{now.day}/group/50"
#print(now.hour)
#print(url)
print(datetime.date.strftime(now, "%Y%m%d"))