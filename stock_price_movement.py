import requests
from twilio.rest import Client
from newsapi.newsapi_client import NewsApiClient
import datetime as dt

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


# Optional: Format the SMS message like this:
"""
TSLA: ðŸ”º2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: ðŸ”»5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

STOCK = "TSLA"
COMPANY_NAME = "Tesla"
stock_api_key = "7247VSA00DPZWKOH"
news_api_key = "061b2ae23aa84de5ba736ff62da073cc"
account_sid = 'AC22d36274c59681a3d827df9aa5df5cdb'
auth_token = 'a43fc4450854e059ce2653237923cb66'


def get_news():
    para = {
        'country': 'us',
        'q': COMPANY_NAME,
        'category': 'business',
        'apiKey': news_api_key
    }
    top_headlines = requests.get(url="https://newsapi.org/v2/top-headlines?", params=para)
    return ["{}\n{}".format(i['title'], i['url']) for i in top_headlines.json()['articles']]


# print("\n".join(get_news()))


def get_stock_price():
    para = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': STOCK,
        'apikey': stock_api_key
    }
    stock_price = requests.get(url="https://www.alphavantage.co/query?", params=para)
    return stock_price.json()


print(get_stock_price())


def past_four_days():
    today = dt.date.today()
    onedayago = today - dt.timedelta(days=1)
    twodayago = today - dt.timedelta(days=2)
    threedayago = today - dt.timedelta(days=3)
    return (today, onedayago, twodayago, threedayago)


def send_txt(stock_alert):
    txt_body = "\n".join(get_news())
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="AIjeet alert:{}\n{} ".format(stock_alert, txt_body),
        from_='+12158834018',
        to='+14086031986'
    )
    print(message.status, message.sid)


# print(past_four_days())
# today_stock_price = get_stock_price()['Time Series (Daily)'][str(past_four_days()[2])]['1. open']
# threedayago_stock_price= get_stock_price()['Time Series (Daily)'][str(past_four_days()[3])]['4. close']
# stock_diff = (float(today_stock_price) - float(threedayago_stock_price))*100/float(today_stock_price)
# print(stock_diff)

def get_stock_price_diff():
    what_day = dt.datetime.now().weekday()
    stock_diff = 0
    if what_day == 0:  # Monday
        today_stock_price = get_stock_price()['Time Series (Daily)'][str(past_four_days()[0])]['1. open']
        threedayago_stock_price = get_stock_price()['Time Series (Daily)'][str(past_four_days()[3])]['4. close']
        stock_diff = abs(float(today_stock_price) - float(threedayago_stock_price))
        print(today_stock_price, threedayago_stock_price)

    if what_day in [1, 2, 3, 4]:  # Tue-Fri
        today_stock_price = get_stock_price()['Time Series (Daily)'][str(past_four_days()[0])]['1. open']
        onedayago_stock_price = get_stock_price()['Time Series (Daily)'][str(past_four_days()[1])]['4. close']
        print(today_stock_price,onedayago_stock_price)
        stock_diff = (float(today_stock_price) - float(onedayago_stock_price)) * 100 / float(today_stock_price)

    # stock_diff = 10.96
    if abs(stock_diff) >= 2:
        if stock_diff < 0:
            send_txt("{} 🔻 down {}%".format(COMPANY_NAME, round(stock_diff,2)))
            return "Message Sent"
        else:
            send_txt("{} 💹 Up {}%".format(COMPANY_NAME, round(stock_diff,2)))
            return "Message Sent"



print(get_stock_price_diff())
