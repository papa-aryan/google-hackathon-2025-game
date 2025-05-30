#!/usr/bin/env python3
"""
Test script to verify authentication system works
"""

from databaseHandler import FirestoreHandler, SERVICE_ACCOUNT_KEY_PATH

def test_authentication():
    """Test basic authentication functionality"""
    print("Testing authentication system...")
    
    try:
        # Initialize database handler
        db_handler = FirestoreHandler(SERVICE_ACCOUNT_KEY_PATH)
        print("✓ Database handler initialized successfully")
        
        # Test data
        test_username = "test_user_123"
        test_password = "test_password"
        
        # Test signup
        print(f"\nTesting signup for user: {test_username}")
        signup_result = db_handler.signup_user(test_username, test_password)
        if signup_result:
            print("✓ Signup successful")
        else:
            print("✗ Signup failed (user may already exist)")
        
        # Test login
        print(f"\nTesting login for user: {test_username}")
        login_result = db_handler.login_user(test_username, test_password)
        if login_result:
            print("✓ Login successful")
        else:
            print("✗ Login failed")
        
        # Test invalid login
        print(f"\nTesting invalid login...")
        invalid_login_result = db_handler.login_user(test_username, "wrong_password")
        if not invalid_login_result:
            print("✓ Invalid login correctly rejected")
        else:
            print("✗ Invalid login incorrectly accepted")
            
        print("\n" + "="*50)
        print("Authentication system test completed!")
        print("The authentication system is properly connected to the database.")
        
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        print("Check that the Firebase credentials file exists and is valid.")

if __name__ == "__main__":
    test_authentication()
