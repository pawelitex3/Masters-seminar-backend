from flask import Flask

app = Flask(__name__)

@app.route("/test")
def test():
    return "<p>123</p"