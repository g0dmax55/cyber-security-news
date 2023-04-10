#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import schedule
import time

account_sid = ''
auth_token = ''
twilio_number = ''
recipient_number = ''

previousData = None

def send_message():

    global previousData

    url = 'https://www.bbc.com/news/topics/cz4pr2gd85qt'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    article = soup.find('div', {'class': 'ssrcss-1f3bvyz-Stack e1y4nx260'})

    headline = article.find('span')

    data = headline.text

    headline2 = article.find('a')

    href_value = headline2['href']

    news = (f"{data}\nhttps://www.bbc.com{href_value}")

    if news != previousData:
        previousData = news
        client = Client(account_sid, auth_token)
        message = news
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=recipient_number
        )

    print(news)

schedule.every().day.at("02:30").do(send_message)

try:
   while True:
        schedule.run_pending()
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExit!")
