import os
import time
from slackclient import SlackClient
from pushbullet import PushBullet

slack_token = os.environ["SLACK_API_TOKEN"]
slack_channel = os.environ["SLACK_CHANNEL"]
bot_name = os.environ["BOT_NAME"]
pushbullet_api_key = os.environ["PUSHBULLET_API_KEY"]

sc = SlackClient(slack_token)
pb = PushBullet(pushbullet_api_key)


def get_bot_id():
    api_call = sc.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == bot_name:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                return user.get('id')
    else:
        print("could not find bot user with the name " + bot_name)
        return None


def parse_slack_output(bot_id, slack_rtm_output):
    at_bot_id = "<@" + bot_id + ">"
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and at_bot_id in output['text']:
                return output['text'], output['channel']
    return None, None


def handle_command(command, channel):
    print(command, channel)
    if "confirm" in command:
        pb.push_note(bot_name, channel + ":" + command)
        response = "Order pushed."
    elif "order" in command:
        response = "Here, I would take an order."
    else:
        response = "I have no idea what you are asking me."

    sc.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


if __name__ == "__main__":
    bot_id = get_bot_id()
    READ_WEBSOCKET_DELAY = 1
    if sc.rtm_connect():
        print(bot_name + " connected and running!")
        while True:
            command, channel = parse_slack_output(bot_id, sc.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
