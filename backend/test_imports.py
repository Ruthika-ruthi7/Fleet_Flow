#!/usr/bin/env python3
"""
Test script to check if all imports work correctly
"""

import os
import sys

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing imports...")
    
    print("1. Testing app creation...")
    from app import create_app
    
    print("2. Testing database...")
    from app import db
    
    print("3. Testing User model...")
    from app.models.user import User
    
    print("4. Testing Driver model...")
    from app.models.driver import Driver
    
    print("5. Testing Bus model...")
    from app.models.bus import Bus
    
    print("6. Testing Route model...")
    from app.models.route import Route
    
    print("7. Testing Student model...")
    from app.models.student import Student
    
    print("✅ All imports successful!")
    
    # Test app creation
    app = create_app()
    print("✅ App creation successful!")
    
    with app.app_context():
        print("✅ App context works!")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print("🎉 All tests passed! Ready to run quick_setup.py")
