import pymysql
from flask import Flask, render_template, request, redirect, url_for, flash, session
app = Flask(__name__)
app.secret_key = "your_secret_key" # can be any but unique
# Database credentials
DB_USERNAME = "" # use the same as you used in RUN_ME_FIRST.py
DB_PASSWORD = "" # use the same as you used in RUN_ME_FIRST.py
DB_HOST = "localhost"
DB_NAME = "scriveners"

# ignore this func its just for debug
def log(txt):
    with open("/scoretable/error.txt", "a") as file:
        file.write(f"{txt}\n")

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Fetch scores from the database
def fetch_scores():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, points FROM scoretable ORDER BY points DESC")
            scores = cursor.fetchall()
        connection.close()
        return scores
    except Exception as e:
        print(f"Error fetching scores: {e}")
        return None
# Update points in the database
def update_points(name, points_to_add):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Check current points
            cursor.execute("SELECT points FROM scoretable WHERE name = %s", (name,))
            result = cursor.fetchone()
            if not result:
                return False  # Name not found
            current_points = result['points']
            if current_points == 0 and points_to_add == -5:
                return True  # Prevent negative points beyond zero
            # Update points
            cursor.execute(
                "UPDATE scoretable SET points = points + %s WHERE name = %s",
                (points_to_add, name)
            )
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error updating points: {e}")
        return False

# Add a new name to the database
def add_name_to_db(name):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO scoretable (name, points) VALUES (%s, 0)", (name,))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error adding name: {e}")
        return False

# Home route
@app.route('/')
def index():
    scores = fetch_scores()
    if scores is None:
        return render_template('error.html')  # Create an error.html template
    return render_template('index.html', score_data=scores, admin_authenticated=session.get('admin_authenticated', False))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == "admin_passwd":
            session['admin_authenticated'] = True
            # flash('Logged in successfully.')
            return redirect(url_for('index'))
        else:
            flash('Invalid password! Please try again.')
            return redirect(url_for('index'))
    return redirect(url_for('index'))

# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('admin_authenticated', None)
    # flash('Logged out successfully.')
    return redirect(url_for('index'))

# Route to add points
@app.route('/add_points', methods=['POST'])
def add_points_route():
    if not session.get('admin_authenticated'):
        flash('You need to log in to perform this action.')
        return redirect(url_for('index'))

    name = request.form.get('name')
    points_to_add = request.form.get('points')

    try:
        points_to_add = int(points_to_add)
    except ValueError:
        flash('Invalid points value.')
        return redirect(url_for('index'))

    if update_points(name, points_to_add):
        flash('Points updated successfully.')
    else:
        flash('Failed to update points.')
    return redirect(url_for('index'))

# Route to add a new name
@app.route('/add_name', methods=['POST'])
def add_name_route():
    password = request.form.get('password', '')
    name = request.form.get('name', '').strip()

    if password != "admin_passwd":
        flash('Invalid password! Please try again.')
        return redirect(url_for('index'))

    if not name:
        flash('Name cannot be empty.')
        return redirect(url_for('index'))

    if add_name_to_db(name):
        flash('Name added successfully.')
    else:
        flash('Failed to add name.')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
