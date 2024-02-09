from graphene import Boolean, Field, List, ObjectType, String, Schema
from pymongo import MongoClient
from decouple import config
from urllib.parse import quote_plus
from bson.codec_options import CodecOptions
from datetime import datetime, timedelta, timezone
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

user = config('MONGO_USER', default='')
password = config('MONGO_PASSWORD', default='')
server = config('MONGO_SERVER', default='localhost:27017')
db = config('MONGO_DB', default='jobsensei')

conn_str = 'mongodb://%s:%s@%s/%s' % (quote_plus(user), quote_plus(password), quote_plus(server), quote_plus(db)) if user and password else 'mongodb://%s/%s' % (quote_plus(server), quote_plus(db))

client = MongoClient(conn_str)

class Location(ObjectType):
    city = String()
    country = String()

class Qualifications(ObjectType):
    required = List(String)
    preferred = List(String)

class Job(ObjectType):
    uuid = String()
    title = String()
    summary = String()
    url = String()
    locations = List(Location)
    skills = List(String)
    responsibilities = List(String)
    qualifications = Field(Qualifications)
    created_on = String()
    is_recent = Boolean()
    deleted_on = String()
    is_deleted = Boolean()

    def resolve_is_recent(parent, info):
        today = datetime.now(tz=timezone.utc)
        try:
            created_on = datetime.fromisoformat(parent.created_on)
            return created_on > today - timedelta(days=7)
        except Exception as e:
            logger.error(f"Failed to resolve is_recent: {e}")
        return False

    def resolve_is_deleted(parent, info):
        return parent.deleted_on != None

def parse_date(candidate):
    if isinstance(candidate, datetime):
        return candidate.isoformat()
    return candidate

def map_job(dict):
    return Job(
        uuid=dict.get('uuid', None),
        title=dict.get('jobTitle', None),
        summary=dict.get('summary', None),
        url=dict.get('url', None),
        locations=dict.get('location', None),
        skills=dict.get('skills', None),
        responsibilities=dict.get('responsibilities', None),
        qualifications=dict.get('qualifications', None),
        created_on=parse_date(dict.get('createdOn', None)),
        deleted_on=parse_date(dict.get('deletedOn', None)),
    )

class Query(ObjectType):
    jobs = List(Job)
    job = Field(Job, uuid=String(required=True))

    def resolve_jobs(parent, info):
        listings = client.jobsensei.listings_categorized.with_options(codec_options=CodecOptions(tz_aware=True))
        jobs = listings.find()
        return [
            map_job(job) for job in jobs
        ]
    
    def resolve_job(parent, info, uuid):
        listings = client.jobsensei.listings_categorized.with_options(codec_options=CodecOptions(tz_aware=True))
        job = listings.find_one({"uuid": uuid})
        if job:
            return map_job(job)
        return None

schema = Schema(query=Query)