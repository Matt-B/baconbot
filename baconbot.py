import os
import time
from slackclient import SlackClient

slack_token = os.environ["SLACK_API_TOKEN"]
slack_channel = os.environ["SLACK_CHANNEL"]

sc = SlackClient(slack_token)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                # return text after the @ mention, whitespace removed
                return output['text'], output['channel']
    return None, None


def handle_command(command, channel):
    print(command, channel)

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if sc.rtm_connect():
        print("baconbot connected and running!")
        while True:
            command, channel = parse_slack_output(sc.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
