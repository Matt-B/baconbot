import os
import time
import re
from slackclient import SlackClient
from pushbullet import PushBullet

slack_token = os.environ["SLACK_API_TOKEN"]
slack_channel = os.environ["SLACK_CHANNEL"]
bot_name = os.environ["BOT_NAME"]
pushbullet_api_key = os.environ["PUSHBULLET_API_KEY"]

sc = SlackClient(slack_token)
pb = PushBullet(pushbullet_api_key)

menu = {1: "Bacon Baguette (Small)",
        2: "Bacon Baguette (Large)",
        3: "Bacon and Sausage Baguette (Small)",
        4: "Bacon and Sausage Baguette (Large)",
        5: "Breakfast Baguette (Bacon/Egg/Sausage) (Large)"}

placed_orders = {}


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
                return output['text'], output['channel'], output['user']
    return None, None, None


def parse_order(order_command, user):
    ordered_items = [int(s) for s in order_command.split() if s.isdigit()]
    items = []
    for item in ordered_items:
        if item <= len(menu):
            items.append(menu.get(item))
    placed_orders[user] = items
    return items


def handle_command(command, channel, user):
    if "confirm" in command:
        pb.push_note(bot_name, channel + ":" + command)
        response = "Order pushed."
    elif "menu" in command:
        response = ""
        for key, value in menu.items():
            response = response + "\n" + str(key) + ": " + value
    elif "order" in command:
        order = parse_order(command, user)
        if len(order) > 0:
            response = "<@" + user + "> You have ordered:\n"
            for item in order:
                response += item + "\n"
        else:
            response = "No menu items matched.\nPlease enter your choice(s) separated by a space."
    else:
        response = "I have no idea what you are asking me."

    sc.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


if __name__ == "__main__":
    bot_id = get_bot_id()
    READ_WEBSOCKET_DELAY = 1
    if sc.rtm_connect():
        print(bot_name + " connected and running!")
        while True:
            command, channel, user = parse_slack_output(bot_id, sc.rtm_read())
            if command and channel and user:
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
