import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

passwords = ["", "root", "password", "1234", "12345678"]
base_url = "mysql+pymysql://root:{}@localhost/habit_tracker"

for p in passwords:
    url = base_url.format(p)
    print(f"Testing root with password: '{p}'...")
    try:
        engine = create_engine(url)
        conn = engine.connect()
        print(f"SUCCESS! Found password: '{p}'")
        conn.close()
        break
    except Exception as e:
        print(f"Failed: {e}")
