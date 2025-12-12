#!/usr/bin/env python3
"""
Setup verification script for Fake Product Detection System.
Checks that all required components are properly configured.
"""
import os
import sys
from pathlib import Path


def check_directory_structure():
    """Verify all required directories exist."""
    required_dirs = [
        "backend",
        "backend/src",
        "backend/alembic",
        "frontend",
        "frontend/src",
        "models",
        "data",
        "tests",
        "temp_uploads",
        "logs"
    ]
    
    print("Checking directory structure...")
    missing = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing.append(dir_path)
            print(f"  ❌ Missing: {dir_path}")
        else:
            print(f"  ✓ Found: {dir_path}")
    
    return len(missing) == 0


def check_config_files():
    """Verify all required configuration files exist."""
    required_files = [
        ".env.example",
        ".gitignore",
        "docker-compose.yml",
        "README.md",
        "backend/requirements.txt",
        "backend/pytest.ini",
        "backend/alembic.ini",
        "backend/Dockerfile",
        "frontend/package.json",
        "frontend/tsconfig.json",
        "frontend/Dockerfile",
        "frontend/nginx.conf"
    ]
    
    print("\nChecking configuration files...")
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
            print(f"  ❌ Missing: {file_path}")
        else:
            print(f"  ✓ Found: {file_path}")
    
    return len(missing) == 0


def check_python_version():
    """Verify Python version is 3.9 or higher."""
    print("\nChecking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor}.{version.micro} (requires 3.9+)")
        return False


def check_git_repo():
    """Verify Git repository is initialized."""
    print("\nChecking Git repository...")
    if Path(".git").exists():
        print("  ✓ Git repository initialized")
        return True
    else:
        print("  ❌ Git repository not initialized")
        return False


def check_env_file():
    """Check if .env file exists (optional but recommended)."""
    print("\nChecking environment configuration...")
    if Path(".env").exists():
        print("  ✓ .env file exists")
        return True
    else:
        print("  ⚠ .env file not found (copy from .env.example)")
        return False


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Fake Product Detection System - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Directory Structure", check_directory_structure()),
        ("Configuration Files", check_config_files()),
        ("Python Version", check_python_version()),
        ("Git Repository", check_git_repo()),
    ]
    
    # Optional check
    env_exists = check_env_file()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    all_passed = all(result for _, result in checks)
    
    for name, result in checks:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    if not env_exists:
        print("⚠ WARNING: .env file not configured")
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ Setup verification complete!")
        print("\nNext steps:")
        print("1. Copy .env.example to .env and configure settings")
        print("2. Start Docker services: docker-compose up -d")
        print("3. Set up Python virtual environment: cd backend && python -m venv venv")
        print("4. Install dependencies: pip install -r requirements.txt")
        print("5. Run database migrations: alembic upgrade head")
        return 0
    else:
        print("\n❌ Setup verification failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
