#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('shelf_life.sqlite3')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Brand')
cur.execute('DROP TABLE IF EXISTS Product')
cur.execute('DROP TABLE IF EXISTS Stock')
cur.execute('''
CREATE TABLE Brand (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
    )
''')
cur.execute('''CREATE TABLE Product (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    unique_name TEXT UNIQUE,
    name TEXT,
    brand_id INTEGER,
    size INTEGER,
    unit TEXT
    )
''')
cur.execute('''CREATE TABLE Stock (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    product_id INTEGER,
    expiring TEXT,
    amount INTEGER
    )
''')


f = open('prepping_-_sheet1.csv')
for row in f:
    fields = row.split(",")
    a = ""
    b = ""
    s = fields[2]
    for char in s:
        if not char.isalpha():
            a = a + char
        else:
            b = b + char
    fields = (fields[0], fields[1], a, b, fields[3], fields[4].strip('\n'))

    # fields[0]: Product.name, fields[1]: Brand.name, fields[2]: Product.size, fields[3]: Product.unit, fields[4]: Stock.expiring, fields[5]: Stock.amount
    # print(fields)
    cur.execute('INSERT OR IGNORE INTO Brand ( name ) VALUES ( ? )', ( fields[1], ))
    cur.execute('SELECT id FROM Brand WHERE name = ? ', ( fields[1], ))
    brand_id = cur.fetchone()[0]

    # unique_name is a placeholder for barcode
    # it identifies the product and makes it unique
    unique_name = fields[1] + fields[0] + fields[2] + fields[3]
    cur.execute('INSERT OR IGNORE INTO Product ( unique_name, name, brand_id, size, unit ) VALUES ( ?, ?, ?, ?, ? )', ( unique_name, fields[0], brand_id, fields[2], fields[3] ))
    cur.execute('SELECT id FROM Product WHERE unique_name = ? ', ( unique_name, ))
    product_id = cur.fetchone()[0]

    cur.execute('SELECT amount FROM Stock WHERE product_id = ? AND expiring = ?', ( product_id, fields[4] ))
    if cur.fetchone() == None:
        cur.execute('INSERT INTO Stock ( product_id, expiring, amount ) VALUES ( ?, ?, ? )', ( product_id, fields[4], fields[5] ))
        print("Created first: ", unique_name)
    else:
        cur.execute('SELECT amount FROM Stock WHERE product_id = ? AND expiring = ?', ( product_id, fields[4] ))
        prev_amount = cur.fetchone()[0]
        amount = int(fields[5]) + prev_amount
        cur.execute('UPDATE Stock SET amount = ? WHERE product_id = ? AND expiring = ?', ( amount, product_id, fields[4] ))
        print("Updated: ", unique_name)
    conn.commit()
#    try:
#        True
#    except sqlite3.IntegrityError:
#        print(fields)
#        cur.execute('SELECT amount FROM Product WHERE unique_name = ?', ( unique_name, ))
#        prev_amount = cur.fetchone()[0]
#        amount = int(fields[5]) + prev_amount
#        print(amount)
#        cur.execute('UPDATE Product SET amount = ? WHERE unique_name = ?', ( amount, unique_name ))

    #print(fields)
#conn.commit()

sqlstr = '''SELECT product_name, amount FROM Product WHERE product_name = "Vorosbab"'''

#for row in cur.execute(sqlstr):
    #print(row)

cur.close()
