import datetime
import time
import os
import math

from flask import Flask, current_app, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import requests

from db import get_db, init_db
from config import Config, sites_list
from model import check


def check_job(sites_list, record=True):
    res = {}
    for address, pattern in sites_list:
        t1 = time.time()
        try:
            r = requests.get(address, timeout=5)
        except (requests.ConnectionError, requests.exceptions.ReadTimeout) as e:
            res[address] = check(address, 0, 0, notes=str(e))     
            continue
        t2 = time.time()
        dt = math.floor((t2-t1)*1000)

        res[address] = check(address, r.status_code, dt)
        if pattern not in r.text:
            res[address].ok = False
            res[address].notes = 'Pattern does not match.'

    if record:    
        for address in res:
            with app.app_context():
                res[address].db_insert()

    print('check done at {}'.format(datetime.datetime.now()))
    return res

def create_app():
    app = Flask(__name__)

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

    @app.route('/timeout')
    def timeout():
        time.sleep(6)
        return 'am sorry i\'m late'

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_job, 'interval', [sites_list], seconds=120) # minutes=120)
    scheduler.start()

    return app
    

if __name__ == "__main__":

#     with app.app_context():
#         init_db()

    app = create_app()
    app.run() # use_reloader=False)
