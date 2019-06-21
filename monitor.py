import praw
import sys
import datetime
import requests
import json
from discord_webhook import DiscordWebhook, DiscordEmbed

webhookurl = 'YOUR WEBHOOK URL HERE'
webhook = DiscordWebhook(url = webhookurl)
reddit = praw.Reddit(client_id='YOUR_CLIENT_ID',
                     client_secret='YOUR_CLIENT_SECRET',
                     user_agent='Reddit Monitor 0.1',
                     )

global newest_submission_time
for submission in reddit.subreddit('buildapcsales').new(limit = 1):
    newest_submission_time = submission.created_utc
    print("Latest submission time found...")
while True:
    try: 
        for submission in reddit.subreddit('buildapcsales').new(limit = 1):
            if newest_submission_time < submission.created_utc:
                    print("Found new submission:", submission.title)
                    newest_submission_time = submission.created_utc
                    data = {
                        'embeds':
                        [{ 'color': 0x00ff00,
                           'title': submission.title,
                           'description': '[GO TO REDDIT]({:1})'.format(submission.shortlink),
                           'footer': {'icon_url': 'https://pbs.twimg.com/profile_images/1058145688599519233/Ja0vMAT5_400x400.jpg', 'text': 'Reddit Monitor by @SKLAD25 | ' + str(datetime.datetime.now())}
                        }]
                    }
                    post = requests.post(webhookurl, data = json.dumps(data), headers = {"Content-Type": "application/json"})
    except KeyboardInterrupt:
        sys.exit(0)
    except:
       print('Network Error')
