from fuzzywuzzy import fuzz
from json.decoder import JSONDecodeError
import requests
from requests.api import head
import check 

URL = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{id}"

def match(ask, listF, limit = 70):
    while True:
        Str1 = input(ask)
        matches = {}
        for district in listF:
            rat = fuzz.token_set_ratio(Str1.lower(),district.lower())
            if rat >= limit:
                matches[district] = rat
        if len(matches) == 0:
            print("No match Found!\n")
        else: break
    maxim = 0
    for ds, rs in matches.items():
        if rs < maxim:
            matches[ds] = 0
        else: maxim = rs
    ret = []
    for ds, rs in matches.items():
        if rs != 0:
            ret.append(ds)
    if len(ret) > 1:
        n = 1
        print("Though your input did not completely match with anything,\nit did match partially with some of them...\n")
        for res in ret:
            print(f"{n}. {res}")
            n += 1
        while True:
            n = int(input("\nEnter the index of the desired result: "))
            if n not in range(1, len(ret)+1) :
                print("Enter a valid integer!")
            else: break
        return ret[n-1]
    else: return ret[0]

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

states = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states", headers=headers).json()["states"]

statesSrc = match("\nEnter your State: ", [state["state_name"] for state in states])
print(f"Searching for {statesSrc}.")
distList = {}
for state in states:
    if state["state_name"] == statesSrc:
        response_raw = requests.get(URL.format(id=state["state_id"]), headers=headers)
        try:
            response = response_raw.json()
        except JSONDecodeError:
            print("state skipped", state)
        for district in response["districts"]:
            distList[district["district_name"]] = district["district_id"]
        # print(list(distList.keys()))
       
districtSrc = match("\nEnter your District: ", distList.keys())
# print(districtSrc)
for district, ID in distList.items():
    if district == districtSrc:
        print(f'District ID for {districtSrc} is {ID}.\n')



# check.check(ID, 18, [], 1)
delay = 60

while True:
        check.check(ID, 18, [], 1)
        check.sleep_with_progress(delay)
