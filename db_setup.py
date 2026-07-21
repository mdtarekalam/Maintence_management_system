import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "mms_db",
}

BUILDINGS = [
    ("Building A",),
    ("Building B",),
    ("Building C",),
    ("Building D",),
]

ROOMS = [
    ("Building A", "108", "DSP Lab", 40),
    ("Building A", "102", "Electrical Circuit Lab", 40),
    ("Building A", "109", "Communication & Robotics Lab", 40),
    ("Building A", "101", "EEE Capstone Project Lab", 40),
    ("Building A", "110", "Physics Lab", 40),
    ("Building A", "202", "Classroom", 1),
    ("Building A", "209", "Classroom", 1),
    ("Building A", "201", "Classroom", 1),
    ("Building A", "210", "Classroom", 1),
    ("Building A", "211", "Classroom", 1),

    ("Building B", "B101", "Lab", 40),
    ("Building B", "B102", "Lab", 40),
    ("Building B", "B103", "Lab", 40),
    ("Building B", "B104", "Lab", 40),
    ("Building B", "B105", "Lab", 40),
    ("Building B", "B106", "Classroom", 1),
    ("Building B", "B107", "Library", 1),

    ("Building C", "CAFETERIA", "Cafeteria", 1),
    ("Building C", "201", "Student Affairs Office", 1),
    ("Building C", "202", "Student Affairs Office", 1),
    ("Building C", "203(a)", "Faculty Room", 1),
    ("Building C", "203(b)", "Exam and Records Office", 1),
    ("Building C", "204", "Classroom", 1),
    ("Building C", "205", "Classroom", 1),
    ("Building C", "206", "Classroom", 1),
    ("Building C", "207", "Classroom", 1),
    ("Building C", "208", "Center for Language Studies", 1),
    ("Building C", "209", "Faculty Room", 1),
    ("Building C", "301", "Proctor Office", 1),
    ("Building C", "302", "Faculty Room", 1),
    ("Building C", "303", "Faculty Room", 1),
    ("Building C", "304", "Faculty Room", 1),
    ("Building C", "305", "Head of CSE Office", 1),
    ("Building C", "306", "Normal Room", 1),
    ("Building C", "307", "Meeting Room", 1),
    ("Building C", "308", "Office", 1),
    ("Building C", "309", "CSE Department Office", 1),
    ("Building C", "310", "Faculty Room", 1),
    ("Building C", "311", "Faculty Room", 1),
    ("Building C", "312", "EEE Department Office", 1),
    ("Building C", "313", "Faculty Office", 1),
    ("Building C", "314", "Office", 1),
    ("Building C", "315", "Faculty Room", 1),
    ("Building C", "316", "Pantry", 1),
    ("Building C", "317", "Faculty Room", 1),
    ("Building C", "318", "Faculty Room", 1),
    ("Building C", "319", "Faculty Room", 1),
    ("Building C", "320", "Faculty Room", 1),
    ("Building C", "321", "Faculty Room", 1),
    ("Building C", "322", "Office", 1),
    ("Building C", "323", "Counselling Center", 1),
    ("Building C", "324", "Faculty Room", 1),
    ("Building C", "325", "Faculty Room", 1),

    ("Building D", "101", "Classroom", 1),
    ("Building D", "102", "Classroom", 1),
    ("Building D", "103", "Classroom", 1),
    ("Building D", "104", "Classroom", 1),
    ("Building D", "105", "Classroom", 1),
    ("Building D", "106", "Register Office", 1),
    ("Building D", "107", "Accounts Office", 1),
    ("Building D", "108", "Classroom", 1),
    ("Building D", "109", "Classroom", 1),
    ("Building D", "110", "Classroom", 1),
    ("Building D", "201", "Classroom", 1),
    ("Building D", "202", "Classroom", 1),
    ("Building D", "203", "Classroom", 1),
    ("Building D", "204", "Classroom", 1),
    ("Building D", "205", "Classroom", 1),
    ("Building D", "206", "Classroom", 1),
    ("Building D", "207", "Classroom", 1),
    ("Building D", "208", "Classroom", 1),
    ("Building D", "209", "Classroom", 1),
    ("Building D", "210", "Classroom", 1),
    ("Building D", "301", "Classroom", 1),
    ("Building D", "302", "Classroom", 1),
    ("Building D", "303", "English & Humanities Program Office", 1),
    ("Building D", "304", "Dean's Office", 1),
    ("Building D", "305", "MBA & EMBA Program Office", 1),
    ("Building D", "306", "Classroom", 1),
    ("Building D", "307", "Classroom", 1),
    ("Building D", "308", "Office", 1),
    ("Building D", "309", "Classroom", 1),
]

DEVICES = [
    ("Keyboard",),
    ("Mouse",),
    ("Monitor",),
    ("Projector",),
    ("Socket",),
    ("Internet",),
    ("Speaker",),
    ("Printer",),
    ("Fan",),
]


