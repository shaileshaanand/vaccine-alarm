# Vaccine Alarm

Check for Vaccine availablity in a district at specified intervals and sounds a loud alarm when a slot ia available.

## Usage

```
Usage: check.py [OPTIONS]

  Checks for Vaccine availablity in a district at specified intervals and
  sounds a loud alarm when a slot ia available.

Options:
  -id, --district-id INTEGER  District ID from Cowin API  [required]
  -d, --delay INTEGER         Delay between each request (in seconds).
                              Default: 60 sec

  -l, --age-limit INTEGER     Minimum age limit, Eg. 18 will trigger only for
                              above 18. Default: 18

  -b, --blacklist INTEGER     Pincodes to exclude in your district, will not
                              trigger for these pincodes.

  -s, --min-seats INTEGER     Minimum number of seats to ensure for trigger.
                              Default: 1

  -h, --help                  Show this message and exit.
```

### Install Dependencies

```bash
pipenv install
```

### Run checker

```bash
python src/check.py
```
