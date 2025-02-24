import pymysql, os
from flask import Flask, render_template, request, redirect, url_for, flash, session
app = Flask(__name__)
app.secret_key = "your_secret_key" # can be any but unique

# Database credentials
DB_USERNAME = "" # use the same as you used in RUN_ME_FIRST.py
USER_PASSWORD = "" # use the same as you used in RUN_ME_FIRST.py
DB_HOST = "localhost" # use the same as you used in RUN_ME_FIRST.py
DB_NAME = "" # use the same as you used in RUN_ME_FIRST.py
admin_pass = "admin_passwd" # admin password for login inside the website

# ------------# If deploying on a deployment service------------
DB_USERNAME = os.environ['DB_USERNAME']
USER_PASSWORD = os.environ['USER_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
admin_pass = os.environ['ADMIN_PASS']


# ignore this func its just for debug
def log(txt):
    with open("error.txt", "a") as file:
        file.write(f"{txt}\n")

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=USER_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
# Home route
@app.route('/<page_name>')
def index(page_name):
    if page_name == "poem":
        scores = fetch_scores_poem()
        
    elif page_name == "music":
        scores = fetch_scores_music()
    else:
        flash("Invalid page requested.")
        return redirect(url_for('index', page_name='poem'))

    if scores is None:
        return render_template('error.html')

    return render_template('index.html', score_data=scores, page_name=page_name, admin_authenticated=session.get('admin_authenticated', False))

# Shared Login Route
@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password', '')
    page_name = request.form.get('page_name', 'poem')  # Default to poem

    if password == admin_pass:
        session['admin_authenticated'] = True
        flash('Logged in successfully.')
    else:
        flash('Invalid password! Please try again.')

    return redirect(url_for('index', page_name=page_name))

# Shared Logout Route
@app.route('/logout', methods=['POST'])
def logout():
    page_name = request.form.get('page_name', 'poem')  # Default to poem
    session.pop('admin_authenticated', None)
    flash('Logged out successfully.')
    return redirect(url_for('index', page_name=page_name))




""" Poem """
# Fetch scores from the table poem
def fetch_scores_poem():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, points FROM poem ORDER BY points DESC")
            scores = cursor.fetchall()
        connection.close()
        return scores
    except Exception as e:
        print(f"Error fetching scores: {e}")
        return None
# Update points in the table poem
def update_points_poem(name, points_to_add):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Check current points
            cursor.execute("SELECT points FROM poem WHERE name = %s", (name,))
            result = cursor.fetchone()
            if not result:
                return False  # Name not found
            current_points = result['points']
            if current_points == 0 and points_to_add == -5:
                return True  # Prevent negative points beyond zero
            # Update points
            cursor.execute(
                "UPDATE poem SET points = points + %s WHERE name = %s",
                (points_to_add, name)
            )
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error updating points: {e}")
        return False

# Add a new name to the table poem
def add_name_to_db_poem(name):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO poem (name, points) VALUES (%s, 0)", (name,))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error adding name: {e}")
        return False

# Route to add points in poem
@app.route('/add_points_poem', methods=['POST'])
def add_points_route_poem():
    if not session.get('admin_authenticated'):
        flash('You need to log in to perform this action.')
        return redirect(url_for('index', page_name="poem"))

    name = request.form.get('name')
    points_to_add = request.form.get('points')

    try:
        points_to_add = int(points_to_add)
    except ValueError:
        flash('Invalid points value.')
        return redirect(url_for('index', page_name="poem"))

    if update_points_poem(name, points_to_add):
        flash('Points updated successfully.')
    else:
        flash('Failed to update points.')
    return redirect(url_for('index', page_name="poem"))

# Route to add a new name in poem
@app.route('/add_name_poem', methods=['POST'])
def add_name_route_poem():
    name = request.form.get('name', '').strip()

    if not name:
        flash('Name cannot be empty.')
        return redirect(url_for('index', page_name="poem"))

    if add_name_to_db_poem(name):
        flash('Name added successfully.')
    else:
        flash('Failed to add name.')
    return redirect(url_for('index', page_name="poem"))













""" Music """
# Fetch scores from the table music
def fetch_scores_music():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, points FROM music ORDER BY points DESC")
            scores = cursor.fetchall()
        connection.close()
        return scores
    except Exception as e:
        print(f"Error fetching scores: {e}")
        return None
# Update points in the table music
def update_points_music(name, points_to_add):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Check current points
            cursor.execute("SELECT points FROM music WHERE name = %s", (name,))
            result = cursor.fetchone()
            if not result:
                return False  # Name not found
            current_points = result['points']
            if current_points == 0 and points_to_add == -5:
                return True  # Prevent negative points beyond zero
            # Update points
            cursor.execute(
                "UPDATE music SET points = points + %s WHERE name = %s",
                (points_to_add, name)
            )
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error updating points: {e}")
        return False

# Add a new name to the table music
def add_name_to_db_music(name):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO music (name, points) VALUES (%s, 0)", (name,))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error adding name: {e}")
        return False

# Route to add points in music
@app.route('/add_points_music', methods=['POST'])
def add_points_route_music():
    if not session.get('admin_authenticated'):
        flash('You need to log in to perform this action.')
        return redirect(url_for('index', page_name="music"))

    name = request.form.get('name')
    points_to_add = request.form.get('points')

    try:
        points_to_add = int(points_to_add)
    except ValueError:
        flash('Invalid points value.')
        return redirect(url_for('index', page_name="music"))

    if update_points_music(name, points_to_add):
        flash('Points updated successfully.')
    else:
        flash('Failed to update points.')
    return redirect(url_for('index', page_name="music"))

# Route to add a new name in music
@app.route('/add_name_music', methods=['POST'])
def add_name_route_music():
    name = request.form.get('name', '').strip()

    if not name:
        flash('Name cannot be empty.')
        return redirect(url_for('index', page_name="music"))

    if add_name_to_db_music(name):
        flash('Name added successfully.')
    else:
        flash('Failed to add name.')
    return redirect(url_for('index', page_name="music"))


if __name__ == "__main__":
    app.run(debug=True)
