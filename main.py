
import smtplib
from email.mime.text import MIMEText
import urllib3
import json
import requests
import sys
import socket
from random import Random

recipient = ["recipient"]
sender = "sender"
subject = "Good Morning!"
smtpServer = ""

state = ""
city = ""
apiKey = ""

celcius = False;

def main():
    # Using requests, we can get the json output from this url. Then we're formatting it to replace the placeholders with the actual values.
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q={0},{1}&appid={2}'.format(city, state, apiKey))

    # Getting the json
    data = r.json()

    if celcius == True:
        # Conversion for Kelvin to Celcius
        temp = (data.get('main').get('temp') - 273.15)
    else:
        # Conversion for Kelvin to Fahrenheit
        temp = 1.8 * (data.get('main').get('temp') - 273) + 32

    humid = data.get('main').get('humidity')
    wind = data.get('wind').get('speed')

    special = ""

    # The celcius ones are just rough of what they should be around.

    if celcius == True:
        if temp <= -1:
            special = "Brr! It's cold out!"
        elif temp > -1 and temp < 10:
            special = "It's kind of warm today! Maybe go outside? Nah. You have too much to do :)"
        elif temp > 10 and temp < 15:
            special = "It's quite warm today!"
        elif temp > 15 and temp < 26:
            special = "It's very warm!"
        else if temp >= 26:
            special = "HOLY BUTTS IT'S HOT! DON'T EVEN THINK ABOUT OUTSIDE!"
    else:
        if temp <= 30:
            special = "Brr! It's cold out!"
        elif temp > 30 and temp < 50:
            special = "It's kind of warm today! Maybe go outside? Nah. Lol you have too much to do :)"
        elif temp > 50 and temp < 60:
            special = "It's quite warm today!"
        elif temp > 60 and temp < 80:
            special = "It's very warm!"
        else if temp >= 80:
            special = "HOLY BUTTS IT'S HOT! DON'T EVEN THINK ABOUT OUTSIDE!"

    if celcius == True:
        unit = "C"
    else:
        unit = "F"

    # Creating the variable 'x' containing all the formatting for the body message
    x = [int(temp), unit, wind, humid, special]

    body = """
    Good Morning!

    The current temperate is %s %s!
    The wind speed is %s mp/h, the current humidity is %s! %s

    Have an amazing day. You rock. :)
    """

    # Formatting body with the 'x' variable
    msg = MIMEText(body % tuple(x))
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipient)

    session = smtplib.SMTP(smtpServer)
    session.starttls()
    session.login(sender, password)
    session.sendmail(sender, recipient, msg.as_string())
    session.quit()

main()
