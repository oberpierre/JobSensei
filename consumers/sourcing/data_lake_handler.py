from pymongo import MongoClient
from urllib.parse import quote_plus

class DataLakeHandler:
    def __init__(self, user, password, server, db):
        self.client = MongoClient('mongodb://%s:%s@%s/%s' % (quote_plus(user), quote_plus(password), quote_plus(server), quote_plus(db)))
        self.db = self.client[db]
        self.listings_raw = self.db['listings_raw']

    def __del__(self):
        if self.client:
            self.client.close()

    def get_all_active_listings(self): 
        return list(self.listings_raw.find({'deleted_data': None}))

    def create_new_listing(self, record):
        self.listings_raw.insert_one(record)
