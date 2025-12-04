import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        user="root",
        password="root",
        host="localhost",
        database="expense_manager"
    )
    if connection:
        print("Connected with the database successfully..")
    else:
        print("Error conencting to the database..")
    
    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()

    cursor.close()
    connection.close()

def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with date : {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expense_manager.expenses WHERE expense_date=%s",(expense_date,))
        expenses = cursor.fetchall()
        return expenses


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start : {start_date}, end : {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute('''
                    SELECT category, SUM(amount) as total FROM expenses 
                    where expense_date 
                    between %s and %s
                    group by category;
                ''', (start_date,end_date))
        summary = cursor.fetchall()
        return summary


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with date : {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expense_manager.expenses WHERE expense_date=%s",(expense_date,))
        

def insert_expenses_for_date(expense_date, amount, category, notes):
    logger.info(f"insert_expenses_for_date called with date : {expense_date},amount : {amount},category : {category},notes : {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("INSERT INTO expense_manager.expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",(expense_date, amount, category, notes))
        

if __name__ == "__main__":
    expenses = fetch_expenses_for_date("2024-08-01")
    print(expenses)
    delete_expenses_for_date("2024-10-01")
    sum = fetch_expense_summary("2024-08-01","2024-08-05")
    print(sum)