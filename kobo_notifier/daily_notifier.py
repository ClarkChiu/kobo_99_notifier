import os
import click
from BasicFuncs import BasicFuncs


@click.command()
@click.option('-m', '--message_type', default=1, help='message type. 1: Kobo 99; 2: Kobo group')
def daily_notifier(message_type):
    if message_type == 1:
        event_name='Kobo99'
    elif message_type == 2:
        event_name='KoboGroup'

    basic_func = BasicFuncs(event_name=event_name)
    today_99_book = basic_func.get_daily_onsale_book('https://www.kobo.com/tw/zh')

    if today_99_book:
        if today_99_book['Coupon']:
            coupon_message = f'{today_99_book["Coupon"]}'
        else:
            coupon_message = '不需折扣碼'

        book_url = today_99_book['URL'].replace(basic_func.age_verify_url, '')

        if message_type == 1:
            message_list = [
                (
                    f'{basic_func.today.strftime("%Y/%m/%d")} Kobo 99 特價書籍\n\n'
                    f'書名：{today_99_book["Name"]}\n'
                    f'作者：{today_99_book["Author"]}\n'
                    f'出版社：{today_99_book["Publisher"]}\n'
                    f'出版日期：{today_99_book["PublishDate"]}\n\n'
                    f'簡介：\n{today_99_book["Intro"]}\n'
                    f'[購買連結]({book_url})'
                ),
                f'`{coupon_message}`',
            ]
        elif message_type == 2:
            message_list = [
                f'今日優惠：《{today_99_book["Name"]}》\n'
                f'99 元-折扣碼: `{coupon_message}`\n'
                f'[購買連結]({book_url})',
            ]

        basic_func.create_telegram_send_conf(
            telegram_token=os.getenv('TELEGRAM_TOKEN'),
            telegram_to=os.getenv('TELEGRAM_TO')
        )

        basic_func.send_notification(message_list)
    else:
        print('The daily onsale web page is not available or parsing error')

if __name__ == '__main__':
    daily_notifier()