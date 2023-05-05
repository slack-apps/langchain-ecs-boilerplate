import logging
import os

from dotenv import load_dotenv
from flask import Flask, make_response
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

app = App(token=os.environ['SLACK_BOT_TOKEN'])
socket_mode_handler = SocketModeHandler(app, os.environ['SLACK_APP_TOKEN'])


@app.message("hello")
def message_hello(message, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Hey there <@{message['user']}>!"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Click Me"
                    },
                    "action_id": "button_click"
                },
            },
        ],
        text=f"Hey there <@{message['user']}>!"
    )


flask_app = Flask(__name__)


@flask_app.route('/health', methods=['GET'])
def slack_events():
    if socket_mode_handler.client is not None and socket_mode_handler.client.is_connected():
        return make_response('', 200)
    return make_response("The Socket Mode client is inactive", 503)


if __name__ == '__main__':
    socket_mode_handler.connect()
    flask_app.run(host='0.0.0.0', port=80)
