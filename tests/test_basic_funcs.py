import json
import urllib.parse
from kobo_notifier.BasicFuncs import BasicFuncs


def test_get_daily_onsale_book(requests_mock):
    result_file_path = 'tests/data/20200628_book_info.json'
    with open(result_file_path, 'r', encoding='UTF-8') as f:
        book_info = json.loads(f.read())

    # Mock the response of kobo 99 event page
    kobo_99_event_page_path = 'tests/data/20200628_kobo_99_event_page.html'
    with open(kobo_99_event_page_path, 'r', encoding='UTF-8') as f:
        requests_mock.get(
            'https://www.kobo.com/tw/zh/p/tw-dailydeal-bestofmonth',
            text=f.read()
        )

    # Mock the response of book page
    kobo_99_book_page_path = 'tests/data/20200628_kobo_99_book_page.html'
    with open(kobo_99_book_page_path, 'r', encoding='UTF-8') as f:
        requests_mock.get(
            book_info['URL'],
            text=f.read()
        )

    basic_func = BasicFuncs()
    assert book_info == basic_func.get_daily_onsale_book()


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
