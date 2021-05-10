import requests
from pprint import pprint
from datetime import date
import simpleaudio as sa
import time
import click


def play_alarm(count: int):
    sound_file = 'assets/alarm.wav'
    for _ in range(count):
        sa.WaveObject.from_wave_file(sound_file).play().wait_done()


def sleep_with_progress(seconds: int):
    for _ in range(seconds):
        print(".", flush=True, end="")
        time.sleep(1)
    print()


def check(district_id, age_limit, pincode_blacklist, min_seats):
    pincode_blacklist = set(pincode_blacklist)
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
        ('district_id', district_id),
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
            if session["min_age_limit"] <= age_limit and session["available_capacity"] >= min_seats and center["pincode"] not in pincode_blacklist:
                found = True
                print(center["name"] + "," + str(center["pincode"]), "has",
                      session["available_capacity"], "vaccine slots for", session["vaccine"])

    if not found:
        print("Could not find any slots.")
    else:
        play_alarm(5)
    return response


@click.command()
@click.option("--district-id", "-id", prompt="District id", required=True, type=int)
@click.option("--delay", "-d", default=60)
@click.option("--age-limit", "-l", default=18)
@click.option("--blacklist", "-b", multiple=True, type=int)
@click.option("--min-seats", "-s", default=1)
def main(district_id, delay, age_limit, blacklist, min_seats):
    """Checks for Vaccine availablity in a district at specified intervals"""

    while True:
        check(district_id, age_limit, blacklist, min_seats)
        print(f"Sleeping for {delay} seconds")
        sleep_with_progress(delay)


if __name__ == "__main__":
    main()
