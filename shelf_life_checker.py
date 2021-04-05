#!/usr/bin/env python3
import sys
import sqlite3

# SQL Examples:
# Table: Users(name, mail)
# INSERT INTO Users (name, email) VALUES ('Kristin', 'kf@umich.edu')
# DELETE FROM Users WHERE email='ted@umich.edu'
# UPDATE Users SET name="Charles" WHERE email='csev@umich.edu'
# SELECT * FROM Users
# SELECT * FROM Users WHERE email='csev@umich.edu'
# SELECT * FROM Users ORDER BY email
# One to Many relation
# CREATE TABLE 'Artist' ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 'name' TEXT)
# CREATE TABLE 'Genre' ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 'name' TEXT)
# CREATE TABLE Album (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, artist_id INTEGER, title TEXT)
# CREATE TABLE Track (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, title TEXT, album_id INTEGER, genre_id INTEGER, len INTEGER, rating INTEGER, count INTEGER)
# select Album.title, Artist.name from Album join Artist on Album.artist_id = Artist.id
# select Album.title, Artist.artist_id, Artist.id, Artist.name from Album join Artist on Album.artist.id = Artist.id
# select Track.title, Genre.name from Track join Genre on Track.genre_id = Genre.id
# select Track.title, Artist.name, Album.title, Genre.name from Track join Genre join Album join Artist on Track.genre_id = Genre.id and Track.album_id = Album.id and Album.artist_id = Artist.id
# Many to many relation
# SELECT User.name, Member.role, Course.title FROM User JOIN Member JOIN Course on Member.user_id = User.id AND Member.course_id = Course.id ORDER BY Course.title, member.role DESC, User.name
# INSERT OR REPLACE/IGNORE: It is possible to give this command. If the item exists and it is a UNIQUE item, then it ignors it.

def list_database(filename):
    """Lists the whole database into STD Output

    Arg:
        file: sqlite database

    Returns:
        Prints out the whole database
    """
    connect = sqlite3.connect(filename)
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM FoodStorage')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def main(filename):
    list_database(filename)



if __name__ == '__main__':
    main(sys.argv[1])
