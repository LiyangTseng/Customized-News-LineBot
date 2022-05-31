from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('4sCZwRAHb8dYzT3ykI3HNsK8Ztm3rolvadOgWtQczgrbmMJ8OmqnbY2m4Ehu1UtGVCJApVUM6FyQoeOWTi4bt4J1v4I4atdxiQHOQEuSiEvB0jlfgbVZhTMQDuxwlFCii33T2DnCWhBU49BHyON8ngdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('c3a553c03e12f19a2279907c56f33e3d')

# monitor callback from post request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

if __name__ == "__main__":
    app.run()