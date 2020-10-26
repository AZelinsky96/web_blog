from uuid import uuid4

from datetime import datetime

from web_blog.models.blog import Blog
from flask import session


class User(object):

    def __init__(
        self, email: str, password: str, database: object,  _id: str=None
    ):
        self.email = email
        self.password = password
        self.database = database
        self._id = uuid4().hex if _id is None else _id

    @classmethod
    def retrieve_user_helper(cls, database: object, search_word: str, search_content: str) -> object:
        data = database.find_one("users", {search_word: search_content})
        if data is not None:
            data['database'] = database
            return cls(**data)

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
            session['email'] = email
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        session['email'] = user_email
    
    @staticmethod
    def logout(user_email):
        session['email'] = None

    def create_json(self):
        return {
            "email": self.email,
            "_id": self._id,
            "password": self.password
        }

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def save_to_mongo(self):
        self.database.insert("user", self.create_json())

    def new_blog(self, blog_title, description):
        blog = Blog(
            author=self.email, blog_title=blog_title, description=description,
            author_id=self._id, database=self.database
        )
        blog.save_to_mongo()

    @staticmethod
    def new_post(self, blog_id, title, content, database):
        blog = Blog.get_blog_from_mongo(database=database, _id=blog_id)
        blog.create_post(title=title, content=content)
