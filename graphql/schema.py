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

class Job(ObjectType):
    uuid = String()
    title = String()
    summary = String()

class Query(ObjectType):
    jobs = List(Job)

    def resolve_jobs(root, info):
        jobs = client.jobsensei.listings_categorized.find()
        return [
            Job(
                uuid=job.get('uuid', None),
                title=job.get('jobTitle', None),
                summary=job.get('summary', None)
            ) for job in jobs
        ]

schema = Schema(query=Query)