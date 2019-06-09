from watchtower.db import get_db 


class check:
    def __init__(self, address, code, response_time, notes=None):
        self.address = address
        self.code = code
        self.ok = code == 200
        self.response_time = response_time
        self.notes = notes

    def __repr__(self):
        return '<check: {}, code: {}, resp time: {}, notes:{}>'.format(
            self.address, self.code, self.response_time, self.notes
            )

    def db_insert(self):
        db = get_db()

        while True:
            website = db.execute(
                'SELECT * FROM website \
                WHERE address = ?', 
                (self.address, )
                ).fetchone()
            if not website:
                db.execute(
                    'INSERT INTO website (address)\
                    VALUES (?)',
                    (self.address, )
                )
                db.commit()
                print('added {} to db'.format(self.address))
            else:
                break
        db.execute(
            'INSERT INTO sitecheck\
            (website_id, code, responsetime, notes, ok)\
            VALUES (?, ?, ?, ?, ?)',
            (website['id'], self.code, self.response_time, self.notes, 1 if self.ok else 0)
        )
        db.commit()

    @staticmethod
    def db_get_latest():
        db = get_db()

        latest = db.execute(
            'SELECT * FROM sitecheck JOIN website \
            ON sitecheck.website_id = website.id \
            WHERE sitecheck.id IN \
            (SELECT max(id) FROM sitecheck GROUP BY website_id)'
        )

        d = []
        for idx, l in enumerate(latest):
            d.append({})
            for k in l.keys():
                d[idx][k] = l[k]
        
        return d

        

