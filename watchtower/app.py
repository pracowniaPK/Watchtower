import datetime
import time
import os
import math

from flask import Flask, current_app, render_template
from flask_apscheduler import APScheduler
import requests

from db import get_db, init_db
from config import Config
from model import check


app = Flask(__name__)

def check_job(sites_list):
    res = {}
    for address, pattern in sites_list:
        t1 = time.time()
        try:
            r = requests.get(address)
        except requests.ConnectionError as e:
            res[address] = check(address, 0, 0, notes=str(e))     
            continue
        t2 = time.time()
        dt = math.floor((t2-t1)*1000)
        res[address] = check(address, r.status_code, dt)
        if pattern not in r.text:
            res[address].ok = False
            res[address].notes = 'Pattern does not match.'
    
    print(datetime.datetime.now())
    for address in res:
        with app.app_context():
            res[address].db_insert()
    print()

app.config.from_object(Config())
app.config.from_mapping(DATABASE=os.path.join(app.instance_path, 'db.sqlite'))

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.route('/')
def index():
    with app.app_context():
        latest = check.db_get_latest()
    return render_template('index.html', checks=latest)

# if __name__ == "__main__":

#     with app.app_context():
#         init_db()

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

app.run(use_reloader=False)
