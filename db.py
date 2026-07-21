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
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(id), building_name FROM buildings GROUP BY building_name ORDER BY building_name")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_rooms(building_id):
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT id, room_number, room_type FROM rooms WHERE building_id = %s", (building_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_computers(room_id):
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT id, computer_number FROM computers WHERE room_id = %s ORDER BY computer_number", (room_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_devices():
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT id, device_name FROM devices")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def check_user_login(user_id, password, role):
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
        if err.errno == 1062:
            return False, "This ID or email is already registered"
        return False, f"Database error: {err}"


def submit_complaint(user_id, computer_id, device_id, description):
    conn = get_connection()
    if not conn:
        return False, "Could not connect to database"
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO complaints (user_id, computer_id, device_id, description, status, priority) "
            "VALUES (%s, %s, %s, %s, 'Pending', 'Low')",
            (user_id, computer_id, device_id, description)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Complaint submitted successfully"
    except mysql.connector.Error as err:
        conn.close()
        return False, f"Database error: {err}"


def submit_suggestion(user_id, computer_id, device_id, description):
    conn = get_connection()
    if not conn:
        return False, "Could not connect to database"
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO suggestions (user_id, computer_id, device_id, description) "
            "VALUES (%s, %s, %s, %s)",
            (user_id, computer_id, device_id, description)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Suggestion submitted successfully"
    except mysql.connector.Error as err:
        conn.close()
        return False, f"Database error: {err}"


def get_user_complaints(user_id):
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.id, c.description, c.status, c.priority, c.admin_note, c.created_at,
               comp.computer_number, r.room_number, b.building_name, d.device_name
        FROM complaints c
        JOIN computers comp ON c.computer_id = comp.id
        JOIN rooms r ON comp.room_id = r.id
        JOIN buildings b ON r.building_id = b.id
        JOIN devices d ON c.device_id = d.id
        WHERE c.user_id = %s
        ORDER BY c.created_at DESC
    """, (user_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_all_complaints():
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.id, c.description, c.status, c.priority, c.admin_note, c.created_at,
               comp.computer_number, r.room_number, b.building_name, d.device_name,
               u.full_name AS reporter_name, u.user_id AS reporter_id
        FROM complaints c
        JOIN computers comp ON c.computer_id = comp.id
        JOIN rooms r ON comp.room_id = r.id
        JOIN buildings b ON r.building_id = b.id
        JOIN devices d ON c.device_id = d.id
        LEFT JOIN users u ON c.user_id = u.id
        ORDER BY c.created_at DESC
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def update_complaint(complaint_id, status, priority, admin_note):
    conn = get_connection()
    if not conn:
        return False, "Could not connect to database"
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE complaints SET status = %s, priority = %s, admin_note = %s WHERE id = %s",
            (status, priority, admin_note, complaint_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Complaint updated successfully"
    except mysql.connector.Error as err:
        conn.close()
        return False, f"Database error: {err}"


def get_device_complaint_stats():
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.device_name, COUNT(*) AS complaint_count
        FROM complaints c
        JOIN devices d ON c.device_id = d.id
        GROUP BY d.device_name
        ORDER BY complaint_count DESC
        LIMIT 5
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_status_summary():
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("""
        SELECT status, COUNT(*) AS count
        FROM complaints
        GROUP BY status
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_priority_summary():
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("""
        SELECT priority, COUNT(*) AS count
        FROM complaints
        GROUP BY priority
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


# Admin helper functions below

def get_all_complaints():
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.id, c.description, c.status, c.priority, c.admin_note, c.created_at,
               comp.computer_number, r.room_number, b.building_name, d.device_name,
               u.full_name AS reporter_name, u.user_id AS reporter_id
        FROM complaints c
        JOIN computers comp ON c.computer_id = comp.id
        JOIN rooms r ON comp.room_id = r.id
        JOIN buildings b ON r.building_id = b.id
        JOIN devices d ON c.device_id = d.id
        LEFT JOIN users u ON c.user_id = u.id
        ORDER BY c.created_at DESC
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def update_complaint(complaint_id, status, priority, admin_note):
    conn = get_connection()
    if not conn:
        return False, "Could not connect to database"
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE complaints SET status = %s, priority = %s, admin_note = %s WHERE id = %s",
            (status, priority, admin_note, complaint_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Complaint updated successfully"
    except mysql.connector.Error as err:
        conn.close()
        return False, f"Database error: {err}"


def get_device_complaint_stats():
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.device_name, COUNT(*) AS complaint_count
        FROM complaints c
        JOIN devices d ON c.device_id = d.id
        GROUP BY d.device_name
        ORDER BY complaint_count DESC
        LIMIT 5
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_status_summary():
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("""
        SELECT status, COUNT(*) AS count
        FROM complaints
        GROUP BY status
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_priority_summary():
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("""
        SELECT priority, COUNT(*) AS count
        FROM complaints
        GROUP BY priority
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


if __name__ == "__main__":
    print("Buildings:", get_buildings())
    print("Devices:", get_devices())