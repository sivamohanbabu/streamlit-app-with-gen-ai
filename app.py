import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu
from expense_app import expense_tracker  # Import your expense tracker

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            age INTEGER,
            email TEXT,
            password TEXT,
            gender TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, age, email, password, gender):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?)', (username, age, email, password, gender))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

init_db()

def home():
    st.title("Home")
    st.write("Welcome to the Home page!")

def sign_in():
    st.title("Sign IN")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        user = authenticate_user(username, password)
        if user:
            st.success(f"Welcome back, {user[0]}!")
            # Fetch and display all users after successful sign in
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("SELECT username, age, email, gender FROM users")
            all_users = c.fetchall()
            conn.close()
            st.header("User List")
            st.dataframe(all_users, use_container_width=True)
        else:
            st.error("Invalid username or password.")

def sign_up():
    st.title("Sign UP")
    username = st.text_input("Username")
    age = st.number_input("Age", min_value=1, max_value=120)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    if st.button("Sign Up"):
        if username and email and password:
            success = add_user(username, age, email, password, gender)
            if success:
                st.success("Account created successfully!")
            else:
                st.error("Username already exists.")
        else:
            st.warning("Please fill all required fields.")

def contact_us():
    st.title("Contact Us")
    st.write("Get in touch with us.")

def chat_with_ai():
    st.title("Chat with AI")
    prompt = st.text_input("Ask me Anything")
    if prompt and st.button("Send"):
        import google.generativeai as genai
        genai.configure(api_key="AIzaSyCWzcmk2_yHv7v9Bg9Q-iQlU-mHEeiTnBU")
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        st.write(response.text)

with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Home", 'Sign IN', 'Sign UP', 'Contact Us', 'Chat', 'Expense Tracker'],
        icons=['house', 'box-arrow-in-right', 'person-add', 'envelope', 'chat', 'cash'],
        menu_icon="cast",
        default_index=0
    )

if selected == 'Home':
    home()
elif selected == 'Sign IN':
    sign_in()
elif selected == 'Sign UP':
    sign_up()
elif selected == 'Contact Us':
    contact_us()
elif selected == 'Chat':
    chat_with_ai()
elif selected == 'Expense Tracker':
    expense_tracker()