import io
import re
import os
import json
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
offset = (today.weekday() - 3) % 7
date_str = (today - timedelta(days=offset)).strftime("%Y%m%d")

url = f'https://tw.news.kobo.com/專題企劃/blog_dd_{date_str}'
print(f'URL: {url}')

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/39.0.2171.95 '
        'Safari/537.36'
    )
}

regex = (
    r'書名：\s*(?P<Name>.+)\n'
    r'作者：\s*(?P<Author>.+)\n'
    r'出版社：\s*(?P<Publisher>.+)\n'
)

latest_99_page_flow = requests.get(url=url, headers=headers)
latest_99_page = BeautifulSoup(latest_99_page_flow.content, 'html.parser')
title = latest_99_page.find('h1', class_='article-title')

if title is not None and re.match(r'.+一週99書單.+', title.text):
    print(f'Page title: {title.text}')
    books = latest_99_page.find_all('div', class_='textImage textImage-inline')
    simple_content = latest_99_page.find_all('div', class_='simplebox-content')
    books_structure = []

    for book in books:
        if not book.a:
            books.remove(book)

    for book, content in zip(books, simple_content):
        content_text = content.get_text()

        try:
            book_structure = re.search(
                regex, content_text, re.MULTILINE
            ).groupdict('')

            coupon = re.search(r'(kobo\d{6})', content_text)

            if coupon:
                coupon = coupon.group(1)
            else:
                coupon = ''

            book_structure['Coupon'] = coupon
            book_structure['URL'] = book.a['href']
            book_structure['Image'] = book.a.img['src']

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

    folder_name = 'book_list'
    create_folder(f'./{folder_name}/')
    with io.open(f'{folder_name}/{date_str}.json', 'w', encoding='utf8') as json_file:
        json.dump(books_structure, json_file, ensure_ascii=False)

else:
    print('The page is not available')
