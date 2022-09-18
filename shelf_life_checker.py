#!/usr/bin/env python3
"""This script has modules to query the databes
Please notice that this is just a placeholder yet, not fully operational."""

import os
import sys
import sqlite3
import datetime
# For barcode scanning:
# read_barcodes
import cv2
from pyzbar import pyzbar

def create_database(file):
    conn = sqlite3.connect(file)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS Brand")
    cur.execute("DROP TABLE IF EXISTS Product")
    cur.execute("DROP TABLE IF EXISTS Stock")
    cur.execute("""CREATE TABLE Brand (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE)""")
    cur.execute("""CREATE TABLE Product (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        barcode INTEGER UNIQUE,
        name TEXT,
        brand_id INTEGER,
        size INTEGER,
        unit TEXT)""")
    cur.execute("""CREATE TABLE Stock (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        product_id INTEGER,
        expiring DATE,
        amount INTEGER)""")


##### Query #####


def list_database(filename):
    """Lists the whole database into STD Output

    Arg:
        filename: sqlite database

    Returns:
        Prints out the whole database
    """
    connect = sqlite3.connect(filename)
    cursor = connect.cursor()
    cursor.execute(
        """SELECT Brand.name, Product.name, Stock.expiring, Product.size, Product.unit, Stock.amount
        FROM Stock JOIN Product JOIN Brand ON
        Stock.product_id = Product.id AND
        Product.brand_id = Brand.id ORDER BY Stock.expiring"""
    )
    rows = cursor.fetchall()
    return rows


def list_expired_items(filename):
    """Lists of the expired items.

    Arg:
        file: sqlite database

    Returns:
        Prints out the the expired items
    """
    connect = sqlite3.connect(filename)
    cursor = connect.cursor()
    cursor.execute(
        """SELECT Brand.name, Product.name, Stock.expiring, Stock.amount
        FROM Stock JOIN Product JOIN Brand ON
        Stock.product_id = Product.id AND
        Product.brand_id = Brand.id
        WHERE date(Stock.expiring) < date('now') ORDER BY Stock.expiring"""
    )
    rows = cursor.fetchall()
    return rows


def list_expires_soon(filename):
    """Lists of those items that expires within a week.

    Arg:
        file: sqlite database

    Returns:
        Prints out the items will be expire within a week.
    """
    connect = sqlite3.connect(filename)
    cursor = connect.cursor()
    cursor.execute(
        """SELECT Brand.name, Product.name, Stock.expiring, Stock.amount
        FROM Stock JOIN Product JOIN Brand ON
        Stock.product_id = Product.id AND
        Product.brand_id = Brand.id
        WHERE date(Stock.expiring) BETWEEN date('now') AND date('now', '+1 month')
        ORDER BY Stock.expiring"""
    )
    rows = cursor.fetchall()
    return rows


def check_item_existence(filename, barcode):
    """Check if an item is already in the database or not.

    Arg:
        filename: sqlite database
        barcode: Barcode of the product

    Returns:
        True/False, Details of the item.
    """
    connect = sqlite3.connect(filename)
    cursor = connect.cursor()
    # cursor.execute("SELECT id FROM Brand WHERE name = ?", (brand_name,))
    cursor.execute("SELECT Brand.name, Product.name, Product.size, Product.unit FROM Product JOIN Brand ON Product.brand_id = Brand.id WHERE Product.barcode = ?", (barcode,))
    row = cursor.fetchone()
    return row


##### Add/Update/Remove #####


def add_new_item(filename,
                 barcode,
                 brand_name,
                 product_name,
                 product_size,
                 product_unit,
                 stock_expiring,
                 stock_amount):
    """Add new item/items to the database.

    Arg:
        filename: sqlite database
        barcode: barcode of the product
        brand_name: brand of the product (e.g.: 'Bonduelle')
        product_name: name of the product (e.g.: 'red beans')
        product_size: number of the size of the product (e.g.: liquid product which is 100ml then: '100')
        product_unit: the unit name of the size of the product (e.g.: ml from 100ml)
        stock_expiring: expiring date in YYYY-MM-DD
        stock_amount: amount of the product (e.g.: in case of you have 5 bottle, then: '5')

    Returns:
        None.
    """
    connect = sqlite3.connect(filename)
    cursor = connect.cursor()
    cursor.execute("INSERT OR IGNORE INTO Brand (name) VALUES (?)", (brand_name,))
    cursor.execute("SELECT id FROM Brand WHERE name = ?", (brand_name,))
    brand_id = cursor.fetchone()[0]

    cursor.execute(
        """INSERT OR IGNORE INTO Product
        (barcode, name, brand_id, size, unit)
        VALUES (?, ?, ?, ?, ?)""",
        (barcode, product_name, brand_id, product_size, product_unit),
    )
    cursor.execute("SELECT id FROM Product WHERE barcode = ?", (barcode,))
    product_id = cursor.fetchone()[0]

    sep_date = stock_expiring.split("-")
    cursor.execute(
        "SELECT amount FROM Stock WHERE product_id = ? AND expiring = ?",
        (product_id, datetime.date(int(sep_date[0]), int(sep_date[1]), int(sep_date[2]))),
    )
    if cursor.fetchone() is None:
        cursor.execute(
            """INSERT INTO Stock (product_id, expiring, amount)
            VALUES (?, ?, ?)""",
            (product_id, datetime.date(int(int(sep_date[0])), int(sep_date[1]), int(sep_date[2])), stock_amount),
        )
    else:
        cursor.execute(
            "SELECT amount FROM Stock WHERE product_id = ? AND expiring = ?",
            (product_id, datetime.date(int(int(sep_date[0])), int(sep_date[1]), int(sep_date[2]))),
        )
        prev_amount = cursor.fetchone()[0]
        amount = int(stock_amount) + prev_amount
        cursor.execute(
            """UPDATE Stock SET amount = ?
            WHERE product_id = ? AND expiring = ?""",
            (amount, product_id, datetime.date(int(int(sep_date[0])), int(sep_date[1]), int(sep_date[2]))),
        )
    connect.commit()


