import logging
from pymongo import MongoClient
from pymongo.errors import BulkWriteError, ConnectionFailure, OperationFailure
from urllib.parse import quote_plus
from datetime import datetime
from uuid import uuid4

logger = logging.getLogger(__name__)

class DataLakeHandler:
    """Handles operations with the MongoDB data lake."""

    def __init__(self, user, password, server, db):
        """Initializes the MongoDB client and connects to the specified database."""

        self.client = MongoClient(self._get_mongo_uri(user, password, server, db))
        self.db = self.client[db]
        self.listings_raw = self.db['listings_raw']
        self.listings_categorized = self.db['listings_categorized']

    def __del__(self):
        """Ensures the MongoDB client is closed upon object destruction."""

        if hasattr(self, 'client') and self.client:
            self.client.close()

    def _get_mongo_uri(self, user, password, server, db):
        if user and password:
            return 'mongodb://%s:%s@%s/%s' % (quote_plus(user), quote_plus(password), quote_plus(server), quote_plus(db))
        return 'mongodb://%s/%s' % (quote_plus(server), quote_plus(db))

    def _get_iso_timestamp(self):
        """Returns the current time in ISO format."""

        return datetime.now().isoformat()

    def get_all_active_listings(self): 
        """Fetches all active listings from the `listings_raw` collection."""

        return list(self.listings_raw.find({'deletedOn': None}))

    def create_new_listing(self, record):
        """Inserts a new listing record into the `listings_raw` collection."""
        uuid = str(uuid4())

        record['createdOn'] = self._get_iso_timestamp()
        record['uuid'] = uuid
        try:
            self.listings_raw.insert_one(record)
            logger.info(f"New listing {uuid} inserted for listing with URL: {record['url']}")
            return uuid
        except e:
            logger.rror(f"Failed to insert new listing for URL: {record['url']}. {e}")
            raise e

    def inactivate_listings(self, urls):
        """Marks listings with the given urls as inactive within the data lake."""

        inactivate_timestamp = self._get_iso_timestamp()
        try:
            self.listings_raw.update_many({'url': {'$in': urls}}, {'$set': {'deletedOn': inactivate_timestamp}})
            self.listings_categorized.update_many({'url': {'$in': urls}}, {'$set': {'deletedOn': inactivate_timestamp}})
            logger.info(f"Listings inactivated. Count: {len(urls)}")
        except (OperationFailure, ConnectionFailure) as e:
            logger.error(f"Failed to inactivate listings. Error: {e}")

    def insert_categorization(self, record):
        """Promotes a listing in our data lake from the bronze to the silver tier."""
        try:
            uuid = record['uuid']
            # Fetching the corresponding listing from the bronze tier
            listing = self.listings_raw.find_one({'uuid': uuid})
            if not listing:
                logger.error(f"Listing for ID {uuid} could not found in bronze tier!")
                return

            # Removing '_id' and 'content' from the listing
            listing.pop('_id', None)
            listing.pop('content', None)

            categorized_listing = {**listing, **record}
            self.listings_categorized.insert_one(categorized_listing)

            logger.info(f"Listing with ID {uuid} categorized.")
        except (OperationFailure, ConnectionFailure, BulkWriteError) as e:
            logger.error(f"Failed to insert categorization for {record['uuid']}. Error: {e}")
