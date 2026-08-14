import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import get_connection


def remove_duplicates():
    conn = get_connection()
    if not conn:
        print('DB connect failed')
        return
    cursor = conn.cursor()
    cursor.execute("SELECT id, room_number FROM rooms WHERE LOWER(room_type) LIKE '%classroom%'")
    rooms = cursor.fetchall()
    total_removed = 0
    for rid, rnum in rooms:
        cursor.execute("SELECT id, computer_number FROM computers WHERE room_id = %s ORDER BY id", (rid,))
        comps = cursor.fetchall()
        # find faculty-like ids
        faculty_ids = [cid for cid, cnum in comps if str(cnum).lower() in ('faculty computer', 'faculty', '0')]
        if len(faculty_ids) <= 1:
            continue
        keep = faculty_ids[0]
        delete = faculty_ids[1:]
        for did in delete:
            cursor.execute("UPDATE complaints SET computer_id = %s WHERE computer_id = %s", (keep, did))
        cursor.executemany("DELETE FROM computers WHERE id = %s", [(d,) for d in delete])
        conn.commit()
        total_removed += len(delete)
        print(f'Room {rnum}: removed {len(delete)} duplicate faculty computers')
    cursor.close()
    conn.close()
    print('Done. Total removed', total_removed)

if __name__ == '__main__':
    remove_duplicates()
