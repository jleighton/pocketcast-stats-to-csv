from requests import request
from datetime import datetime
import json
import csv
import config

with open('stats.json') as stats_file:
    data_yesterday = json.load(stats_file)

yesterday_date = data_yesterday['date']
timeListenTotal = data_yesterday['timeListenTotal']



"""Gets the user statistics from the PocketCasts API
Parameters
----------
username : str
    Your login email address for PocketCasts.
password : str
    Your login password for PocketCasts.
Returns
-------
An dict all the statistics about your profile.
"""

# Login and get a tocken from PocketCasts
login_url = "https://api.pocketcasts.com/user/login"
data = (
    f'{{"email":'+config.pocketcasts_email + ',"password":' + config.pocketcasts_password +',"scope":"webplayer"}}'
)
headers = {"Origin": "https://play.pocketcasts.com"}
response = request("POST", login_url, data=data, headers=headers).json()

if "message" in response:
    raise Exception("Login Failed")
else:
    token = response["token"]

# Get the statistics through the API
req = request(
    "POST",
    "https://api.pocketcasts.com/user/stats/summary",
    data=("{}"),
    headers={
        "Authorization": f"Bearer {token}",
        "Origin": "https://play.pocketcasts.com",
        "Accept": "*/*",
    },
)

if not req.ok:
    raise Exception("Invalid request")

json_data = req.json()
timeListened = json_data["timeListened"]
timeListenedToday = int(timeListened) - int(timeListenTotal)
today = datetime.today()
today = (today.strftime("%Y-%m-%d"))

stats = {
    "date":today,
    "timeListenedToday":int(timeListenedToday),
    "timeListenTotal": int(timeListened)
}

print (stats["date"])
print (timeListenedToday)



with open('stats.json', 'w') as outfile:#
    json.dump(stats, outfile)


fields=[today,int(timeListenedToday),int(timeListened)]
with open(r'stats.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
