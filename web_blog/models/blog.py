from datetime import datetime
from uuid import uuid4

from web_blog.models.post import Post


class Blog(object):

    COLLECTION = "blogs"

    def __init__(
        self, author: str, author_id: str, blog_title: str, description: str,
        database: object, _id: str=None,
        ) -> None:
        self.author = author
        self.author_id = author_id
        self.blog_title = blog_title
        self.description = description
        self.database = database
        self._id = uuid4().hex if _id is None else _id

    def __repr__(self) -> str:
        return (
            f"<Blog object: blog_title='{self.blog_title}', author='{self.author}', "
            f"_id='{self.blog_title}', description='{self.description}'>"
        )

    def create_post(self, title: str, content: str) -> None:
        Post(
            _id=self._id, author=self.author, title=title,
            content=content, database=self.database
        ).save_to_mongo()

    def find_posts_from_blog(self) -> list:
        return [post for post in self.database.find("posts", {"_id": self._id})]

    def save_to_mongo(self):
        self.database.insert(
            collection=self.COLLECTION, data=self.create_json()
        )

    def create_json(self):
        return {
            "_id": self._id,
            "author": self.author,
            "author_id": self.author_id,
            "blog_title": self.blog_title,
            "description": self.description,
            "date_created": datetime.utcnow().strftime("%Y-%m-%d  %H:%M:%S")
        }

    @classmethod
    def get_blog_from_mongo(cls, _id: str, database: object) -> object:
        blog_data = database.find_one(
            collection=cls.COLLECTION, query={"_id": _id}
        )
        return cls(
            database=database,
            **blog_data
        )

    @classmethod
    def find_by_author_id(cls, author_id):
        blog_data = self.database.find(
            collection='blogs', query={'_id': author_id}
        )
        return [cls(**blog) for blog in blog_data]