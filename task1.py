#import required libraries 
import pandas as pd  # Used for handling tabular data
import sqlite3  # Helps store data in a small database (like a baby version of SQL)
import matplotlib
matplotlib.use("Agg")  # Use a non-GUI backend
import matplotlib.pyplot as plt # Used for drawing graphs
import seaborn as sns  # Makes graphs look better and easier to understand

# Create the database
def init_db():
    conn = sqlite3.connect("finance.db")  # Connect to database or create if it doesn't exist
    cursor = conn.cursor()  # Allows us to execute SQL commands

    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      type TEXT,
                      category TEXT,
                      amount REAL,
                      date TEXT)''')  # Create table

    conn.commit()  # Save changes to database
    conn.close()

# Adding a transaction
def add_transaction(t_type, category, amount, date):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)",
                   (t_type, category, amount, date))  # Add new record
    conn.commit()
    conn.close()

# Fetching all transactions
def get_transactions():
    conn = sqlite3.connect("finance.db")
    df = pd.read_sql_query("SELECT * FROM transactions", conn)  # Correct table name
    conn.close()
    return df  # Return the data as a table

# Generate a spending report
def generate_report():
    df = get_transactions()
    if df.empty:
        print("No data available")
        return
    
    df_expenses = df[df['type'] == 'Expense']  # Filter only expenses
    category_summary = df_expenses.groupby('category')['amount'].sum()  # Sum expenses by category

    plt.figure(figsize=(8, 5))  # Set figure size
    sns.barplot(x=category_summary.index, y=category_summary.values)  # Create a bar chart
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.title("Spending by Category")  # Title
    plt.xlabel("Category")  
    plt.ylabel("Total Spent")  
    plt.show()

# Exporting data to CSV file
def export_csv():
    df = get_transactions()
    df.to_csv("finance_data.csv", index=False)  # Save the data to a CSV file
    print("Data exported successfully")

# Running the program
init_db()

add_transaction("Income", "Salary", 5000, "2025-01-28")  # Fixed typo
add_transaction("Expense", "Rent", 1200, "2025-01-28")
add_transaction("Expense", "Groceries", 300, "2025-01-28")

generate_report()  # Generate report
export_csv()  # Export data
