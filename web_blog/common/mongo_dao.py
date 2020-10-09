class MongoDao(object):

    def __init__(self, client: object, database: object):
        self.client = client
        self.database = client[f'{database}']
    
    def __repr__(self) -> str:
        return f"<MongoDao object: database='{self.database}'"
    
    def insert(self, collection: str, data: dict) -> None:
        try:
            self.database[collection].insert(data)
        except Exception as e:
            raise Exception(f"Error occured during insert operation: {e}.")
    
    def find(self, collection: str, query: dict) -> object:
        return self.database[collection].find(query)
    
    def find_one(self, collection: str, query: dict) -> object:
        return self.database[collection].find_one(query)