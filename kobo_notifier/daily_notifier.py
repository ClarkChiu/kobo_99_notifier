import os
from BasicFuncs import BasicFuncs


basic_func = BasicFuncs(event_name='daily')
if not os.path.exists(basic_func.checkpoint_filepath):
    url_list = [
        'https://www.kobo.com/tw/zh/p/tw-dailydeal-bestofmonth',
        'https://www.kobo.com/tw/zh'
    ]

    try:
        today_99_book = basic_func.get_daily_onsale_book(url_list[0])
    except Exception:
        today_99_book = False

    if not today_99_book:
        today_99_book = basic_func.get_daily_onsale_book(url_list[1])

    if today_99_book:
        basic_func.create_telegram_send_conf(
            telegram_token=os.getenv('TELEGRAM_TOKEN'),
            telegram_to=os.getenv('TELEGRAM_TO')
        )

        if today_99_book["Coupon"]:
            coupon_message = f'{today_99_book["Coupon"]}'
        else:
            coupon_message = '不需折扣碼'

        book_url = today_99_book["URL"].replace(basic_func.age_verify_url, "")

        message_list = [
            (
                f'{basic_func.today.strftime("%Y/%m/%d")}\nKobo 99 特價書籍\n\n'
                f'書名：{today_99_book["Name"]}\n'
                f'作者：{today_99_book["Author"]}\n'
                f'出版社：{today_99_book["Publisher"]}\n'
                f'出版日期：{today_99_book["PublishDate"]}\n\n'
                f'簡介：\n{today_99_book["Intro"]}\n'
                f'購買連結：{book_url}'
            ),
        ]
        basic_func.send_notification(message_list)
        basic_func.send_notification([f'`{coupon_message}`'], parse_mode='markdown')

        basic_func.create_telegram_send_conf(
            telegram_token=os.getenv('TELEGRAM_TOKEN'),
            telegram_to=os.getenv('TELEGRAM_TO_KOBO_GROUP')
        )

        message_list = [
            f'今日優惠：{today_99_book["Name"]} 99 元 折扣碼: `{coupon_message}`\n'
            f'[購買連結]({book_url})',
        ]
        basic_func.send_notification(message_list, parse_mode='markdown')

        basic_func.create_checkpoint()
    else:
        print('The daily onsale web page is not available or parsing error')
else:
    print('Today\'s daily notification has been sent. Program exit')
