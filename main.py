import requests
import datetime
import os
from twilio.rest import Client

STOCK_NAME = "AAPL"         # Type in the company name. 
COMPANY_NAME = "Apple"      # Company keywords can be found here: https://www.nasdaq.com/market-activity/stocks/screener

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

API_KEY_1 = "Type in API key for Alpha Vantage"
API_KEY_2 = "Type in API key for News Api"

# Obtain credentials for twilio and type in below
account_sid = "account_sid"
auth_token = "auth_token"
client = Client(account_sid, auth_token)

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "datatype": "json",
    "outputsize": "compact",
    "apikey": API_KEY_1,
}

DATE = datetime.date.today() - datetime.timedelta(days=1)
DATE_BEFORE = datetime.date.today() - datetime.timedelta(days=2)

art_param = {
    "q": COMPANY_NAME,
    "from": DATE,
    "language": "en",
    "sortBy": "publishedAt",
    "apiKey": API_KEY_2,
}

response = requests.get(STOCK_ENDPOINT, parameters)

yes_val = response.json()["Time Series (Daily)"][str(DATE)]["4. close"]
db4yes_val = response.json()["Time Series (Daily)"][str(DATE_BEFORE)]["4. close"]

diff = ((abs(float(yes_val) - float(db4yes_val)))/float(db4yes_val))*100
print(diff)

emoji = "🔻"

if (float(yes_val) - float(db4yes_val)) > 0:
    emoji = '🔺'

if diff >= 0:
    article = requests.get(NEWS_ENDPOINT, art_param)
    for i in range(0, 3):
        body_val = article.json()["articles"][i]["title"]
        cont_val = article.json()["articles"][i]["description"]
        print("")
        message = client.messages.create(
            body=f"TSLA:{emoji}{round(diff, 2)}%\n{body_val}\n{cont_val}",

            # Type in the from and to phone numbers below.
            # The from phone number can be obtained from: https://www.twilio.com/en-us
            # The to phone number is the phone to which sms needs to be sent.
            from_="+1234567890",
            to="+919876543210"
        )

        print(message.sid)
