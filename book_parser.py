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
# print(f'The idx is {idx}')

try:
    book = book_list[idx]

    # Create the configuration file for telegram
    with open('telegram-send.conf', 'w') as conf_file:
        conf_file.write(
            '[telegram]\n'
            f'token = {os.getenv("TELEGRAM_TOKEN")}\n'
            f'chat_id = {os.getenv("TELEGRAM_TO")}'
        )

    if book["Coupon"]:
        coupon_message = f'折扣碼： {book["Coupon"]}'
    else:
        coupon_message = f'不需折扣碼'

    message = (
        f'書名： {book["Name"]}\n'
        f'作者： {book["Author"]}\n'
        f'出版社： {book["Publisher"]}\n'
        f'{coupon_message}\n'
        f'簡介： {book["Intro"]}\n'
        f'[購買連結]({book["URL"]})'
    )

    telegram_send.send(
        messages=[message],
        parse_mode='markdown',
        conf='telegram-send.conf',
    )

    # Download and sending the book cover
    # url = book['Image']
    # file_name = os.path.basename(url)
    # r = requests.get(url, stream=True)
    # if r.status_code == 200:
    #     with open(file_name, 'wb') as f:
    #         r.raw.decode_content = True
    #         shutil.copyfileobj(r.raw, f) 

    # with open(file_name, "rb") as f:
    #     message = (
    #         f'書名： {book["Name"]}\n'
    #         f'作者： {book["Author"]}\n'
    #         f'出版社： {book["Publisher"]}\n'
    #         f'折扣碼： {book["Coupon"]}\n'
    #         f'簡介： {book["Intro"]}\n'
    #         f'[購買連結]({book["URL"]})'
    #     )
    #     telegram_send.send(
    #         messages=[message],
    #         images=[f],
    #         parse_mode='markdown',
    #         conf='telegram-send.conf',
    #     )
except Exception as e:
    raise e

