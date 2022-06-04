import configparser
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from crawl_news import CNBC_Crawler

config = configparser.ConfigParser()
config.read("config.ini")
# Channel Access Token
line_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"))
# Channel Secret
handler = WebhookHandler(config.get("line-bot", "channel_secret"))


def Notify_News(num_news=3):
    crawler = CNBC_Crawler()
    title_link_pairs = crawler.crawl(num_news)
    msg = "latest news from {}\n".format(crawler.name)
    for title, link in title_link_pairs:
        msg += title + "\n" + link + "\n\n"

    # https://developers.line.biz/en/reference/messaging-api/#send-broadcast-message
    line_bot_api.broadcast(TextSendMessage(text=msg))

def DoNotSleep():
    url = "https://news-collector-linebot.herokuapp.com/"
    r = requests.get(url)

sched = BlockingScheduler()

sched.add_job(DoNotSleep, trigger='interval', id="doNotSleeps_job", minutes=20)
# https://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html?highlight=day_of_week
# TODO: check what day in a week to update the news
sched.add_job(Notify_News, trigger='cron', id="notify_news_job_cont_night", day_of_week='wed', hour=21, minute=30)
sched.add_job(Notify_News, trigger='cron', id="notify_news_job_cont_noon", day_of_week='sat', hour=10, minute=00)
sched.start()