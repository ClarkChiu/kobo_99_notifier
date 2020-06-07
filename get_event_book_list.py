# import io
# import json
import re
import os
import requests
import unicodedata
from bs4 import BeautifulSoup
from datetime import date, timedelta


def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print(f'Error: Creating directory. {directory}')


today = date.today()
offset = today.weekday() % 7
date_str = (today - timedelta(days=offset)).strftime("%Y%m%d")

url = f'https://tw.news.kobo.com/專題企劃/blog-weekly-booklist-{date_str}'
redirectUrl = 'https://www.kobo.com/tw/zh/ageverification/confirm?redirectUrl='
print(f'URL: {url}')

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/39.0.2171.95 '
        'Safari/537.36'
    )
}

event_page_flow = requests.get(url=url, headers=headers)
event_page = BeautifulSoup(event_page_flow.content, 'html.parser')
title = event_page.find('h1', class_='article-title')

if title is not None and re.match(r'.+本週精選書單.+', title.text):
    print(f'Page title: {title.text}')
    books = event_page.find_all('p', {'style': 'text-align: center;'})
    coupon_msg = event_page.find(
        'div',
        {'style': "background:#eee;border:1px solid #ccc;padding:5px 10px;"}
    ).text

    coupon = re.search(r'本週折扣代碼：(\w{5})', coupon_msg).group(1)
    books_structure = []

    for book in books:
        if not book.a:
            books.remove(book)

    for book in books:
        try:
            book_structure = {}
            book_structure['Name'] = re.sub(r'《|》', '', book.text).strip()
            book_structure['URL'] = f'{redirectUrl}{book.a["href"]}'

            book_page_flow = requests.get(
                url=book_structure['URL'], headers=headers
            )

            book_page = BeautifulSoup(book_page_flow.content, 'html.parser')
            desc = book_page.find('div', class_='synopsis-description')

            book_structure['Intro'] = unicodedata.normalize(
                'NFKD', desc.get_text()
            )

            books_structure.append(book_structure)
        except Exception as e:
            raise e

    # folder_name = 'event_book_list'
    # create_folder(f'./{folder_name}/')
    # filename = f'{folder_name}/{date_str}_event.json'
    # with io.open(filename, 'w', encoding='utf8') as json_file:
    #     json.dump(books_structure, json_file, ensure_ascii=False)

    import telegram_send

    try:
        # Create the configuration file for telegram
        with open('telegram-send.conf', 'w') as conf_file:
            conf_file.write(
                '[telegram]\n'
                f'token = {os.getenv("TELEGRAM_TOKEN")}\n'
                f'chat_id = {os.getenv("TELEGRAM_TO")}'
            )

        telegram_send.send(
            messages=[coupon_msg, coupon],
            parse_mode='markdown',
            conf='telegram-send.conf',
        )

        for book in books_structure:
            message = (
                f'書名：{book["Name"]}\n'
                f'簡介：\n{book["Intro"]}\n'
                f'[購買連結]({book["URL"]})'
            )

            telegram_send.send(
                messages=[message],
                parse_mode='markdown',
                conf='telegram-send.conf',
            )

    except Exception as e:
        raise e
else:
    print('The page is not available')
