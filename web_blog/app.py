
from flask import Flask, render_template, request, session, make_response
from web_blog.common.db_client_factory import initialize_database
from web_blog.models.user import User
from web_blog.models.blog import Blog
from web_blog.models.post import Post


app = Flask(__name__)
app.secret_key = "test_secret"
mongo_db = initialize_database(connection_type="local", database_name="fullstack")


def get_email_and_password():
    return request.form["email"], request.form['password']


@app.route("/")
def home_template():
    return render_template("home.html")


@app.route('/login') # www.mysite.com/api
def login_template():
    return render_template("login.html")


@app.route('/register')
def register_template():
    return render_template("register.html")


@app.route('/auth/login', methods=['POST'])
def login_user():
    email, password = get_email_and_password()

    if User.login_valid(email, password, mongo_db):
        User.login(email)
    else:
        session['email'] = None

    return render_template("profile.html", email=session['email'])


@app.route("/auth/register", methods=["POST"])
def register_user():
    email, password = get_email_and_password
    User.register_user(email, password)

    return render_template("profile.html", email=session['email'])


@app.route("/blogs/<string:user_id>")
@app.route("/blogs")
def user_blogs(user_id=None):
    if user_id:
        user = User.get_by_id(_id=user_id, database=mongo_db)
    else:
        user = User.get_by_email(email=session['email'], database=mongo_db)
    blogs = user.get_blogs()
    return render_template("user_blogs.html", blogs=blogs, email=user.email)


@app.route("/posts/<string:blog_id>")
def blog_posts(blog_id):
    blog = Blog.get_blog_from_mongo(_id=blog_id, database=mongo_db)
    posts = blog.find_posts_from_blog()
    return render_template('posts.html', posts=posts, blog_title=blog.blog_title, blog_id=blog._id)


@app.route("/blogs/new", methods=["POST", "GET"])
def create_new_blog():
    if request.method == "GET":
        return render_template("new_blog.html")
    else:
        title=request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'], mongo_db)
        
        new_blog = Blog(
            author=user.email,
            author_id=user._id,
            blog_title=title,
            description=description,
            database=mongo_db
        )
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))


@app.route("/posts/new/<string:blog_id>", methods=["POST", "GET"])
def create_new_post(blog_id):
    if request.method == "GET":
        return render_template("new_post.html", blog_id=blog_id)
    else:
        title=request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'], mongo_db)
        
        new_post = Post(
            author=user.email,
            title=title,
            content=description,
            blog_id=blog_id,
            database=mongo_db
        )
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))


def main():
    app.run(port=4996)


if __name__ == "__main__":
    main()