import os
from dotenv import load_dotenv
import pymysql

load_dotenv()
conn = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', 3306)),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', 'root'),
    database=os.getenv('DB_NAME', 'habit_tracker')
)
cursor = conn.cursor()

# Check which columns already exist
cursor.execute('DESCRIBE users')
existing_cols = {row[0] for row in cursor.fetchall()}
print('Existing columns:', existing_cols)

# Columns to add if missing
migrations = [
    ('gender', 'VARCHAR(10) NULL'),
    ('height', 'FLOAT NULL'),
    ('weight', 'FLOAT NULL'),
    ('daily_calorie_goal', 'INT DEFAULT 2000'),
    ('daily_protein_goal', 'FLOAT DEFAULT 50.0'),
    ('water_goal_glasses', 'INT DEFAULT 8'),
    ('diet_type', "VARCHAR(20) DEFAULT 'Veg'"),
    ('allergies', 'VARCHAR(255) NULL'),
    ('step_goal', 'INT DEFAULT 10000'),
]

for col, definition in migrations:
    if col not in existing_cols:
        sql = f'ALTER TABLE users ADD COLUMN {col} {definition}'
        print(f'Adding missing column: {col}')
        cursor.execute(sql)
    else:
        print(f'Column already exists (skipping): {col}')

conn.commit()
cursor.close()
conn.close()
print('\nMigration complete!')
