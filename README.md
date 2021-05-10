# Vaccine Alarm

Sounds an alarm if vaccine is available in your district.

## Usage

```
check.py [OPTIONS]

Options:
-id, --district-id INTEGER [required]
-d, --delay INTEGER
-l, --age-limit INTEGER
-b, --blacklist INTEGER
-s, --min-seats INTEGER
--help Show this message and exit.
```

### Install Dependencies

```bash
pipenv install
```

### Run checker

```bash
python src/check.py
```
