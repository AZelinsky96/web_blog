
from flask import Flask

app = Flask(__name__)

@app.route('/') # www.mysite.com/api
def hello_method():
    return "Hello World!"

def main():
    app.run()

if __name__ == "__main__":
    main()