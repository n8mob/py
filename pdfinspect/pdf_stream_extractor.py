# pdf_stream_extractor.py
import argparse
import re
import sqlite3
import zlib

from pdf_db_filename import get_db_path


def create_database(db_name):
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS pdf_streams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER,
    dictionary TEXT,
    decompressed_stream TEXT,
    FOREIGN KEY(parent_id) REFERENCES pdf_streams(id)
  )
  """)
  conn.commit()
  return conn


def insert_data(conn, dictionary, decompressed_stream, parent_id=None):
  cursor = conn.cursor()
  cursor.execute("""
  INSERT INTO pdf_streams (parent_id, dictionary, decompressed_stream)
  VALUES (?, ?, ?)""",(parent_id, dictionary, decompressed_stream))
  conn.commit()
  return cursor.lastrowid


def main(args):
  args.db_path = get_db_path(args.filename, args.db_path)
  conn = create_database(args.db_path)
  with open(args.filename, "rb") as f:
    data = f.read()
  pattern = re.compile(rb'(<<.*?>>)\s*stream\s*(.*?)\s*endstream', re.DOTALL)
  matches = pattern.findall(data)
  for dictionary, stream in matches:
    dict_str = dictionary.decode(errors="ignore")
    decompressed_str = ""
    if args.decompress:
      try:
        decompressed = zlib.decompress(stream)
        decompressed_str = decompressed.decode(errors="ignore")
        nested_pattern = re.compile(rb'(<<.*?>>)\s*stream\s*(.*?)\s*endstream', re.DOTALL)
        nested_matches = nested_pattern.findall(decompressed)
        parent_id = insert_data(conn, dict_str, decompressed_str)
        for nested_dict, nested_stream in nested_matches:
          nested_dict_str = nested_dict.decode(errors="ignore")
          nested_decompressed_str = zlib.decompress(nested_stream).decode(errors="ignore")
          insert_data(conn, nested_dict_str, nested_decompressed_str, parent_id)
      except zlib.error:
        insert_data(conn, dict_str, stream)
    else:
      insert_data(conn, dict_str, decompressed_str)
  conn.close()


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Extract streams from a PDF file and store in SQLite database")
  parser.add_argument("filename", help="The PDF file from which to extract streams")
  parser.add_argument("--decompress", help="Decompress the stream using zlib", action="store_true", default=True)
  parser.add_argument("--db-path", help="Path to the SQLite database file to store the extracted streams", default=None)
  script_args = parser.parse_args()
  main(script_args)