def delete_item(filename, barcode, stock_expiring, stock_amount):
    """Remove item/items from the database. (From Stock table.)

    Arg:
        file: sqlite database
        barcode: Barcode of the product
        brand_name: brand of the product (e.g.: 'Bonduelle')
        product_name: name of the product (e.g.: 'red beans')
        product_size: number of the size of the product (e.g.: liquid product which is 100ml then: '100')
        product_unit: the unit name of the size of the product (e.g.: ml from 100ml)
        stock_expiring: expiring date in YYYY-MM-DD
        stock_amount: amount of the product (e.g.: in case of you have 5 bottle, then: '5')

    Returns:
        None.
    """
    connect = sqlite3.connect(filename)
    cursor = connect.cursor()

    cursor.execute("SELECT id FROM Product WHERE barcode = ?", (barcode,))
    product_id = cursor.fetchone()[0]

    sep_date = stock_expiring.split("-")
    cursor.execute(
        "SELECT amount FROM Stock WHERE product_id = ? AND expiring = ?",
        (product_id, datetime.date(int(int(sep_date[0])), int(sep_date[1]), int(sep_date[2]))),
    )
    prev_amount = cursor.fetchone()[0]
    amount = prev_amount - int(stock_amount)
    if amount == 0:
        cursor.execute(
            """DELETE FROM Stock WHERE product_id = ? AND expiring = ?""",
            (product_id, datetime.date(int(int(sep_date[0])), int(sep_date[1]), int(sep_date[2]))),
        )
    else:
        cursor.execute(
            """UPDATE Stock SET amount = ?
            WHERE product_id = ? AND expiring = ?""",
            (amount, product_id, datetime.date(int(int(sep_date[0])), int(sep_date[1]), int(sep_date[2]))),
    )
    connect.commit()


def read_barcodes(frame):
    barcode_text = ""
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        barcode_text = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
    return frame, barcode_text


def barcode_scanner():
    camera = cv2.VideoCapture(2)
    ret, frame = camera.read()

    def rescale_frame(frame, percent=30):
        scale_percent = 30
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

    while ret:
        ret, frame = camera.read()
        frame = rescale_frame(frame, percent=30)
        frame, result_text = read_barcodes(frame)
        cv2.imshow('Barcode reader', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        if result_text != "":
            break

    camera.release()
    cv2.destroyAllWindows()
    return result_text


def main(filename):
    """Starts list_expired_item() in case this was started as a script."""
    if os.path.isfile(filename) is not True:
        print("File does not exist exist. \nCreating new file.")
        create_database(filename)

    def menu():
        print("[1] Add new item")
        print("[2] Delete and item based on barcode")
        print("[3] List all items")
        print("[0] Exit")
    menu()
    try:
        option = int(input("Enter your option: "))
    except ValueError:
        print("Invalid option.")
        exit()
    while option != 0:
        if option == 1:
            barcode = barcode_scanner()
            print("Barcode was: ", barcode)
            item = check_item_existence(filename, barcode)
            if item is None:
                brand_name = input("Enter the name of the brand: ")
                product_name = input("Enter the product: ")
                product_size = input("Enter the size of the product: ")
                product_unit = input("Enter the unit of the size: ")
                stock_expiring = input("Enter expiring date: ")
                stock_amount = input("Enter the amount of the product: ")
                pass
            else:
                brand_name = item[0]
                product_name = item[1]
                product_size = item[2]
                product_unit = item[3]
                stock_expiring = input("Enter expiring date: ")
                stock_amount = input("Enter the amount of the product: ")
                pass
            add_new_item(filename, barcode, brand_name, product_name, product_size, product_unit, stock_expiring, stock_amount)
            pass
        elif option == 2:
            barcode = barcode_scanner()
            print("Barcode was: ", barcode)
            item = check_item_existence(filename, barcode)
            if item is None:
                print("Product is not available in the database.")
                pass
            else:
                stock_expiring = input("Enter expiring date: ")
                stock_amount = input("Enter the amount of the product: ")
                delete_item(filename, barcode, stock_expiring, stock_amount)
                pass
            pass
        elif option == 3:
            rows = list_database(filename)
            for row in rows:
                print(row)
            pass
        else:
            print("Invalid option.")

        menu()
        try:
            option = int(input("Enter your option: "))
        except ValueError:
            print("Invalid Option")


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        print("Usage: shelf_life_checker.py <filename>")
