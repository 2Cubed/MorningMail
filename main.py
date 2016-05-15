
from smtplib import SMTP
from email.mime.text import MIMEText
from json import load
from requests import get
from os.path import exists
from shutil import copyfile


class MorningMail:

    def __init__(self):
        self.weather_data = {}

        print("Loading config file...")
        self._load_config()

    def _load_config(self):

        if exists("config.json"):
            with open("config.json") as config:
                self.config = load(config)
        else:
            print(r"Please add your config to config.json and restart.")
            copyfile("config-template.json", "config.json")
            exit(1)

    def send_mail(self):
        print("Sending mail...")
        weather_data = get(
            r"http://api.openweathermap.org/data/2.5/weather",
            params=dict(
                q=','.join(self.config["location"]),
                appid=self.config["openweathermap"]["api_key"]
            )
        ).json()

        conversions = {
            "temperature": {
                "key": "temperature",
                "default": "Farenheit",
                "convert": {
                    "f": 1.8 * weather_data["main"]["temp"] - 459.67,
                    "c": weather_data["main"]["temp"] - 273.15,
                    "k": weather_data["main"]["temp"]
                }
            },
            "distance": {
                "key": "wind_speed",
                "default": "miles",
                "convert": {
                    "m": weather_data["wind"]["speed"],
                    "k": weather_data["wind"]["speed"] / 0.62137
                }
            }
        }

        for unit, data in conversions.items():
            if self.config["units"][unit][0].lower() not in data["convert"]:
                print("{} is not a valid unit. Defaulting to {}.".format(
                    self.config["units"][unit]), data["default"])
                self.config["units"][unit] = data["default"]
            self.weather_data[data["key"]] = data["convert"][
                self.config["units"][unit][0].lower()]

        self.weather_data["humidity"] = weather_data["main"]["humidity"]

        body = """
        {text[greeting]}

        The temperature is {weather[temperature]:.2f} °{units[temperature]}!
        The wind speed is {weather[wind_speed]:.2f} {units[distance]}/h!
        The humidity is {weather[humidity]:.0f}%!

        {text[inspiration]}
        """.format(
            text=self.config["text"],
            weather=self.weather_data,
            units=self.config["units"]
        )

        message = MIMEText(body)
        message['Subject'] = self.config["text"]["subject"]
        message['From'] = self.config["email"]["auth"]["user"]
        message['To'] = ', '.join(self.config["recipients"])

        session = SMTP(**self.config["email"]["config"])
        session.starttls()
        session.login(**self.config["email"]["auth"])
        session.sendmail(
            self.config["email"]["auth"]["user"],
            self.config["recipients"],
            message.as_string()
        )
        session.quit()
        print("Mail sent!")

MorningMail().send_mail()
