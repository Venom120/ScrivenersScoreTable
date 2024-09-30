from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
username = "username"
passwd = "password@123"
app = Flask(__name__)

# function to init connection
def connec():
	return pymysql.connect(host="localhost", user=username, password=passwd, database="scriveners")

# Function to fetch scores from the database
def fetch_scores():
	try:
		mydbl = connec()
		cur = mydbl.cursor()
		cur.execute("SELECT name, points FROM scoretable")
		scores = cur.fetchall()
		cur.close()
		mydbl.close()
		return scores
	except Exception as e:
		print(f"Error fetching scores: {e}")  # Log the error
		return None  # Return None or handle it appropriately

# Function to update points in the database
def update_points(name, points_to_add):
	try:
		mydbl = connec()
		cur = mydbl.cursor()
		cur.execute("UPDATE scoretable SET points = points + %s WHERE name = %s", (points_to_add, name))
		mydbl.commit()
		cur.close()
		mydbl.close()
	except Exception as e:
		print(f"Error updating points: {e}")  # Log the error
		return False
	return True

@app.route('/')
def index():
	score_data = fetch_scores()
	if score_data is None:
		return render_template('error.html')  # Render error page if fetching fails
	return render_template('index.html', score_data=score_data)

@app.route('/add_points', methods=['POST'])
def add_points():
	name = request.form['name']
	points_to_add = int(request.form['points'])
	password = request.form.get('password', '')

	if password == "password":
		if update_points(name, points_to_add):
			return redirect(url_for('index'))
		else:
			return render_template('error.html')  # Render error page if update fails
	else:
		flash('Invalid password! Please try again.')
		return redirect(url_for('index'))

@app.route('/add_name', methods=['POST'])
def add_name():
	name = request.form['name']
	password = request.form.get('password', '')

	if password == "password":
		try:
			mydbl = connec()
			cur = mydbl.cursor()
			cur.execute("INSERT INTO scoretable (name, points) VALUES (%s, 0)", (name,))
			mydbl.commit()
			cur.close()
			mydbl.close()
			return redirect(url_for('index'))
		except Exception as e:
			print(f"Error adding name: {e}")  # Log the error
			return render_template('error.html')  # Render error page if adding fails
	else:
		flash('Invalid password! Please try again.')
		return redirect(url_for('index'))

if __name__ == "__main__":
	app.run(debug=True)
