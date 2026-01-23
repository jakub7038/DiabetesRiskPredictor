import sqlite3
import os

# Path to the database
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'health_predictor.db')

# If instance folder doesn't exist, try root (based on config default)
if not os.path.exists(db_path):
    db_path = os.path.join(os.path.dirname(__file__), 'health_predictor.db')

print(f"Connecting to database at: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if column exists
    cursor.execute("PRAGMA table_info(history)")
    columns = [info[1] for info in cursor.fetchall()]
    
    if 'model_scores' not in columns:
        print("Adding 'model_scores' column...")
        # SQLite doesn't have a native JSON type, it stores as TEXT
        cursor.execute("ALTER TABLE history ADD COLUMN model_scores TEXT")
        conn.commit()
        print("Column added successfully.")
    else:
        print("Column 'model_scores' already exists.")
        
    conn.close()

except Exception as e:
    print(f"Error: {e}")
