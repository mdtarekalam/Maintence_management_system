import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import get_connection


def cleanup():
    conn = get_connection()
    if not conn:
        print('DB connect failed')
        return
    cursor = conn.cursor()
    cursor.execute("SELECT id, room_number FROM rooms WHERE LOWER(room_type) LIKE '%classroom%'")
    rooms = cursor.fetchall()
    removed = 0
    for rid, rnum in rooms:
        # find computers in this room
        cursor.execute("SELECT id, computer_number FROM computers WHERE room_id = %s ORDER BY id", (rid,))
        comps = cursor.fetchall()
        # normalize computer_number to string
        faculty_ids = [cid for cid, cnum in comps if str(cnum).lower() in ('faculty computer', 'faculty', '0')]
        # if multiple faculty entries, keep first, delete others
        if len(faculty_ids) > 1:
            keep = faculty_ids[0]
            delete = faculty_ids[1:]
            for did in delete:
                cursor.execute("UPDATE complaints SET computer_id = %s WHERE computer_id = %s", (keep, did))
            cursor.executemany("DELETE FROM computers WHERE id = %s", [(d,) for d in delete])
            conn.commit()
            removed += len(delete)
            print(f'Room {rnum}: removed {len(delete)} duplicate faculty computers')
        # remove Computer 1 entries (numeric or literal) and reassign to faculty
        comp1_ids = [cid for cid, cnum in comps if str(cnum).lower() in ('1', 'computer 1')]
        if comp1_ids:
            # find an alternate computer to reassign complaints to
            cursor.execute("SELECT id FROM computers WHERE room_id = %s AND id NOT IN (%s) LIMIT 1" % ("%s", ",".join(["%s"]*len(comp1_ids))), [rid] + comp1_ids)
            row = cursor.fetchone()
            if row:
                target = row[0]
            else:
                # create a new Faculty Computer entry
                cursor.execute("INSERT INTO computers (room_id, computer_number) VALUES (%s, %s)", (rid, 0))
                conn.commit()
                target = cursor.lastrowid
            for did in comp1_ids:
                cursor.execute("UPDATE complaints SET computer_id = %s WHERE computer_id = %s", (target, did))
            cursor.executemany("DELETE FROM computers WHERE id = %s", [(d,) for d in comp1_ids])
            conn.commit()
            removed += len(comp1_ids)
            print(f'Room {rnum}: removed {len(comp1_ids)} Computer 1 entries (reassigned to {target})')
    cursor.close()
    conn.close()
    print('Cleanup done. Removed rows:', removed)

if __name__ == '__main__':
    cleanup()
