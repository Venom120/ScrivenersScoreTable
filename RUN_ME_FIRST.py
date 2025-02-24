import pymysql
host = "" # Change this to your host
root_username = ""  # Change this if your root username is different
root_passwd = ""  # Change this to your actual root password

# New user details
username = "" # Username for the new user
passwd = ""  # Password for the new user

# Connect to MySQL as root (or a user with privileges to create users)
mydbl = pymysql.connect(host=host, user=root_username, password=root_passwd)
cur = mydbl.cursor()
# Create the new user if it doesn't exist
try:
    cur.execute("CREATE USER IF NOT EXISTS %s@'%' IDENTIFIED BY %s",(username, passwd))
    print("User %s created or already exists.",(username))
    # Grant specific privileges to the new user
    cur.execute("GRANT SELECT, INSERT, UPDATE, CREATE ON scriveners.* TO %s@'%'",(username))
    print("Granted SELECT, INSERT, CREATE, and UPDATE privileges to %s on 'poem'.",(username))

except Exception as e:
    print("Error creating user or granting privileges: %s",(e))
finally:
    cur.close()
    mydbl.close()

# Connect to MySQL as the new user to create the database
mydbl = pymysql.connect(host=host, user=username, password=passwd)
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
    
# Connect to MySQL as the new user to create the tables
mydbl = pymysql.connect(host=host, user=username, password=passwd, database="scriveners")
cur = mydbl.cursor()
# Create the table
try:
    cur.execute("CREATE TABLE IF NOT EXISTS poem (name VARCHAR(50), points INT DEFAULT 0)")
    mydbl.commit()
    print("Table 'poem' created or already exists.")
    cur.execute("CREATE TABLE IF NOT EXISTS music (name VARCHAR(50), points INT DEFAULT 0)")
    mydbl.commit()
    print("Table 'music' created or already exists.")
except Exception as e:
    print("Error creating tables: %s",(e))
finally:
    cur.close()
    mydbl.close()
print("Setup complete.")
