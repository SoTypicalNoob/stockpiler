from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    from shelf_life_checker import list_expired_items
    expired = list_expired_items('shelf_life.sqlite3')
    from shelf_life_checker import list_expires_soon
    soon_expire = list_expires_soon('shelf_life.sqlite3')
    return render_template("dashboard.html", expired=expired, soon_expire=soon_expire)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
