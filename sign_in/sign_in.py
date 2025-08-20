import streamlit as st
import sqlite3

def sign_in():
    st.title("Sign IN")
    st.write("Please enter your credentials to sign in.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign IN"):
        try:
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cur.fetchone()
            conn.close()
            if user:
                st.success(f"Welcome, {username}!")
                # Show user list only after successful sign in
                conn = sqlite3.connect('users.db')
                cur = conn.cursor()
                cur.execute("SELECT username, age, email, gender FROM users")
                allUsers = cur.fetchall()
                conn.close()
                st.header("User List")
      
                st.dataframe(allUsers, use_container_width=True)
            else:
                st.error("Invalid username or password.")
        except sqlite3.Error as e:
            st.error(f"An error occurred: {e}")