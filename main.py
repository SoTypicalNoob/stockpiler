from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    from shelf_life_checker import list_expired_items
    expired = list_expired_items('shelf_life.sqlite3')
    from shelf_life_checker import list_expires_soon
    soon_expire = list_expires_soon('shelf_life.sqlite3')
    return render_template("dashboard.html", expired=expired, soon_expire=soon_expire)


@app.route("/add/", methods=["GET", "POST"])
def add_item():
    from shelf_life_checker import add_new_item
    if request.method == "POST":
        brand_name = request.form.get("brandName")
        product_name = request.form.get("productName")
        product_size = request.form.get("productSize")
        product_unit = request.form.get("productUnit")
        stock_expiring = request.form.get("stockExpiring")
        stock_amount = request.form.get("stockAmount")
    #from shelf_life_checker import add_new_item('shelf_life.sqlite3')
        add_new_item('shelf_life.sqlite3', brand_name,
                                    product_name, product_size, product_unit,
                                    stock_expiring, stock_amount)
    return render_template("add_item.html")


@app.route("/delete/", methods=["GET", "POST"])
def delete_item():
    from shelf_life_checker import delete_item
    if request.method == "POST":
        brand_name = request.form.get("brandName")
        product_name = request.form.get("productName")
        product_size = request.form.get("productSize")
        product_unit = request.form.get("productUnit")
        stock_expiring = request.form.get("stockExpiring")
        stock_amount = request.form.get("stockAmount")
    #from shelf_life_checker import add_new_item('shelf_life.sqlite3')
        delete_item('shelf_life.sqlite3', brand_name,
                                    product_name, product_size, product_unit,
                                    stock_expiring, stock_amount)
    return render_template("delete_item.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
