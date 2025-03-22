import os
import psycopg2
from decouple import config

SUPABASE_HOST = config("SUPABASE_HOST")
SUPABASE_KEY = config("SUPABASE_KEY")
SUPABASE_DB_URL = config("SUPABASE_DB_URL")

def get_db_connection():
    return psycopg2.connect(SUPABASE_DB_URL)

def fetch_events():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT id, title, description, start_date, end_date
    FROM location_event WHERE start_time > NOW();
    """

    cursor.execute(query)
    events = cursor.fetchall()

    event_list = [
        {"id": e[0], "title": e[1], "description": e[2]}
        for e in events
    ]

    cursor.close()
    conn.close()
    return event_list

    # headers = {"apikey": SUPABASE_KEY}
    # url = f"{SUPABASE_URL}"