import sqlite3

# Define the test data to be inserted
test_data = [
    (1, 101, 201, 301, "Some application data 1", "pending"),
    (2, 102, 202, 302, "Some application data 2", "approved"),
    (3, 103, 203, 303, "Some application data 3", "rejected"),
]

# Function to insert test data into the LoanApplications table
def insert_test_data():
    try:
        # Connect to the database or create one if it doesn't exist
        conn = sqlite3.connect("digi_loans.db")
        cursor = conn.cursor()

        # Create the LoanApplications table if it doesn't exist
        cursor.execute("""
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
        """)

        # Insert test data into the table
        cursor.executemany("""
            INSERT INTO LoanApplications (application_id, user_id, product_id, form_id, application_data, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, test_data)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        print("Test data inserted successfully.")

    except sqlite3.Error as e:
        print("Error occurred:", e)

if __name__ == "__main__":
    insert_test_data()
