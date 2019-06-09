# Watchtower

Watchtower is an app that periodically checks the availability of chosen websites and presents recent data on the website.

## Usage

### Setup
```
$ git clone https://github.com/pracowniaPK/Watchtower.git
$ cd Watchtower
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ pip install -e .
$ export FLASK_APP=watchtower.app:create_app
$ flask init_db
```
### Run server
```
$ source venv/bin/activate
$ export FLASK_APP=watchtower.app:create_app
$ export FLASK_ENV=development
$ flask run
```
### Run tests
```
$ source venv/bin/activate
$ pytest
```

## Configuration

The list of wbsites to be checked is stored in `watchtower\config.py` file as list tuples of addresses and content to mach. `seconds_interval` in the same file determines delay between consecutive checks. E.g.
```
sites_list = [
    ('https://www.google.com/', 'search'),
]
seconds_interval = 120
```

## Possible expansion

The app could be used to conduct measurements from different geographical locations and show combined data. This modification would require changes in existing code as well as building new features.

The most crucial design decision in a choice between client-server architecture in which workers would report to a single central server and peer-to-peer architecture where every server would exchange data with all others.

Changes would concern mainly accommodating storage (model) and visualization (view) of data extended by measurement location.

The most needed new feature would be authentication of servers exchanging data and possibly users (that would enable configuration directly through app website and customization of shown content).
