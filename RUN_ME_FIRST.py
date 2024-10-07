import pymysql
root_username = "root"  # Change this if your root username is different
root_passwd = "root_database_password"  # Change this to your actual root password
# New user details
username = "any_username_of_your_choice"
passwd = "any_password_of_your_choice"  # Password for the new user

# Connect to MySQL as root (or a user with privileges to create users)
mydbl = pymysql.connect(host="localhost", user=root_username, password=root_passwd)
cur = mydbl.cursor()
# Create the new user if it doesn't exist
try:
    cur.execute("CREATE USER IF NOT EXISTS %s@'localhost' IDENTIFIED BY %s",(username, passwd))
    print("User %s created or already exists.",(username))
    
    # Grant specific privileges to the new user
    cur.execute("GRANT SELECT, INSERT, UPDATE, CREATE ON scriveners.* TO %s@'localhost'",(username))
    
    print("Granted SELECT, INSERT, CREATE, and UPDATE privileges to %s on 'scoretable'.",(username))

except Exception as e:
    print("Error creating user or granting privileges: %s",(e))
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
    print("Error creating database: %s",(e))
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
    print("Error creating table: %s",(e))
finally:
    cur.close()
    mydbl.close()
print("Setup complete.")
