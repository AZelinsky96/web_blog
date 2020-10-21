

class User(object):

    def __init__(self, email: str, password: str, database: object, _id: str=None):
        self.email = email
        self.password = password
        self.database = database
        self._id = uuid4().hex if _id is None else _id

    @classmethod
    def retrieve_user_helper(cls, database: object, search_word: str, search_content: str) -> object:
        data = database.find_one("users", {search_word: search_content})
        if data:
            return cls(*data)

    @classmethod
    def get_by_email(cls, email, database: object) -> object:
        return cls.retrieve_user_helper(database, "email", email)

    @classmethod
    def get_by_id(cls, _id: str, database: object) -> object:
        return cls.retrieve_user_helper(database, "_id", _id)

    @staticmethod
    def login_valid(email: str, password: str, database: object) -> bool:
        user = User.get_by_email(email=email, database=database)
        if user:
            return user.password == password
        return False

    @classmethod
    def register(cls, email: str, password: str, database: object) -> bool:
        user = cls.get_by_email(email=email, database=database)
        if not user:
            new_user = cls(email=email, password=password, database=database)
            new_user.save_to_mongo()
            return True
        else:
            return False

    def login(self):
        pass

    def get_blogs(self):
        pass

    def create_json(self):
        pass

    def save_to_mongo(self):
        pass
