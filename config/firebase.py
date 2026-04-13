import os
import firebase_admin
from firebase_admin import credentials, auth, firestore
from dotenv import load_dotenv

load_dotenv()

# Path to your serviceAccountKey.json
# You need to download this from Firebase Console -> Project Settings -> Service accounts
SERVICE_ACCOUNT_KEY = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "serviceAccountKey.json")

# Initialize Firebase Admin SDK
try:
    if not firebase_admin._apps:
        if os.path.exists(SERVICE_ACCOUNT_KEY):
            cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
            firebase_admin.initialize_app(cred)
            print("Successfully initialized Firebase Admin SDK with service account.")
        else:
            # Try to initialize with default credentials (useful for GCP environments)
            # If this fails, the app will still start but Firestore calls will fail
            firebase_admin.initialize_app()
            print("Initialized Firebase Admin SDK with default credentials.")
except Exception as e:
    print(f"CRITICAL Warning: Firebase Admin SDK NOT initialized correctly. Firestore features will fail. Error: {e}")

# Get Firestore database client
try:
    db = firestore.client()
except Exception as e:
    print(f"Warning: Could not create Firestore client. Database operations will fail. Error: {e}")
    db = None

# Firebase Web API Key for login (REST API)
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY", "YOUR_WEB_API_KEY")
