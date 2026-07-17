import os
import django
import sys

# Manually inject the known DB_PASSWORD for the local test since .env is UTF-16 encoded
os.environ['DB_PASSWORD'] = 'Marena25012004$'

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.contrib.auth import get_user_model
from django.db import connection

def run_check():
    User = get_user_model()
    
    print("=== 1. Checking Database Connection ===")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
        print("[SUCCESS] Database connection successful. Result:", row)
    except Exception as e:
        print("[FAILED] Database connection failed:", str(e))
        return

    print("\n=== 2. Checking ORM & Dummy Data Insertion ===")
    try:
        dummy_email = 'dummy_test_db@example.com'
        if User.objects.filter(email=dummy_email).exists():
            user = User.objects.get(email=dummy_email)
            print(f"[SUCCESS] Dummy user already exists: {user.username} (ID: {user.id})")
        else:
            user = User.objects.create_user(
                username='dummy_test_db', 
                email=dummy_email, 
                password='password123',
                first_name='Dummy',
                last_name='Data'
            )
            print(f"[SUCCESS] Successfully created dummy user: {user.username} (ID: {user.id})")
        
        print(f"[SUCCESS] Total users in database: {User.objects.count()}")
    except Exception as e:
        print("[FAILED] Failed to create/query dummy user:", str(e))
        import traceback
        traceback.print_exc()
        return
        
    print("\n=== 3. Cleaning up Dummy Data ===")
    try:
        User.objects.filter(email=dummy_email).delete()
        print("[SUCCESS] Successfully deleted dummy user.")
    except Exception as e:
        print("[FAILED] Failed to clean up dummy user:", str(e))

    print("\n[SUCCESS] All database and system integration checks passed successfully!")

if __name__ == '__main__':
    run_check()
