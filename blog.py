from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages, g
import sqlite3
from functools import wraps 

app = Flask(__name__)

#configuration - use CAPITAL LETTERS
DATABASE = "blog.db" 
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = b'9w\x84\xcf\xd1\xdeg\x9d\xf9\x02\x8d\xaa\xc7g^\x0e\xf1Y\x12\xad\x05\xa6\x94\x94'

app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config["DATABASE"])

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to log in first.')
			return redirect(url_for('login'))
	return wrap


@app.route("/", methods=['GET', 'POST'])
def login():
	print(request.method)
	error = None 
	status_code = 200
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Credentials. Please try again.'
			status_code = 401
		else:
			session['logged_in'] = True 
			return redirect(url_for('main'))
	if error:
		print(error) 
	else: 
		print("error is none")
	return render_template("login.html", error=error), status_code


@app.route("/main")
@login_required
def main():
	g.db = connect_db()
	c = g.db.cursor() 
	c.execute("SELECT * FROM posts ") 
	posts = [dict(title=row[0], post=row[1]) for row in c.fetchall()]
	g.db.close()
	return render_template("main.html", posts=posts)


@app.route("/logout")
def logout():
	session.pop('logged_in', None) #this is not the list pop() function but rather it's a function defined within the session class
	flash('You were logged out')
	print(get_flashed_messages())
	#return redirect(url_for('login'))
	return render_template("login.html", error=None), 200

@app.route("/add", methods=['POST'])
@login_required
def add_post():
	title = request.form['title']
	post = request.form['post']
	if not title or not post:
		flash('All fields are required. Please try again')
		return redirect(url_for('main'))
	g.db = connect_db()
	c = g.db.cursor() 
	c.execute("INSERT INTO posts VALUES(?,?)", (title, post))
	g.db.commit()
	flash('New entry was successfully posted!')
	g.db.close()
	return redirect(url_for('main'))

if __name__ == '__main__':
	app.run(debug=True)
