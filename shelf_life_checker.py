#!/usr/bin/env python3
"""This script has modules to query the databes
Please notice that this is just a placeholder yet, not fully operational."""

import sys
import sqlite3


def list_database(filename):
    """Lists the whole database into STD Output

    Arg:
        file: sqlite database

    Returns:
        Prints out the whole database
    """
    connect = sqlite3.connect(filename)
    cursor = connect.cursor()
    cursor.execute(
        """SELECT Brand.name, Product.name, Stock.expiring
        FROM Stock JOIN Product JOIN Brand ON
        Stock.product_id = Product.id AND
        Product.brand_id = Brand.id"""
    )
    rows = cursor.fetchall()
    for row in rows:
        print(row)
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
        """SELECT Brand.name, Product.name, Stock.expiring
        FROM Stock JOIN Product JOIN Brand ON
        Stock.product_id = Product.id AND
        Product.brand_id = Brand.id
        WHERE date(Stock.expiring) < date('now')"""
    )
    #WHERE date(Stock.expiring) < date('now')""")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
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
        """SELECT Brand.name, Product.name, Stock.expiring
        FROM Stock JOIN Product JOIN Brand ON
        Stock.product_id = Product.id AND
        Product.brand_id = Brand.id
        WHERE date(Stock.expiring) BETWEEN date('now') AND date('now', '+1 month')"""
    )
    #WHERE date(Stock.expiring) < date('now')""")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return rows

def main(filename):
    """Starts list_expired_item() in case this was started as a script."""
    list_expires_soon(filename)


if __name__ == "__main__":
    main(sys.argv[1])
