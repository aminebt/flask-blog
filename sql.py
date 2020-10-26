# sql.py - Create a SQLite3 table and populate it with data 

import sqlite3 


first_posts = [
	("Good", "I\'m Good"),
	("Okay", "I\'m Okay"),
	("Well", "I\'m Well"),
	("Good", "I\'m Excellent")
]

with sqlite3.connect("blog.db") as conn:

	c = conn.cursor()
	try:
		c.execute("CREATE TABLE posts(title TEXT, post TEXT)")
		c.executemany("INSERT INTO posts VALUES(?,?)", first_posts)

	except sqlite3.OperationalError as oe:
		print("The following error occured: {}".format(oe))