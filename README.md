# miniature-happiness

A simple web service for the local transit authority.

Initially the service will support a single train station with an arbitrary number of
train lines running through it, like the Fulton Street station, which hosts the 2, 3, 4,
5, A, C, J, and Z lines.

We would like the service to manage the schedules of the trains in this station,
recording when they arrive as well as reporting when multiple trains are in the station
at the same time.

## Objective & Requirements

Write a small API web service that provides endpoints to track and manage the train
schedules for the station and the data storage mechanism for it.

### Service Capability

The web service should provide a means for clients to post a schedule for a new train
line that runs through this station and verify its correctness:

- A request to `/trains` should accept a train identifier (a string that contains up to
  four alphanumeric characters, e.g. ‘EWR0’, ‘ALP5’, ‘TOMO’, etc) and a list of times
  when the train arrives in the station
- A request to `/trains/<train_id>` should provide the schedule for the specified train
  identifier
- A request to `/trains/next` should return the time two or more trains will be in the
  station.

### Data Storage Capability

This web service uses a key-value store for keeping state, with the following functions:

- A *db.set(key, value)* method to set the value associated with a key.
- A *db.get(key)* method to retrieve the object set at a key.
- A *db.keys()* method to return the list of all defined keys in the database. This
  function returns an empty list if none have been defined.

The service should be threadsafe and use this hypothetical key-value store (with only
these three methods available).

## Installation

The original prompt instructions work nicely, provided pip is up to date.

1. Download the latest major version of Python (3.9.8+)
1. Start virtualenv, install the requirements and start flask, as below:

```bash
$ python3.9 -m venv venv
$ . venv/bin/activate
$ python3 -m pip install --upgrade pip
$ python3 -m pip install -r requirements.txt
$ python3 -m flask run
```

To verify that Flask is running the template service, issue a CURL (or browser request)
to http://127.0.0.1:5000/, e.g.

```bash
% curl -I http://127.0.0.1:5000/ 
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 2
Server: Werkzeug/2.0.2 Python/3.10.0
Date: Fri, 12 Nov 2021 01:42:25 GMT                       
```

To run the test suite, simply execute pytest

```bash
$ python3 -m pytest
```

When I am developing, I am using tox to also:

- format imports using isort
- format code using black
- format markdown files using mdformat
- sorting the whitelist.txt spellchecking dictionary
- manage the requirements.txt file using poetry
- run pytest to check unit tests
- run mypy to check types
- run flake8 with a couple of extra plugins for static code analysis

To run tox:

```bash
$ python3 -m tox
```

*Note, the first time you run tox, it will take a while for it to install all of the
flake8 plugins. It usually is not hung.*

## Template

### Assumptions

- All trains have the same schedule each day (i.e. no special schedules for weekends and
  holidays).

- If there are no times after the specified time value when multiple trains will be in
  the station simultaneously, the service should "wrap around" and return the first time
  of the day when multiple trains arrive at the station simultaneously (tomorrow,
  perhaps)

- If there are no instances when multiple trains are in the station at the same time,
  this method should return no time.

You may define the API contract for this service however you wish, including the format
used for accepting and returning time arguments. The endpoint should return a 2XX
response for valid requests, and a 4xx request for invalid requests (with actual HTTP
code at your discretion).

### Additional Assumptions Made

- All train identifiers are for unique trains, not train lines.
- All time can be simplified to unique 1 minute time slots.
- All database keys have to be strings.
- Database queries are a costly operation, and are to be minimized.
- Times are expressed as 2 digits of hours, 2 digits of minutes (HHMM), and in the
  original template, the test_app.py, line 17, the schedule value of "180" is a type-o,
  since minutes can't be more than 59. See:
  https://github.com/jaustinpage/miniature-happiness/commit/90a9b62e5f63e17284615962e7d6f70e91a46901#diff-a67cb1853203a6f1956991a9d9881d231c4d43557f5baffd45cc672a87e41cc6R17
