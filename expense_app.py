import streamlit as st
import pandas as pd
import sqlite3
from datetime import date
import io

# Initialize DB
def init_expense_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_date TEXT,
            category TEXT,
            description TEXT,
            amount REAL
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(expense_date, category, description, amount):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('INSERT INTO expenses (expense_date, category, description, amount) VALUES (?, ?, ?, ?)',
              (expense_date, category, description, amount))
    conn.commit()
    conn.close()

def get_expenses():
    conn = sqlite3.connect('expenses.db')
    df = pd.read_sql_query('SELECT expense_date, category, description, amount FROM expenses ORDER BY expense_date DESC', conn)
    conn.close()
    return df

init_expense_db()

st.title("Daily Financial Expense Tracker")

with st.form("expense_form"):
    expense_date = st.date_input("Date", value=date.today())
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Expense")
    if submitted:
        add_expense(str(expense_date), category, description, amount)
        st.success("Expense added!")

st.header("Expense History")
df = get_expenses()
st.dataframe(df, use_container_width=True)

# Download buttons
st.subheader("Download Expense Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", data=csv, file_name="expenses.csv", mime="text/csv")

# Fix for XLSX download
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df.to_excel(writer, index=False)
xlsx_data = output.getvalue()
st.download_button("Download XLSX", data=xlsx_data, file_name="expenses.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")