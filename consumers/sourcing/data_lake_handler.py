from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime

class DataLakeHandler:
    """Handles operations with the MongoDB data lake."""

    def __init__(self, user, password, server, db):
        """Initializes the MongoDB client and connects to the specified database."""

        self.client = MongoClient('mongodb://%s:%s@%s/%s' % (quote_plus(user), quote_plus(password), quote_plus(server), quote_plus(db)))
        self.db = self.client[db]
        self.listings_raw = self.db['listings_raw']

    def __del__(self):
        """Ensures the MongoDB client is closed upon object destruction."""

        if self.client:
            self.client.close()

    def _get_iso_timestamp(self):
        """Returns the current time in ISO format."""

        return datetime.now().isoformat()

    def get_all_active_listings(self): 
        """Fetches all active listings from the `listings_raw` collection."""

        return list(self.listings_raw.find({'deletedOn': None}))

    def create_new_listing(self, record):
        """Inserts a new listing record into the `listings_raw` collection."""

        record['createdOn'] = self._get_iso_timestamp()
        self.listings_raw.insert_one(record)

    def inactivate_listings(self, urls):
        """Marks listings with the given urls as inactive within the data lake."""

        self.listings_raw.update_many({'url': {'$in': urls}}, {'$set': {'deletedOn': self._get_iso_timestamp()}})
