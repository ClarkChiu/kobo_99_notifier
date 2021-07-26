import os
import re
import json
import shutil
import urllib.parse
from unittest import mock
from kobo_notifier.BasicFuncs import BasicFuncs


def test_get_daily_onsale_book(requests_mock):
    url = 'https://www.kobo.com/tw/zh/p/tw-dailydeal-bestofmonth'
    result_file_path = 'tests/data/20200628_book_info.json'
    with open(result_file_path, 'r', encoding='UTF-8') as f:
        book_info = json.loads(f.read())

    # Mock the response of kobo 99 event page
    kobo_99_event_page_path = 'tests/data/20200628_kobo_99_event_page.html'
    with open(kobo_99_event_page_path, 'r', encoding='UTF-8') as f:
        requests_mock.get(url, text=f.read())

    # Mock the response of book page
    kobo_99_book_page_path = 'tests/data/20200628_kobo_99_book_page.html'
    with open(kobo_99_book_page_path, 'r', encoding='UTF-8') as f:
        requests_mock.get(
            book_info['URL'],
            text=f.read()
        )

    basic_func = BasicFuncs()
    assert book_info == basic_func.get_daily_onsale_book(url)


def test_get_event_onsale_book(requests_mock):
    result_file_path = 'tests/data/20200622_weekly_event_info.json'
    with open(result_file_path, 'r', encoding='UTF-8') as f:
        event_info = json.loads(f.read())

    # Mock the response of kobo 99 event page
    kobo_event_page_path = 'tests/data/20200622_weekly_event_info.html'
    with open(kobo_event_page_path, 'r', encoding='UTF-8') as f:
        requests_mock.get(
            urllib.parse.quote(event_info['URL'], safe=':/'),
            text=f.read()
        )

    basic_func = BasicFuncs(latest_monday_date='20200622')
    assert event_info == basic_func.get_event_onsale_book()


def test_create_telegram_send_conf():
    basic_func = BasicFuncs()
    basic_func.create_telegram_send_conf(
        telegram_token=os.getenv('TELEGRAM_TOKEN'),
        telegram_to=os.getenv('TELEGRAM_TO')
    )

    with open('telegram-send.conf', 'r') as conf_file:
        assert re.match(
            (
                r'\[telegram\]\n'
                r'token = [0-9]{10}:[a-zA-Z0-9_-]{35}\n'
                r'chat_id = [\-\@\w\_]+'
            ),
            conf_file.read()
        )


@mock.patch('kobo_notifier.BasicFuncs.send')
def test_send_notification(telegram_send_send_action):
    basic_func = BasicFuncs()
    basic_func.send_notification(['123'])
    telegram_send_send_action.assert_called_once()


def test_create_checkpoint_daily():
    event_name_lists = ['daily', 'event']
    for event_name in event_name_lists:
        basic_func = BasicFuncs(event_name=event_name)
        basic_func.create_checkpoint()
        with open(basic_func.checkpoint_filepath, 'r') as check_point_file:
            pass
