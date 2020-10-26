
from flask import Flask, render_template, request, session
from web_blog.common.db_client_factory import initialize_database
from web_blog.models.user import User


app = Flask(__name__)
app.secret_key = "test_secret"
mongo_db = initialize_database("local", "fullstack")


def get_email_and_password():
    return request.form["email"], request.form['password']


@app.route('/') # www.mysite.com/api
def hello_method():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_user():
    email, password = get_email_and_password()

    if User.login_valid(email, password, mongo_db):
        User.login(email)
    else:
        session['email'] = None

    return render_template("profile.html", email=session['email'])


@app.route("/register", methods=["POST"])
def register_user():
    email, password = get_email_and_password
    User.register_user(email, password)
    session['email'] = email

    return render_template("profile.html", email=session['email'])


def main():
    app.run()

if __name__ == "__main__":
    main()