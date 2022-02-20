import os
import re
import pytz
import unicodedata
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from telegram_send import send

import undetected_chromedriver.v2 as uc


class BasicFuncs(object):
    """docstring for BasicFuncs."""

    def __init__(self, event_name='daily'):
        self.age_verify_url = \
            'https://www.kobo.com/tw/zh/ageverification/confirm?redirectUrl='

        now = datetime.utcnow()
        tw_tz = pytz.timezone('Asia/Taipei')
        self.today = now.astimezone(tw_tz).today()
        self.checkpoint_filename = \
            f'{self.today.strftime("%Y%m%d")}.{event_name}'

        self.checkpoint_filepath = \
            f'./checkpoint/{self.checkpoint_filename}.checkpoint'

    def get_daily_onsale_book(self, url):
        book_info = {}

        kobo99_flow = uc.Chrome(headless=True)
        kobo99_flow.get(url)

        kobo99_page = BeautifulSoup(kobo99_flow.page_source, 'html.parser')
        today_99_block = kobo99_page.find('div', class_='SpotlightWidget')

        coupon = re.search(r'(kobo[\w\d]+)', today_99_block.text)

        if coupon:
            book_info['Coupon'] = coupon.group(1)
        else:
            book_info['Coupon'] = ''

        book_info['URL'] = (
            f"{self.age_verify_url}{today_99_block.find('a')['href']}"
        )

        # Parser for book page
        book_page_flow = uc.Chrome(headless=True)
        book_page_flow.get(book_info['URL'])
        book_page = BeautifulSoup(book_page_flow.page_source, 'html.parser')

        resources_path = {
            'Name': ['h2', 'title product-field'],
            'Author': ['a', 'contributor-name'],
        }

        for element in resources_path:
            element_content = book_page.find(
                resources_path[element][0],
                class_=resources_path[element][1]
            )

            if element_content:
                book_info[element] = \
                    list(element_content.stripped_strings)[0]
            else:
                book_info[element] = 'N/A'

        book_info['Intro'] = unicodedata.normalize(
            'NFKD',
            book_page.find(
                'div', class_='synopsis-description'
            ).text
        )

        # Parser for book publication info
        book_detail_info = book_page.find(
            'div', class_='bookitem-secondary-metadata'
        )

        publisher_block = book_detail_info.find(
            'a', class_='description-anchor'
        )

        book_info['Publisher'] = \
            publisher_block.text if publisher_block else 'N/A'

        publish_date_regex = re.search(
            r'(\d{4}年\d{1,2}月\d{1,2}日)', book_detail_info.text
        )

        if publish_date_regex:
            publish_date = datetime.strptime(
                publish_date_regex.group(1), '%Y年%m月%d日'
            )
            book_info['PublishDate'] = publish_date.strftime('%Y/%m/%d')
        else:
            book_info['PublishDate'] = 'N/A'

        return book_info

    def create_telegram_send_conf(self, telegram_token, telegram_to):
        if not telegram_token or not telegram_to:
            raise Exception(
                'The telegram-send related info are not in env variable'
            )

        with open('telegram-send.conf', 'w') as conf_file:
            conf_file.write(
                '[telegram]\n'
                f'token = {telegram_token}\n'
                f'chat_id = {telegram_to}'
            )

    def send_notification(self, message_list):
        send(
            messages=message_list,
            parse_mode='markdown',
            conf='telegram-send.conf',
        )

    def create_checkpoint(self):
        os.makedirs(
            os.path.dirname(self.checkpoint_filepath), exist_ok=True
        )

        with open(self.checkpoint_filepath, 'w') as check_point_file:
            pass