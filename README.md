Baconbot
========
This is an (unfinished) bot designed to take orders via Slack from a pre-determined menu for sandwiches and then send those orders via Pushbullet to a single person who is to pickup the order, hopefully avoiding any confusion or misunderstood orders in the process.

Getting setup
-------------

To get started you will need to create a bot on your Slack using [this link](https://my.slack.com/services/new/bot).

Once you have an API token for the Slack bot, you'll then want to set some environment variables:

```
SLACK_API_TOKEN=your Slack API token
SLACK_CHANNEL=the channel your bot lives in
PUSHBULLET_API_KEY=an API key for the pushbullet user
BOT_NAME=your bots name
```

Once these are set, you should be good to go:

```
python baconbot.py
```

How to use the bot
------------------

Nothing is actually implemented as yet, but when it is I will endeavour to document it here.