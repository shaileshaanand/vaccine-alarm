import requests
from pprint import pprint
from datetime import date
import simpleaudio as sa
import time


DISTRICT_ID = 97


def play_alarm(count: int):
    sound_file = 'assets/alarm.wav'
    for _ in range(count):
        sa.WaveObject.from_wave_file(sound_file).play().wait_done()


def sleep_with_progress(seconds: int):
    for _ in range(seconds):
        print(".", flush=True, end="")
        time.sleep(1)
    print()


def check():

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.cowin.gov.in',
        'Connection': 'keep-alive',
        'Referer': 'https://www.cowin.gov.in/',
        'TE': 'Trailers',
        'If-None-Match': 'W/"29da8-hpVXpOen2PnjOlRfXqrEVF7FjX4"',
    }

    params = (
        ('district_id', DISTRICT_ID),
        ('date', date.today().strftime("%d-%m-%Y")),
    )
    try:
        response = requests.get(
            'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict',
            headers=headers,
            params=params,
        )
    except Exception:
        print("ERROR")

    found = False
    for center in response.json()["centers"]:
        for session in center["sessions"]:
            if session["min_age_limit"] < 45 and session["available_capacity"] > 0:
                found = True
                print(center["name"] + "," + str(center["pincode"]), "has",
                      session["available_capacity"], "vaccine slots for", session["vaccine"])

    if not found:
        print("Could not find any slots.")
    else:
        play_alarm(5)
    return response


if __name__ == "__main__":
    while True:
        check()
        sleep_with_progress(60)
