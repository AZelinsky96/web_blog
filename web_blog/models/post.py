from datetime import datetime
from uuid import uuid4

class Post(object):

    COLLECTION = "posts"

    def __init__(
        self, blog_id: int, author: str, content: str,
        title: str, database: object, _id: str=None) -> None:
        self.blog_id = blog_id
        self.author = author
        self.content = content
        self.title = title
        self.database = database
        self._id = uuid4().hex if _id is None else _id


    def __repr__(self) -> str:
        return (
            f"<Post object attrs: blog_id='{self.blog_id}, '_id='{self._id}', "
            f"title='{self.title}', author='{self.author}'>"
        )
    def create_json(self) -> dict:
        return {
            "blog_id": self.blog_id,
            "_id": self._id,
            "author": self.author,
            "content": self.content,
            "title": self.title,
            "date_created": datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        }

    def save_to_mongo(self) -> None:
        self.database.insert(
            collection=self.COLLECTION, data=self.create_json()
        )

    def search_for_posts_in_mongo(self, **kwargs) -> list:
        return [post for post in self.database.find(self.COLLECTION, kwargs)]

    @classmethod
    def get_post_from_mongo(cls, _id: int, database: object) -> object:
        post_data = database.find_one(
            collection=cls.COLLECTION, query={"_id": _id}
        )
        return cls(
            database=database,
            **post_data
        )
