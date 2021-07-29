# -*- encoding: utf-8 -*-

"""
rss.py

钉钉 Rss 机器人
推送 Rss 信息到钉钉机器人Api
 
"""

from datetime import datetime
import feedparser
import dateparser
from models import db, Rss, History
from conf import webhook_url, webhook_template
import os
import requests
import re
import json


# h = {
#     'Content-Type': 'text/json'
# }

class CardItem:
    def __init__(self, title, url, pic_url, blog_name, summary=''):
        self.title = title
        self.url = url
        self.pic_url = pic_url
        self.summary = summary
        self.blog_name = blog_name


class RssRobot:
    def __init__(self):
        self.webhook = webhook_url
        self.card = webhook_template

    def parse_rss(self):
        # self.remove_old_history()
        rss_list = Rss.select()
        rss_card_dict = {}
        post_url_list = [rss_history.url for rss_history in
                         History.select().where(History.publish_at == datetime.today().strftime("%Y-%m-%d"))]
        for rss in rss_list:
            rss_history_list = []
            card_list = []
            feed = feedparser.parse(rss.feed)
            print(feed.entries)
            for entry in feed.entries:
                if entry.link not in post_url_list:
                    card_list.append(CardItem(title=f'{entry.title}',
                                              url=entry.link,
                                              pic_url='https://ftp.bmp.ovh/imgs/2020/07/6cdb9f606677c9e3.jpg',
                                              blog_name=rss.title,
                                              summary=self.parse_summary(entry.summary)))
                    rss_history_list.append(History(url=entry.link))
            print('{} new post found in feed:{}'.format(len(card_list), rss.url))
            if len(card_list) > 0:
                rss_card_dict[rss.title] = card_list
                with db.atomic():
                    History.bulk_create(rss_history_list, batch_size=10)

        return rss_card_dict

    def parse_summary(self, summary):
        return summary.replace(
            '<br /><br /><span style="font-size: 12px; color: gray;">(Feed generated with <a href="http://fetchrss.com" target="_blank">FetchRSS</a>)</span>',
            '')

    def is_today(self, entry):
        return dateparser.parse(entry['updated']).date() == datetime.today().date()

    def send_rss(self):
        rss_card_dict = self.parse_rss()
        for key in rss_card_dict:
            for item in rss_card_dict[key]:
                self.request_feishu_webhook(item)

    def request_feishu_webhook(self, carditem):
        data = webhook_template.replace('$TITLE_TEXT', self.json_encode(carditem.title))
        data = data.replace('$SUMMARY', self.json_encode(carditem.summary))
        data = data.replace('$LINK', self.json_encode(carditem.url))
        data = data.replace('$BLOG_NAME', self.json_encode(carditem.blog_name))
        r = requests.post(url=webhook_url, headers={'Content-Type': 'application/json'}, data=data.encode('utf8'))
        print(r.content)

    def remove_old_history(self):
        # history_list = History.delete().where(History.publish_at < datetime.today().strftime("%Y-%m-%d"))
        history_list = History.delete().where(True)
        history_list.execute()

    def json_encode(self, s):
        return s.replace('\\', '\\\\').replace('"', '\\"')


def send_rss():
    rss_bot = RssRobot()
    rss_bot.send_rss()
    pass


if __name__ == '__main__':
    send_rss()
