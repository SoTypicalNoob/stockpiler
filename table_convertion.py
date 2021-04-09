#!/usr/bin/env python3
"""This scirpt converts csv to SQLite database format."""

import sqlite3
import datetime

conn = sqlite3.connect("shelf_life.sqlite3")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Brand")
cur.execute("DROP TABLE IF EXISTS Product")
cur.execute("DROP TABLE IF EXISTS Stock")
cur.execute(
    """CREATE TABLE Brand (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
    )
"""
)
cur.execute(
    """CREATE TABLE Product (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    unique_name TEXT UNIQUE,
    name TEXT,
    brand_id INTEGER,
    size INTEGER,
    unit TEXT
    )
"""
)
cur.execute(
    """CREATE TABLE Stock (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    product_id INTEGER,
    expiring DATE,
    amount INTEGER
    )
"""
)


f = open("prepping_-_sheet1.csv")
for row in f:
    fields = row.split(",")
    size_string = ""
    unit_string = ""
    for char in fields[2]:
        if not char.isalpha():
            size_string = size_string + char
        else:
            unit_string = unit_string + char
    fields = (
        fields[0],
        fields[1],
        size_string,
        unit_string,
        fields[3],
        fields[4].strip("\n"),
    )

    # fields[0]: Product.name, fields[1]: Brand.name, fields[2]: Product.size,
    # fields[3]: Product.unit, fields[4]: Stock.expiring,
    # import datetime
    # fields[5]: Stock.amount
    cur.execute("INSERT OR IGNORE INTO Brand (name) VALUES (?)", (fields[1],))
    cur.execute("SELECT id FROM Brand WHERE name = ?", (fields[1],))
    brand_id = cur.fetchone()[0]

    # unique_name is a placeholder for barcode
    # it identifies the product and makes it ..., well, unique
    unique_name = fields[1] + fields[0] + fields[2] + fields[3]
    cur.execute(
        """INSERT OR IGNORE INTO Product
        (unique_name, name, brand_id, size, unit)
        VALUES (?, ?, ?, ?, ?)""",
        (unique_name, fields[0], brand_id, fields[2], fields[3]),
    )
    cur.execute("SELECT id FROM Product WHERE unique_name = ?", (unique_name,))
    product_id = cur.fetchone()[0]


    sep_date = fields[4].split("-")
    cur.execute(
        "SELECT amount FROM Stock WHERE product_id = ? AND expiring = ?",
        (product_id, datetime.date(int(sep_date[0]), int(sep_date[1]), int(sep_date[2]))),
    )
    if cur.fetchone() is None:
        cur.execute(
            """INSERT INTO Stock (product_id, expiring, amount)
            VALUES (?, ?, ?)""",
            (product_id, datetime.date(int(int(sep_date[0])), int(sep_date[1]), int(sep_date[2])), fields[5]),
        )
    else:
        cur.execute(
            "SELECT amount FROM Stock WHERE product_id = ? AND expiring = ?",
            (product_id, datetime.date(int(int(sep_date[0])), int(sep_date[1]), int(sep_date[2]))),
        )
        prev_amount = cur.fetchone()[0]
        amount = int(fields[5]) + prev_amount
        cur.execute(
            """UPDATE Stock SET amount = ?
            WHERE product_id = ? AND expiring = ?""",
            (amount, product_id, datetime.date(int(int(sep_date[0])), int(sep_date[1]), int(sep_date[2]))),
        )
    conn.commit()

cur.close()
