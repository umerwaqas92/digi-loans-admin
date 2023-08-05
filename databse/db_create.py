import sqlite3

def create_tables():
    # Connect to or create the SQLite database file
    conn = sqlite3.connect('databse/digi_loans.db')
    cursor = conn.cursor()

    try:
      
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                role_id INTEGER,
                full_name TEXT,
                date_of_birth TEXT,
                address TEXT,
                phone_number TEXT,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create the Roles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Roles (
                role_id INTEGER PRIMARY KEY,
                role_name TEXT NOT NULL,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Insert roles data (admin, user, zone) into the Roles table
        cursor.executemany('INSERT INTO Roles (role_name) VALUES (?)', [('admin',), ('user',), ('zone',)])

        # Create the Zones table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Zones (
                zone_id INTEGER PRIMARY KEY,
                zone_name TEXT NOT NULL,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Insert zones data (North zone, East zone, Swat zone, West zone) into the Zones table
        cursor.executemany('INSERT INTO Zones (zone_name) VALUES (?)', [('North zone',), ('East zone',), ('Swat zone',), ('West zone',)])

        # Create the LoanProducts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS LoanProducts (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                product_image TEXT,
                zone_id INTEGER,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (zone_id) REFERENCES Zones (zone_id)
            )
        ''')

        # Create the ProductForms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ProductForms (
                form_id INTEGER PRIMARY KEY,
                product_id INTEGER,
                form_title TEXT,
                form_fields TEXT,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES LoanProducts (product_id)
            )
        ''')

        # Create the LoanApplications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS LoanApplications (
                application_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                form_id INTEGER,
                application_data TEXT,
                status TEXT,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users (user_id),
                FOREIGN KEY (product_id) REFERENCES LoanProducts (product_id),
                FOREIGN KEY (form_id) REFERENCES ProductForms (form_id)
            )
        ''')

        # Create the ProductCategory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ProductCategory (
                category_id INTEGER PRIMARY KEY,
                category_name TEXT NOT NULL,
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')


        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        print("Database, tables, roles, and zones inserted successfully.")

    except sqlite3.Error as e:
        print("Error creating database, tables, roles, and zones:", e)

