import os
import re
import pytz
import unicodedata
from datetime import datetime, timedelta

import requests
from telegram_send import send
from bs4 import BeautifulSoup


class BasicFuncs(object):
    """docstring for BasicFuncs."""

    def __init__(self, latest_monday_date=None, event_name='daily'):
        self.age_verify_url = \
            'https://www.kobo.com/tw/zh/ageverification/confirm?redirectUrl='

        self.headers = {
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/39.0.2171.95 '
                'Safari/537.36'
            )
        }

        now = datetime.utcnow()
        tw_tz = pytz.timezone('Asia/Taipei')
        self.today = now.astimezone(tw_tz).today()
        self.checkpoint_filename = \
            f'{self.today.strftime("%Y%m%d")}.{event_name}'

        self.checkpoint_filepath = \
            f'./checkpoint/{self.checkpoint_filename}.checkpoint'

        if not latest_monday_date:
            # Get the date of latest monday
            offset_to_latest_monday = self.today.weekday() % 7
            self.latest_monday_date = (
                self.today - timedelta(days=offset_to_latest_monday)
            ).strftime('%Y%m%d')
        else:
            self.latest_monday_date = latest_monday_date

    def get_daily_onsale_book(self):
        book_info = {}
        url = f'https://www.kobo.com/tw/zh/p/tw-dailydeal-bestofmonth'

        # Parser for kobo 99 event page
        kobo99_flow = requests.get(url=url, headers=self.headers)
        kobo99_page = BeautifulSoup(kobo99_flow.content, 'html.parser')
        today_99_block = kobo99_page.find('div', class_='SpotlightWidget')

        coupon = re.search(r'(kobo\d{6})', today_99_block.text)
        if coupon:
            book_info['Coupon'] = coupon.group(1)
        else:
            book_info['Coupon'] = ''

        book_info['URL'] = (
            f"{self.age_verify_url}{today_99_block.find('a')['href']}"
        )

        # Parser for book page
        book_page_flow = requests.get(
            url=book_info['URL'], headers=self.headers
        )

        book_page = BeautifulSoup(book_page_flow.content, 'html.parser')

        resources_path = {
            'Name': ['span', 'title product-field'],
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

    def get_event_onsale_book(self):
        base_url = 'https://tw.news.kobo.com/專題企劃/blog-weekly-booklist-'
        url = f'{base_url}{self.latest_monday_date}'

        # Parser for event page
        kobo_event_flow = requests.get(url=url, headers=self.headers)
        kobo_event_page = BeautifulSoup(
            kobo_event_flow.content, 'html.parser'
        )
        title = kobo_event_page.find('h1', class_='article-title')

        if title is not None and re.match(r'.+本週精選書單.+', title.text):
            books = kobo_event_page.find_all(
                'p', {'style': 'text-align: center;'}
            )

            coupon_msg = kobo_event_page.find(
                'div', style=re.compile(r'background:#eee;')
            ).text

            coupon = re.search(r'本週折扣代碼：(\w+)', coupon_msg).group(1)

            books_info = []
            for book in books:
                if book.a:
                    book_structure = {}

                    book_structure['Name'] = \
                        re.sub(r'《|》', '', book.text).strip()

                    book_structure['URL'] = \
                        f'{self.age_verify_url}{book.a["href"]}'

                    books_info.append(book_structure)

            event_info = {
                'URL': url,
                'Title': title.text,
                'Coupon': coupon,
                'BookList': books_info,
            }

            return event_info

    def create_telegram_send_conf(self):
        telegram_token = os.getenv('TELEGRAM_TOKEN')
        telegram_to = os.getenv('TELEGRAM_TO')

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
            parse_mode='text',
            conf='telegram-send.conf',
        )

    def create_checkpoint(self):
        os.makedirs(
            os.path.dirname(self.checkpoint_filepath), exist_ok=True
        )

        with open(self.checkpoint_filepath, 'w') as check_point_file:
            pass
