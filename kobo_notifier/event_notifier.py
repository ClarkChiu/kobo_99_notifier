import os
import sys
from BasicFuncs import BasicFuncs


basic_func = BasicFuncs(event_name='event')

if os.path.exists(basic_func.checkpoint_filepath):
    sys.exit('Today\'s event notification has been sent. Program exit')

event_onsale_book = basic_func.get_event_onsale_book()

if event_onsale_book:
    print(event_onsale_book)
    basic_func.create_telegram_send_conf()

    message_list = [
        (
            f'標題：{event_onsale_book["Title"]}\n'
            f'Blog 網址：{event_onsale_book["URL"]}'
        ),
        event_onsale_book['Coupon']
    ]

    for book in event_onsale_book["BookList"]:
        message_list.append(
            f'書名：{book["Name"]}\n'
            f'購買連結：{book["URL"]}'
        )

    basic_func.send_notification(message_list)
    basic_func.create_checkpoint()
else:
    print('The event onsale web page is not available or parsing error')
