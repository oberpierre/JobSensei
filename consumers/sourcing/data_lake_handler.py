from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime

class DataLakeHandler:
    def __init__(self, user, password, server, db):
        self.client = MongoClient('mongodb://%s:%s@%s/%s' % (quote_plus(user), quote_plus(password), quote_plus(server), quote_plus(db)))
        self.db = self.client[db]
        self.listings_raw = self.db['listings_raw']

    def __del__(self):
        if self.client:
            self.client.close()

    def _get_iso_timestamp(self):
        return datetime.now().isoformat()

    def get_all_active_listings(self): 
        return list(self.listings_raw.find({'deletedOn': None}))

    def create_new_listing(self, record):
        record['createdOn'] = self._get_iso_timestamp()
        self.listings_raw.insert_one(record)

    def inactivate_listings(self, urls):
        self.listings_raw.update_many({'url': {'$in': urls}}, {'$set': {'deletedOn': self._get_iso_timestamp()}})
