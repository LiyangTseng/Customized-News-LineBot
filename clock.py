import configparser
from linebot import LineBotApi, WebhookHandler
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from crawl_news import crawl

config = configparser.ConfigParser()
config.read("config.ini")
# Channel Access Token
line_bot_api = LineBotApi(config.get("line-bot", "channel_access_token"))
# Channel Secret
handler = WebhookHandler(config.get("line-bot", "channel_secret"))


def Notify_News():
    title, link = crawl()
    # https://developers.line.biz/en/reference/messaging-api/#send-broadcast-message
    line_bot_api.broadcast("{}\n{}".format(title, link))

def DoNotSleep():
    url = "https://news-collector-linebot.herokuapp.com/"
    r = requests.get(url)

sched = BlockingScheduler()

sched.add_job(DoNotSleep, trigger='interval', id="doNotSleeps_job", minutes=20)
sched.add_job(Notify_News, trigger='cron', id="notify_news_job", hour=10, minute=40)
sched.add_job(Notify_News, trigger='interval', id="notify_news_job_cont", minutes=5)