def get_connection(db=None):
    config = {"host": DB_CONFIG["host"], "user": DB_CONFIG["user"], "password": DB_CONFIG["password"]}
    if db:
        config["database"] = db
    return mysql.connector.connect(**config)


def create_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS mms_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.close()
    conn.close()


def create_tables():
    conn = get_connection("mms_db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS buildings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            building_name VARCHAR(100) UNIQUE NOT NULL
        ) ENGINE=InnoDB
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS rooms (
            id INT AUTO_INCREMENT PRIMARY KEY,
            building_id INT NOT NULL,
            room_number VARCHAR(50) NOT NULL,
            room_type VARCHAR(100) DEFAULT 'Unknown',
            UNIQUE KEY unique_room (building_id, room_number),
            FOREIGN KEY (building_id) REFERENCES buildings(id) ON DELETE CASCADE
        ) ENGINE=InnoDB
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS computers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            room_id INT NOT NULL,
            computer_number VARCHAR(50) NOT NULL,
            UNIQUE KEY unique_computer (room_id, computer_number),
            FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
        ) ENGINE=InnoDB
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS devices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            device_name VARCHAR(100) UNIQUE NOT NULL
        ) ENGINE=InnoDB
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(120),
            user_id VARCHAR(80) UNIQUE,
            email VARCHAR(120) UNIQUE,
            password VARCHAR(120),
            department VARCHAR(80),
            role VARCHAR(30)
        ) ENGINE=InnoDB
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS admin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(80) UNIQUE,
            password VARCHAR(120)
        ) ENGINE=InnoDB
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS complaints (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            computer_id INT,
            device_id INT,
            description TEXT,
            status VARCHAR(40) DEFAULT 'Pending',
            priority VARCHAR(40) DEFAULT 'Low',
            admin_note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (computer_id) REFERENCES computers(id) ON DELETE SET NULL,
            FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE SET NULL
        ) ENGINE=InnoDB
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS suggestions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            computer_id INT,
            device_id INT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (computer_id) REFERENCES computers(id) ON DELETE SET NULL,
            FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE SET NULL
        ) ENGINE=InnoDB
        """
    )

    conn.commit()
    cursor.close()
    conn.close()


def canonical_building_name(name):
    mapping = {
        "A Building": "Building A",
        "B Building": "Building B",
        "C Building": "Building C",
        "D Building": "Building D",
    }
    return mapping.get(name, name)


def cleanup_buildings():
    conn = get_connection("mms_db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, building_name FROM buildings")
    rows = cursor.fetchall()

    groups = {}
    for bid, name in rows:
        canonical = canonical_building_name(name)
        groups.setdefault(canonical, []).append((bid, name))

    for canonical, items in groups.items():
        keep_id = items[0][0]
        keep_name = items[0][1]
        if keep_name != canonical:
            cursor.execute("UPDATE buildings SET building_name = %s WHERE id = %s", (canonical, keep_id))

        for bid, name in items[1:]:
            cursor.execute("UPDATE rooms SET building_id = %s WHERE building_id = %s", (keep_id, bid))
            cursor.execute("DELETE FROM buildings WHERE id = %s", (bid,))

    cursor.execute("ALTER TABLE buildings ADD UNIQUE KEY unique_building_name (building_name)")
    conn.commit()
    cursor.close()
    conn.close()


def seed_data():
    conn = get_connection("mms_db")
    cursor = conn.cursor()

    cursor.executemany("INSERT IGNORE INTO buildings (building_name) VALUES (%s)", BUILDINGS)
    conn.commit()

    cursor.execute("SELECT id, building_name FROM buildings")
    building_map = {name: bid for bid, name in cursor.fetchall()}

    room_rows = []
    computer_rows = []
    for building_name, room_number, room_type, count in ROOMS:
        building_id = building_map[building_name]
        room_rows.append((building_id, room_number, room_type))

    cursor.executemany(
        "INSERT IGNORE INTO rooms (building_id, room_number, room_type) VALUES (%s, %s, %s)",
        room_rows,
    )
    conn.commit()

    cursor.execute("SELECT id, building_id, room_number FROM rooms")
    room_map = {(bid, rnum): rid for rid, bid, rnum in cursor.fetchall()}

    for building_name, room_number, room_type, count in ROOMS:
        building_id = building_map[building_name]
        room_id = room_map[(building_id, room_number)]
        if count <= 0:
            continue
        for n in range(1, count + 1):
            computer_rows.append((room_id, str(n)))

    cursor.executemany(
        "INSERT IGNORE INTO computers (room_id, computer_number) VALUES (%s, %s)",
        computer_rows,
    )
    conn.commit()

    cursor.executemany("INSERT IGNORE INTO devices (device_name) VALUES (%s)", DEVICES)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM admin")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", ("admin", "admin123"))
        conn.commit()

    cursor.close()
    conn.close()


def main():
    print("Creating database and tables...")
    create_database()
    create_tables()
    print("Cleaning up buildings...")
    cleanup_buildings()
    print("Seeding data...")
    seed_data()
    print("Setup complete. Run python main.py to start the application.")


if __name__ == "__main__":
    main()
