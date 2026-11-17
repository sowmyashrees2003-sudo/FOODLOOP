import sqlite3


def create_table():

    conn = sqlite3.connect("foodloop.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_name TEXT,
            food_name TEXT,
            quantity INTEGER,
            food_type TEXT,
            preparation_time TEXT,
            expiry_time TEXT,
            location TEXT,
            storage TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)

    cursor.execute("PRAGMA table_info(donations)")
    columns = [column[1] for column in cursor.fetchall()]

    if "status" not in columns:
        cursor.execute("""
            ALTER TABLE donations
            ADD COLUMN status TEXT DEFAULT 'Pending'
        """)

    conn.commit()
    conn.close()


def save_donation(donor, food, quantity, category,
                  preparation, expiry, location, storage):

    conn = sqlite3.connect("foodloop.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO donations
        (donor_name, food_name, quantity, food_type,
         preparation_time, expiry_time, location, storage)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        donor, food, quantity, category,
        preparation, expiry, location, storage
    ))

    conn.commit()
    conn.close()


def get_donations():

    conn = sqlite3.connect("foodloop.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            donor_name,
            food_name,
            quantity,
            food_type,
            preparation_time,
            expiry_time,
            location,
            storage,
            status
        FROM donations
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records


def update_donation_status(donation_id, new_status):

    conn = sqlite3.connect("foodloop.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE donations
        SET status = ?
        WHERE id = ?
    """, (new_status, donation_id))

    conn.commit()
    conn.close()