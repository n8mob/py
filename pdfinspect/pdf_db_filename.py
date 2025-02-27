import os

def get_db_path(pdf_path, db_path=None):
    if not db_path:
        db_path = os.path.dirname(pdf_path)
    if os.path.isdir(db_path):
        pdf_filename = os.path.basename(pdf_path)
        db_filename = os.path.splitext(pdf_filename)[0] + '.db'
        db_path = os.path.join(db_path, db_filename)
    return db_path
