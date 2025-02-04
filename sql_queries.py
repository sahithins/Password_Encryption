import sqlite3
from password_encryption import *
import os

key = generate_key(master_password, salt)

def init_DB():
    try:
        sqliteConnection = sqlite3.connect("nadimpalliDB")
        cursor = sqliteConnection.cursor()
        print('DB initialised')
        
        # Write a query and execute it with cursor
        query = 'select sqlite_version();'
        cursor.execute(query)
        
        # Fetch and output result
        result = cursor.fetchall()
        print('SQLite Version is {}'.format(result))

        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        );
        '''

        # Execute the SQL command to create the table
        cursor.execute(create_table_query)

        create_table_query = '''
        CREATE TABLE IF NOT EXISTS password_manager (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            website TEXT NOT NULL,
            website_username TEXT NOT NULL,
            website_password TEXT NOT NULL,
            UNIQUE(username, website, website_username)
        );
        '''

        # Execute the CREATE TABLE command
        cursor.execute(create_table_query)
                
        # Close the cursor
        cursor.close()
    
    # Handle errors
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    
    # Close DB Connection irrespective of success
    # or failure
    finally:
    
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')

def register_user(username, password, key):
    conn = sqlite3.connect('nadimpalliDB')
    cursor = conn.cursor()

    encrypted_password = encrypt_data(password, key)

    print(encrypted_password)

    # Define the INSERT SQL command
    insert_query = '''
    INSERT INTO users (username, password)
    VALUES (?, ?);
    '''

    # Execute the INSERT command with username and password as parameters
    cursor.execute(insert_query, (username, encrypted_password))

    # Commit the transaction
    conn.commit()

    print(f"User {username} added to db successfully!")
    # Close the connection
    conn.close()

def verify_user(username, password, key):
    conn = sqlite3.connect('nadimpalliDB')
    cursor = conn.cursor()

    # Define the SELECT SQL command
    select_query = '''
    SELECT * FROM users WHERE username = ?;
    '''

    # Execute the SELECT command with username as a parameter
    cursor.execute(select_query, (username,))

    # Fetch one row, if it exists
    row = cursor.fetchone()

    # Close the connection
    conn.close()

    # Check if a row was found
    if row:
        if decrypt_data(row[1], key)==password:
            return 1
        return 0
    else:
        return -1

def show_users():
    conn = sqlite3.connect('nadimpalliDB')
    cursor = conn.cursor()

    # Define the INSERT SQL command
    insert_query = '''
    SELECT * from users;
    '''

    # Execute the INSERT command with username and password as parameters
    cursor.execute(insert_query)

    row = cursor.fetchall()

    print(row)

    # Commit the transaction
    conn.commit()
    conn.close()

def add_website_creds(username, website_name, website_username, website_password, key):
    conn = sqlite3.connect('nadimpalliDB')
    cursor = conn.cursor()

    encrypted_password = encrypt_data(website_password, key)

    print(encrypted_password)

    # Define the INSERT SQL command
    insert_query = '''
    INSERT INTO password_manager (username, website, website_username, website_password)
    VALUES (?, ?, ?, ?);
    '''

    try:
        # Execute the INSERT command with username and password as parameters
        cursor.execute(insert_query, (username, website_name, website_username, encrypted_password))

        # Commit the transaction
        conn.commit()

        conn.close()

        print(f"User {username} added {website_name} credentials to db successfully!")
        # Close the connection
        return 1
    except:
        conn.close()
        return -1
    

def show_user_website_creds(username):
    conn = sqlite3.connect('nadimpalliDB')
    cursor = conn.cursor()

    # Define the INSERT SQL command
    insert_query = '''
    SELECT * from password_manager
    where username=?;
    '''

    # Execute the INSERT command with username and password as parameters
    cursor.execute(insert_query, (username, ))

    row = cursor.fetchall()

    print(row)

    # Commit the transaction
    conn.commit()
    conn.close()

    return row

def show_all_website_creds():
    conn = sqlite3.connect('nadimpalliDB')
    cursor = conn.cursor()

    # Define the INSERT SQL command
    insert_query = '''
    SELECT * from password_manager;
    '''

    # Execute the INSERT command with username and password as parameters
    cursor.execute(insert_query)

    row = cursor.fetchall()

    print(row)

    # Commit the transaction
    conn.commit()
    conn.close()

    return row
# def verify_website_creds(username, website_name, website_username, website_password, key):
#     conn = sqlite3.connect('nadimpalliDB')
#     cursor = conn.cursor()

#     encrypted_password = encrypt_data(website_password, key)

#     print(encrypted_password)

#     # Define the SELECT SQL command
#     select_query = '''
#     SELECT * FROM password_manager WHERE username = ? and website = ?;
#     '''

#     # Execute the SELECT command with username as a parameter
#     cursor.execute(select_query, (username, website_name))

#     # Fetch one row, if it exists
#     row = cursor.fetchone()

#     # Close the connection
#     conn.close()

#     # Check if a row was found
#     if row:
#         if decrypt_data(row[1], key)==password:
#             return 1
#         return 0
#     else:
#         return -1

if __name__ == "__main__":
    # show_users()
    # init_DB()
    # key = generate_key(master_password, salt)
    # print(key)
    # register_user("user786",b"pass123", key)
    print(f"{key=}")
    pas = "random"
    
    # print(verify_user("user786", pas.encode('utf-8'),key))
    # print(add_website_creds("user786", "google", "user786@googl", b"google@123", key))
    show_user_website_creds("user786")
    
