import pymysql
root_username = "root"  # Change this if your root username is different
root_passwd = "root123"  # Change this to your actual root password
# New user details
username = "username"
passwd = "password@123"  # Password for the new user

# Connect to MySQL as root (or a user with privileges to create users)
mydbl = pymysql.connect(host="localhost", user=root_username, password=root_passwd)
cur = mydbl.cursor()
# Create the new user if it doesn't exist
try:
    cur.execute(f"CREATE USER IF NOT EXISTS '{username}'@'localhost' IDENTIFIED BY '{passwd}'")
    print(f"User '{username}' created or already exists.")
    
    # Grant specific privileges to the new user
    cur.execute(f"GRANT SELECT, INSERT, UPDATE, CREATE ON scriveners.* TO '{username}'@'localhost'")
    cur.execute(f"FLUSH PRIVILEGES")
    
    print(f"Granted SELECT, INSERT, CREATE, and UPDATE privileges to '{username}' on 'scoretable'.")

except Exception as e:
    print(f"Error creating user or granting privileges: {e}")
finally:
    cur.close()
    mydbl.close()

# Connect to MySQL as the new user to create the database
mydbl = pymysql.connect(host="localhost", user=username, password=passwd)
cur = mydbl.cursor()
# Create the database
try:
    cur.execute("CREATE DATABASE IF NOT EXISTS scriveners")
    mydbl.commit()
    print("Database 'scriveners' created or already exists.")
except Exception as e:
    print(f"Error creating database: {e}")
finally:
    cur.close()
    mydbl.close()
    
# Connect to MySQL as the new user to create the table
mydbl = pymysql.connect(host="localhost", user=username, password=passwd, database="scriveners")
cur = mydbl.cursor()
# Create the table
try:
    cur.execute("CREATE TABLE IF NOT EXISTS scoretable (name VARCHAR(50), points INT DEFAULT 0)")
    mydbl.commit()
    print("Table 'scoretable' created or already exists.")
except Exception as e:
    print(f"Error creating table: {e}")
finally:
    cur.close()
    mydbl.close()
print("Setup complete.")
