DROP TABLE IF EXISTS website;
DROP TABLE IF EXISTS sitecheck;

CREATE TABLE website (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  address TEXT UNIQUE NOT NULL
);

CREATE TABLE sitecheck (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  website_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  code INTEGER,
  responsetime INTEGER,
  notes TEXT,
  ok INTEGER,
  FOREIGN KEY (website_id) REFERENCES website (id)
);