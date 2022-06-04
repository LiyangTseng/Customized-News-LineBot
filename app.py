from __future__ import unicode_literals
import os
import configparser
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from crawl_news import CNBC_Crawler

app = Flask(__name__)

config = configparser.ConfigParser()
config.read("config.ini")
# Channel Access Token
line_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"))
# Channel Secret
handler = WebhookHandler(config.get("line-bot", "channel_secret"))

# monitor callback from post request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    print("request body: ", body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    """ need to turn on webhook in LINE developer console !! """
    # TODO: add more interactions with users (keyword spotting)
    if event.message.text.lower() == "cnbc":
        """ if users query CNBC """
        crawler = CNBC_Crawler()
        num_news = 3
        title_link_pairs = crawler.crawl(num_news)
        msg = "latest news from {}\n".format(crawler.name)
        for title, link in title_link_pairs:
            msg += title + "\n" + link + "\n\n"

        message = TextSendMessage(text=msg)
    else:
        message = TextSendMessage(text=event.message.text)
    
    line_bot_api.reply_message(
        event.reply_token,
        message
    )

# TODO: add customizing rich menu ?

if __name__ == "__main__":
    app.run()