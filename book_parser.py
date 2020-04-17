import os
import json
import glob
import datetime
import telegram_send
import requests
import shutil

list_of_files = glob.glob('./book_list/*')
latest_file = max(list_of_files)

with open(latest_file, 'r', encoding='utf-8') as f:
    book_list = json.loads(f.readline())

idx = (datetime.datetime.today().weekday() + 4) % 7

try:
    book = book_list[idx]

    # Create the configuration file for telegram
    with open('telegram-send.conf', 'w') as conf_file:
        conf_file.write(
            '[telegram]\n'
            f'token = {os.getenv("TELEGRAM_TOKEN")}\n'
            f'chat_id = {os.getenv("TELEGRAM_TO")}'
        )

    coupon_message = f'{book["Coupon"]}' if book["Coupon"] else '不需折扣碼'

    message = (
        f'書名： {book["Name"]}\n'
        f'作者： {book["Author"]}\n'
        f'出版社： {book["Publisher"]}\n'
        f'簡介： {book["Intro"]}\n'
        f'[購買連結]({book["URL"]})'
    )

    # Download and sending the book cover
    url = book['Image']
    file_name = os.path.basename(url)
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(file_name, 'wb') as book_cover:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, book_cover) 

    telegram_send.send(
        messages=[message],
        parse_mode='markdown',
        conf='telegram-send.conf',
    )

    with open(file_name, "rb") as book_cover:
        telegram_send.send(
            messages=[f'{coupon_message}'],
            images=[book_cover],
            conf='telegram-send.conf',
        )

except Exception as e:
    raise e

