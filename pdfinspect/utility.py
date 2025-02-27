import os
import sqlite3


def get_db_path(pdf_path, db_path=None):
    if not db_path:
        db_path = os.path.dirname(pdf_path)
    if os.path.isdir(db_path):
        pdf_filename = os.path.basename(pdf_path)
        db_filename = os.path.splitext(pdf_filename)[0] + '.db'
        db_path = os.path.join(db_path, db_filename)
    return db_path


def fetch_data(db_path):
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute("SELECT id, parent_id, dictionary, decompressed_stream FROM pdf_streams")
  data = cursor.fetchall()
  conn.close()
  return data
