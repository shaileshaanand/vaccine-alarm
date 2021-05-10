from json.decoder import JSONDecodeError
import requests
from requests.api import head
URL = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{id}"

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://apisetu.gov.in/public/api/cowin',
    'Origin': 'https://apisetu.gov.in',
    'Connection': 'keep-alive',
    'If-None-Match': 'W/"5d8-2jrF3Zf1hjCMuSob9rLD7lhEGJI"',
    'TE': 'Trailers',
}
states = requests.get(
    "https://cdn-api.co-vin.in/api/v2/admin/location/states",
    headers=headers
).json()["states"]
for state in states:
    response_raw = requests.get(
        URL.format(id=state["state_id"]),
        headers=headers
    )
    try:
        response = response_raw.json()
    except JSONDecodeError:
        print("state skipped", state)

    print("## " + state["state_name"])
    print("District | District ID")
    print("-------- | -----------")
    for district in response["districts"]:
        print(f'{district["district_name"]} | {district["district_id"]}')
    print()
