import sqlite3
import pandas as pd

def create_sample_db(db_path='sample.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY,
        age INTEGER,
        systolic_bp REAL,
        diastolic_bp REAL,
        symptoms TEXT,
        diagnosis TEXT
    )
    ''')
    conn.commit()
    # Insert sample data if table empty
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM patients')
    count = cur.fetchone()[0]
    if count == 0:
        sample = [
            (25, 120, 80, 'headache, nausea', 'migraine'),
            (67, 150, 95, 'chest pain, shortness of breath', 'angina'),
            (54, 135, 85, 'fatigue', 'hypertension'),
            (40, 128, 82, 'dizziness', 'vertigo'),
            (30, 110, 70, 'fever, cough', 'infection'),
        ]
        c.executemany('INSERT INTO patients (age, systolic_bp, diastolic_bp, symptoms, diagnosis) VALUES (?,?,?,?,?)', sample)
        conn.commit()
    conn.close()

def read_db_to_csv(db_path='sample.db', csv_path='sample_from_db.csv'):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query('SELECT * FROM patients', conn)
    df.to_csv(csv_path, index=False)
    conn.close()
    return csv_path
