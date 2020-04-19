import os
import json
import pytz
import glob
import datetime
import telegram_send

# Get the latest book list on book_list folder
list_of_files = glob.glob('./book_list/*')
latest_file = max(list_of_files)

try:
    with open(latest_file, 'r', encoding='utf-8') as f:
        book_list = json.loads(f.readline())
except Exception as e:
    raise e

taiwan_tz = pytz.timezone('Asia/Taipei')
today = datetime.datetime.today().astimezone(taiwan_tz)
weekday_of_today = today.weekday()
idx = (weekday_of_today + 4) % 7

try:
    # Create the configuration file for telegram
    with open('telegram-send.conf', 'w') as conf_file:
        conf_file.write(
            '[telegram]\n'
            f'token = {os.getenv("TELEGRAM_TOKEN")}\n'
            f'chat_id = {os.getenv("TELEGRAM_TO")}'
        )

    book = book_list[idx]
    coupon_message = f'{book["Coupon"]}' if book["Coupon"] else '不需折扣碼'
    message = (
        f'{today.strftime("%Y/%m/%d")} Kobo 特價書籍\n\n'
        f'書名：{book["Name"]}\n'
        f'作者：{book["Author"]}\n'
        f'出版社：{book["Publisher"]}\n\n'
        f'簡介：\n{book["Intro"]}\n'
        f'[購買連結]({book["URL"]})'
    )

    telegram_send.send(
        messages=[message, f'{coupon_message}'],
        parse_mode='markdown',
        conf='telegram-send.conf',
    )
except Exception as e:
    raise e
