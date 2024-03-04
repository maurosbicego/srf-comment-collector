from pony import orm
import settings
from models import db
from methods.rss import *
from methods.article import *
from time import sleep

import logging

numeric_level = getattr(logging, settings.loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % settings.loglevel.upper())


logging.basicConfig(level=numeric_level, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
logging.info(f"Setting up database with config: {settings.db_params}")

db.bind(**settings.db_params)
db.generate_mapping(create_tables=True)

if __name__ == '__main__':
    while True:
        logging.info("Loading data...")
        loadAndSaveAllArticles(getArticleIds(settings.rss_urls))
        checkArticlesForNewlyClosed()
        logging.info(f"Sleeping for {settings.update_delay} seconds")
        sleep(settings.update_delay)