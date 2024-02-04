from graphene import Field, List, ObjectType, String, Schema
from pymongo import MongoClient
from decouple import config
from urllib.parse import quote_plus

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
    deleted_on = String()

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
        jobs = client.jobsensei.listings_categorized.find()
        return [
            map_job(job) for job in jobs
        ]
    
    def resolve_job(parent, info, uuid):
        job = client.jobsensei.listings_categorized.find_one({"uuid": uuid})
        if job:
            return map_job(job)
        return None

schema = Schema(query=Query)