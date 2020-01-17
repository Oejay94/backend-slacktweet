import os
import time
import sys
from slack import RTMClient
import ssl as ssl_lib
import certifi


if sys.version_info[0] < 3:
    raise RuntimeError("This program requires Python 3")

"""
There were some issues with my MacOS ssl certificates, so I imported a ssl library
and modified it to where it took in my own hard coded ssl certificates
"""
ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
# slack_token = os.environ["BOT_USER_TOKEN"]
# client = RTMClient(token=slack_token, ssl=ssl_context)


bot_user_token = os.environ['BOT_USER_TOKEN']
bot_oauth_token = os.environ['BOT_OAUTH_TOKEN']


print(f"oauth= {bot_oauth_token}")
print(f"bot_user_token= {bot_user_token}")


class SlackBot:
    def __init__(self, user_token, oauth_token):
        # Create RTM client and set up event callbacks
        self.sc = RTMClient(token=bot_user_token,
                            ssl=ssl_context, run_async=True)

        # The main 3 events that I'm interested in:
        RTMClient.run_on(event="hello")(self.on_hello)
        RTMClient.run_on(event="goodbye")(self.on_goodbye)
        RTMClient.run_on(event="message")(self.on_message)

        # Start the RTM client, connect on Slack server
        self.future = self.sc.start()
        self.wc = None

    def on_hello(self, **payload):
        print("Slack says: YOU ARE NOW CONNECTED")
        self.wc = payload['web_client']
        assert self.wc is not None
        print("I now have a web_client instance")

        # say hello to the channel
        self.send_message("Hello Channel")

    def on_goodbye(self, **payload):
        print("Slack says: GOODBYE")

    def on_message(self, **payload):
        print("Slack says: You got a message")

    def send_message(self, msg, chan='#bot-test'):
        self.wc.chat_postMessage(
            channel=chan,
            text=msg
        )

    def run(self):
        """wait for slack rtm client to complete"""
        #logger.info(f'{self} Waiting for commands')
        try:
            loop = self.future.get_loop()
            loop.run_until_complete(self.future)
        except Exception as e:
            logger.error(f'Unhandled Error: {e}')
        #logger.info(f'{self} Exiting command loop')



# create an instance of a slack bot
sb = SlackBot(bot_user_token, bot_oauth_token)

# sb.send_message("Hello from before sb.run")

# blocking call
sb.run()

print("Slackbot is done.")
