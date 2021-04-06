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


def main(filename):
    """Starts list_database() in case this was started as a script."""
    list_database(filename)


if __name__ == "__main__":
    main(sys.argv[1])
