# 樂天 Kobo 書城優惠 Telegram 通知機器人

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ClarkChiu/kobo_99_notifier.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ClarkChiu/kobo_99_notifier/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/ClarkChiu/kobo_99_notifier.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ClarkChiu/kobo_99_notifier/alerts/)
[![codecov](https://codecov.io/gh/ClarkChiu/kobo_99_notifier/branch/master/graph/badge.svg)](https://codecov.io/gh/ClarkChiu/kobo_99_notifier)

# 功能簡介

- 台灣時區 <u>**每日上午 00:05**</u> 自動擷取最新樂天 Kobo 書城當日特價書籍資訊並推播至 Telegram 頻道
- 自動抓取多個跨頁面之書籍資訊

# 訊息格式

第 1 封訊息
```
{{日期}} Kobo 99 特價書籍

書名： {{書名}}

作者： {{作者}}
出版社： {{出版社}}
出版日期： {{出版日期}}

簡介：
{{簡介}}

{{購買連結}}
```

第 2 封訊息（方便行動裝置使用者可以直接複製折扣碼購買）
```
{{折扣碼資訊}}
```



# Telegram 頻道

[**Kobo 每周 99 優惠電子書推播功能**](https://t.me/kobo_99_notifier)



# 推播內容範例圖

![Telegram 推播內容截圖](images/screenshot.jpg)
