from decouple import config
from flask import Flask
from graphql_server.flask import GraphQLView
from schema import schema

server = Flask(__name__)

server.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
))

if __name__ == '__main__':
    from waitress import serve
    serve(server, host=config('HOST', default='127.0.0.1'), port=config('PORT', default='5000'))