import requests
import smtplib
from email.message import EmailMessage
import threading
import sys
import os
import config


def check():
    threading.Timer(300.0, check).start()
    r = requests.get('https://am-i-eligible.covid19vaccine.health.ny.gov/api/list-providers')
    providers = r.json()

    for provider in providers['providerList']:
        #Javits Center
        if provider['providerId'] == 1000: 
            available_apts = provider['availableAppointments']

            if available_apts != 'NAC':
                print("Appointments availabile!")
                msg = EmailMessage()
                msg['Subject'] = 'Appointments available at Javits Center'
                msg['From'] = 'nyc_vaccine_check'
                msg['To'] = config.gmail
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(config.gmail, config.password)
                s.send_message(msg)
                s.quit()
                os._exit(1)
            else:
                print("No appointments")


check()
