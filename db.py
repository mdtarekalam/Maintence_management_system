import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="mms_db"
        )
        return conn
    except mysql.connector.Error as err:
        print("❌ Connection failed:", err)
        return None


def get_buildings():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM buildings")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    return []


def check_user_login(user_id, password, role):
    """Check login for Student, Faculty, or Staff against the users table."""
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM users WHERE user_id = %s AND password = %s AND role = %s",
        (user_id, password, role)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def check_admin_login(username, password):
    """Check login for Admin against the admin table."""
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM admin WHERE username = %s AND password = %s",
        (username, password)
    )
    admin = cursor.fetchone()
    cursor.close()
    conn.close()
    return admin


def register_user(full_name, user_id, email, password, department, role):
    """Insert a new user into the users table."""
    conn = get_connection()
    if not conn:
        return False, "Could not connect to database"
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (full_name, user_id, email, password, department, role) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (full_name, user_id, email, password, department, role)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Registration successful"
    except mysql.connector.Error as err:
        conn.close()
        if err.errno == 1062:  # duplicate entry error code
            return False, "This ID or email is already registered"
        return False, f"Database error: {err}"


if __name__ == "__main__":
    buildings = get_buildings()
    for b in buildings:
        print(b)