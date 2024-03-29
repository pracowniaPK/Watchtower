import datetime
import time
import os
import math

from flask import Flask, render_template, Response
from apscheduler.schedulers.background import BackgroundScheduler
import requests

from watchtower.config import Config, sites_list, seconds_interval
from watchtower.model import check


def get_check_job(app):
    def wrapper(sites_list, record=True):
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
    return wrapper

def create_app(dev_config=None):
    app = Flask(__name__)

    app.config.from_object(Config())
    app.config.from_mapping(DATABASE=os.path.join(app.instance_path, 'db.sqlite'))

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if dev_config is not None:
        app.config.from_mapping(dev_config)

    @app.route('/')
    def index():
        with app.app_context():
            latest = check.db_get_latest()
        ok = 0
        err = 0
        for ch in latest:
            if ch['ok']:
                ok += 1
            else:
                err += 1
        return render_template('index.html', checks=latest, ok=ok, err=err)
    
    @app.route('/get_log')
    def get_log():
        with app.app_context():
            latest = check.db_get_latest()
        log = ''
        for ch in latest:
            log += ('{} code: {}, response time: {}ms, notes: {}, last checked: {}\r\n'
                .format(ch['address'], ch['code'], ch['responsetime'], 
                ch['notes'], ch['created'])
                )
        return Response(
            log, 
            mimetype='text/plain', 
            headers={"Content-disposition": "attachment; filename=checks.log"}
            )

    from watchtower import db
    db.init_app(app)

    check_job = get_check_job(app)
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        check_job, 'interval', [sites_list], seconds=seconds_interval)
    scheduler.start()

    return app
    