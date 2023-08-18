import sqlite3
from sqlite3 import Error
from databse.db_service import connect_db
import datetime



# Create operation for Expenses
def create_expense(user_id, title, amount, category, createdAt):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Expenses (user_id, title, amount, category, createdAt)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, title, amount, category, createdAt))


        connection.commit()
        print("Expense created successfully")
    except Error as e:
        print("Error create_expense",e)
    finally:
        if connection:
            connection.close()

# Read operation for Expenses
def get_expense_by_id(expense_id):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM Expenses WHERE id = ?
        """, (expense_id,))

        expense = cursor.fetchone()
        if expense:
            print(expense)
        else:
            print("Expense not found")
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

# Update operation for Expenses
def update_expense(expense_id, title, amount, category,expanes_date):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE Expenses SET title = ?, amount = ?, category = ?, createdAt = ?
            WHERE id = ?
        """, (title, amount, category, expanes_date, expense_id))

        connection.commit()
        print("Expense updated successfully")
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

# Delete operation for Expenses
def delete_expense(expense_id):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM Expenses WHERE id = ?
        """, (expense_id,))

        connection.commit()
        print("Expense deleted successfully")
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

# Get all operation for Expenses
def get_all_expenses():
    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM Expenses ORDER BY createdAt DESC
        """)

        expenses = cursor.fetchall()
        return expenses

    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

# Create operation for ExpensesCategory
def create_category(name):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO ExpensesCategory (name)
            VALUES (?)
        """, (name,))

        connection.commit()
        print("Category created successfully")
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

# Read operation for ExpensesCategory
def get_category_by_id(category_id):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM ExpensesCategory WHERE id = ?
        """, (category_id,))

        category = cursor.fetchone()
        if category:
            print(category)
        else:
            print("Category not found")
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

# Update operation for ExpensesCategory
def update_category(category_id, name):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE ExpensesCategory SET name = ?
            WHERE id = ?
        """, (name, category_id))

        connection.commit()
        print("Category updated successfully")
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

# Delete operation for ExpensesCategory
def delete_category(category_id):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM ExpensesCategory WHERE id = ?
        """, (category_id,))

        connection.commit()
        print("Category deleted successfully")
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

# Get all operation for ExpensesCategory
def get_all_categories():
    try:
        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM ExpensesCategory
        """)

        categories = cursor.fetchall()
        return categories

    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()

