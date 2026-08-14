import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import get_connection, ensure_computer_exists, ensure_device_exists

def fix_classrooms():
    conn = get_connection()
    if not conn:
        print('Could not connect to database')
        return
    cursor = conn.cursor()
    cursor.execute("SELECT id, room_number, room_type FROM rooms WHERE LOWER(room_type) LIKE '%classroom%'")
    rooms = cursor.fetchall()
    print(f'Found {len(rooms)} classroom rooms')
    removed_total = 0
    for rid, rnum, rtype in rooms:
        cursor.execute("SELECT id, computer_number FROM computers WHERE room_id = %s ORDER BY id", (rid,))
        comps = cursor.fetchall()
        if not comps:
            # ensure a faculty computer exists
            ensure_computer_exists(rid, 'Faculty Computer')
            print(f'Room {rnum}: added Faculty Computer')
            continue
        # prefer a Faculty Computer to keep
        keep_id = None
        for cid, cnum in comps:
            if str(cnum).lower() == 'faculty computer':
                keep_id = cid
                break
        if keep_id is None:
            # keep the first one
            keep_id = comps[0][0]
            # also ensure faculty computer exists
            ensure_computer_exists(rid, 'Faculty Computer')
        # delete others
        delete_ids = [cid for cid, _ in comps if cid != keep_id]
        if delete_ids:
            # reassign any complaints referencing the deleted computers to the kept computer
            for did in delete_ids:
                cursor.execute("UPDATE complaints SET computer_id = %s WHERE computer_id = %s", (keep_id, did))
            # now safe to delete
            cursor.executemany("DELETE FROM computers WHERE id = %s", [(did,) for did in delete_ids])
            conn.commit()
            removed_total += len(delete_ids)
            print(f'Room {rnum}: removed {len(delete_ids)} extra computers (complaints reassigned)')
        else:
            print(f'Room {rnum}: already has single computer')
        # ensure classroom devices exist
        for dn in ['AC', 'Projector', 'Fan', 'Speaker', 'Faculty Computer']:
            ensure_device_exists(dn)
    cursor.close()
    conn.close()
    print(f'Done. Removed {removed_total} computer rows.')

if __name__ == '__main__':
    fix_classrooms()
