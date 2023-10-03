# database/database

import psycopg2, os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import secrets

# Load environment variables from .env file
load_dotenv()

# Database config and connection
conn = psycopg2.connect(dbname=os.getenv('DATABASE_NAME'), user=os.getenv('DATABASE_USER'), password=os.getenv('DATABASE_PASSWORD'), host=os.getenv('DATABASE_HOST'), port=os.getenv('DATABASE_PORT'), sslmode=os.getenv('DATABASE_SSL_MODE'))

# SignUp user
def signup(email, password, chat_id):
     cursor = conn.cursor()
     cursor.execute('INSERT INTO users (email, password, chat_id) VALUES (%s, %s)', (email, password, chat_id))
     conn.commit()
     return True

# SignIn user
def signin(email, password):
     cursor = conn.cursor()
     cursor.execute('SELECT * FROM users WHERE email=%s AND password=%s', (email, password))
     user = cursor.fetchone()
     if user:
          print(user)
          # create_session(user[0])
          return user
     else:
          return False

# Create new session for user
def create_session(user_id):
     # Generate a unique session ID
     session_id = secrets.token_hex(16)

     # Insert session record into database
     cursor = conn.cursor()
     cursor.execute("INSERT INTO sessions (session_id, user_id, created_at) VALUES (%s, %s, %s)", (session_id, user_id, datetime.now()))
     conn.commit()

     return session_id

# Check if user has valid session
def check_session(chat_id):
     # Get user from database
     cursor = conn.cursor()
     cursor.execute('SELECT id FROM users WHERE chat_id=%s', chat_id)
     user = cursor.fetchone()

     # Check if user exists
     if user is not None:
          user_id = user[0]

          # Get session from database
          cursor = conn.cursor()
          cursor.execute("SELECT session_id, created_at FROM sessions WHERE user_id = %s", user_id)
          session = cursor.fetchone()

          # Check if session exists and is not expired
          if session is not None:
               session_id = session[0]
               created_at = session[1]
               if datetime.now() - created_at < timedelta(hours=1):
                    # Update session timestamp
                    cursor.execute("UPDATE sessions SET created_at = %s WHERE user_id = %s AND session_id = %s", (datetime.now(), user_id, session_id))
                    conn.commit()
                    return True
               # else:
                    # bot.reply_to(message, "Your session has expired. Please login again.")
          # else:
               # bot.reply_to(message, "Please login first.")

     return False
