
from uuid import uuid4

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