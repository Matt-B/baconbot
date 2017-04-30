import os
from slackclient import SlackClient

slack_token = os.environ["SLACK_API_TOKEN"]
slack_channel = os.environ["SLACK_CHANNEL"]

sc = SlackClient(slack_token)

sc.api_call(
    "chat.postMessage",
    channel=slack_channel,
    text="Hello from baconbot!"
)
