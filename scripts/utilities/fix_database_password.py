"""
Helper script to test and fix database password configuration.
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

import psycopg2
from getpass import getpass


def test_connection(password):
    """Test database connection with given password."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="fakedetect",
            user="postgres",
            password=password
        )
        conn.close()
        return True
    except psycopg2.OperationalError as e:
        if "does not exist" in str(e):
            print(f"⚠️  Database 'fakedetect' does not exist. Create it first!")
            return False
        return False
    except Exception as e:
        return False


def update_config_file(password):
    """Update the config.py file with the correct password."""
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'src', 'config.py')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the database_url line
        import re
        pattern = r'database_url: str = "postgresql://postgres:[^@]*@localhost:5432/fakedetect"'
        replacement = f'database_url: str = "postgresql://postgres:{password}@localhost:5432/fakedetect"'
        
        new_content = re.sub(pattern, replacement, content)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"❌ Error updating config file: {e}")
        return False


def main():
    print("=" * 60)
    print("Database Password Configuration Helper")
    print("=" * 60)
    print()
    
    # Try common passwords first
    print("Testing common default passwords...")
    common_passwords = ['postgres', 'admin', '123123', 'password', '123456', '']
    
    for pwd in common_passwords:
        print(f"  Trying: {'(empty)' if pwd == '' else pwd}...", end=' ')
        if test_connection(pwd):
            print("✅ SUCCESS!")
            print()
            print(f"✅ Found working password: {'(empty)' if pwd == '' else pwd}")
            print()
            
            response = input("Do you want to update config.py with this password? (y/n): ")
            if response.lower() == 'y':
                if update_config_file(pwd):
                    print("✅ Configuration updated successfully!")
                    print()
                    print("You can now run: python scripts\\utilities\\run_backend.py")
                else:
                    print("❌ Failed to update configuration")
            return
        else:
            print("❌")
    
    print()
    print("❌ None of the common passwords worked.")
    print()
    
    # Ask user for password
    print("Please enter your PostgreSQL password manually:")
    print("(The password will be hidden as you type)")
    print()
    
    while True:
        password = getpass("PostgreSQL password for user 'postgres': ")
        
        print("Testing connection...", end=' ')
        if test_connection(password):
            print("✅ SUCCESS!")
            print()
            
            response = input("Do you want to update config.py with this password? (y/n): ")
            if response.lower() == 'y':
                if update_config_file(password):
                    print("✅ Configuration updated successfully!")
                    print()
                    print("You can now run: python scripts\\utilities\\run_backend.py")
                else:
                    print("❌ Failed to update configuration")
            break
        else:
            print("❌ Failed")
            print()
            retry = input("Try again? (y/n): ")
            if retry.lower() != 'y':
                break
    
    print()
    print("=" * 60)
    print("If you need to reset your PostgreSQL password, see:")
    print("FIX_DATABASE_PASSWORD.md")
    print("=" * 60)


if __name__ == "__main__":
    main()
