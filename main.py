import requests
from datetime import datetime
import smtplib
import time

#-------------------------- CONSTANTS ---------------------------#
MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude
MY_EMAIL = "pradipsinhdemo@gmail.com"
MY_PASSWORD = "jlvt rgve zbga hbtj"
RECEIVER_EMAIL = "umangvdemo1@gmail.com"

#-------------------------- FUNCTIONS ---------------------------#
def iss_is_close():
    """Return True if the ISS is close to your current location."""
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()

    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])
    # Check Your position is within +5 or -5 degrees of the ISS position.
    if (MY_LAT-5) <= iss_latitude<= (MY_LAT+5) and (MY_LONG-5) <= iss_longitude <= (MY_LONG+5):
        return True

def is_night():
    """Return True if there is Night."""
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0, #'0' for 24-hours formate
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour

    if sunset <= time_now <= sunrise:
        return True

#-------------------------- SEND EMAIL ---------------------------#
while True:
    time.sleep(30)
    # Keep Run this in background for 24 hours for getting email.
    if iss_is_close() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=RECEIVER_EMAIL,
                                msg="Subject:ISS Overhead Alert"
                                    "\n\nLook Up ISS is Visible in the sky.")
