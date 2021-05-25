import requests
from datetime import date
from playsound import playsound
import time
import click


def play_alarm(count: int):
    sound2 = "../assets/alarmVar.wav"
    for _ in range(count):
        playsound(sound2)


def sleep_with_progress(seconds: int):
    print(f"Sleeping for {seconds} seconds")
    print("Elapsed seconds =  ", end="")
    erase = ""
    d = 1
    for i in range(seconds):
        if not (i) % d:
            erase += "\b"
            d *= 10
        print(erase + str(i+1), end="", flush=True)
        time.sleep(1)
    print()


def check(district_id, age_limit=18, pincode_blacklist=[], min_seats=1):
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


@click.command("check.py",
               context_settings={
                   "help_option_names": ['-h', '--help']
               })
@click.option("--district-id",
              "-id",
              prompt="District id",
              required=True,
              help="District ID from Cowin API, Get your district ID at http://bit.ly/districtid",
              type=int)
@click.option("--delay",
              "-d",
              help="Delay between each request (in seconds). Default: 60 sec",
              default=60)
@click.option("--age-limit",
              "-l",
              help="Minimum age limit, Eg. 18 will trigger only for above 18. Default: 18",
              default=18)
@click.option("--blacklist",
              "-b",
              multiple=True,
              help="Pincodes to exclude in your district, will not trigger for these pincodes.",
              type=int)
@click.option("--min-seats",
              "-s",
              help="Minimum number of seats to ensure for trigger. Default: 1",
              default=1)
def main(district_id, delay, age_limit, blacklist, min_seats):
    """
    Checks for Vaccine availablity in a district at specified intervals
    and sounds a loud alarm when a slot ia available.
    """
    while True:
        check(district_id, age_limit, blacklist, min_seats)
        sleep_with_progress(delay)


if __name__ == "__main__":
    main()
