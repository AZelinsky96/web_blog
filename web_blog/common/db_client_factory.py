
from uuid import uuid4

from web_blog.common.mongo_dao import MongoDao
from web_blog.common.constants import local_uri
from pymongo import MongoClient


def create_local_client() -> MongoClient:
    return MongoClient(local_uri)


CONNECTIONS = {
    "local": create_local_client
}


class MongoClientFactory(object):

    def __init__(self, connection_type: str):
        self.connection_type = connection_type

    def create_client(self) -> MongoClient:
        try:
            return CONNECTIONS[self.connection_type]()
        except KeyError:
            raise KeyError("Unsupported Connection Type")


def initialize_database(connection_type: str, collection_name: str) -> MongoDao:
    mongo_client = MongoClientFactory(connection_type).create_client()
    
    return MongoDao(mongo_client, collection_name)