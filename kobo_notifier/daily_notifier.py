from BasicFuncs import BasicFuncs


basic_func = BasicFuncs()
today_99_book = basic_func.get_daily_onsale_book()
print(today_99_book)

if today_99_book:
    basic_func.create_telegram_send_conf()

    if today_99_book["Coupon"]:
        coupon_message = f'{today_99_book["Coupon"]}'
    else:
        coupon_message = '不需折扣碼'

    message_list = [
        (
            f'{basic_func.today.strftime("%Y/%m/%d")}\nKobo 99 特價書籍\n\n'
            f'書名：{today_99_book["Name"]}\n\n'
            f'作者：{today_99_book["Author"]}\n'
            f'出版社：{today_99_book["Publisher"]}\n'
            f'出版日期：{today_99_book["PublishDate"]}\n\n'
            f'簡介：\n{today_99_book["Intro"]}\n'
            # f'[購買連結]({today_99_book["URL"]})'
            f'購買連結：{today_99_book["URL"]}'
        ),
        coupon_message
    ]

    basic_func.send_notification(message_list)
