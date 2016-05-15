
from smtplib import SMTP
from email.mime.text import MIMEText
from json import load
from requests import get
from os.path import exists
from shutil import copyfile


class MorningMail:

    def __init__(self):
        print("Loading config")
        self._load_config()

        print("Sending email")
        self.send_mail()

    def _load_config(self):

        if exists("config.json"):
            with open('config.json') as conf:
                conf = load(conf)

                self.recipient = conf['to']
                self.sender = conf['sender']
                self.password = conf['password']
                self.subject = conf['subject']
                self.smtp_server = conf['server']
                self.state = conf['state']
                self.city = conf['city']
                self.api_key = conf['api_key']
                self.unit = conf['unit']
                self.greeting = conf['greeting']
                self.insperation = conf['insperation']
        else:
            copyfile("config-template.json", "config.json")

    def send_mail(self):
        req = get(
            'http://api.openweathermap.org/data/2.5/weather?q={city},{state}&appid={api_key}'
            .format(city=self.city, state=self.state, api_key=self.api_key))

        data = req.json()

        if self.unit.lower() == "f":
            self.temp = 1.8 * (data['main']['temp'] - 273) + 32
        elif self.unit.lower() == "c":
            self.temp = (data['main']['temp'] - 273.15)
        elif self.unit.lower() == "k":
            self.temp = data['main']['temp']
        else:
            print(self.unit + " is not a valid unit.")
            exit(1)

        self.humid = data['main']['humidity']
        self.wind = data['wind']['speed']

        body = """
        {greeting}

        The current temperate isf {temp} {unit}!
        The wind speed is {wind} mp/h, the current humidity is {humid}!

        {insperation}
        """.format(greeting=self.greeting, temp=int(self.temp), unit=self.unit, wind=self.wind, humid=self.humid, insperation="stuff")

        msg = MIMEText(body)
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = ", ".join(self.recipient)

        session = SMTP(self.smtp_server)
        session.starttls()
        session.login(self.sender, self.password)
        session.sendmail(self.sender, self.recipient, msg.as_string())
        session.quit()

mail = MorningMail()
