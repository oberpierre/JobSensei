from flask import Flask
from graphql_server.flask import GraphQLView
from schema import schema

server = Flask(__name__)

server.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))

if __name__ == '__main__':
    server.run()