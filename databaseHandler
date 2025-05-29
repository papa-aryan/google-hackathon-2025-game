import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

SERVICE_ACCOUNT_KEY_PATH = os.path.join(os.path.dirname(__file__), 'hackathon2025db.json')

class FirestoreHandler:
    def __init__(self, service_account_key_path):
        self.db = None
        try:
            cred = credentials.Certificate(service_account_key_path)
            # Check if the app is already initialized to prevent re-initialization error
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
                print("Firebase app initialized successfully!")
            else:
                print("Firebase app already initialized.")
            self.db = firestore.client()
            print("Firestore client obtained.")
        except Exception as e:
            print(f"Error initializing Firebase or getting Firestore client: {e}")
            # Optionally, re-raise the exception or handle it as per application needs
            # For now, we'll let db be None and subsequent operations will likely fail,
            # which should be handled by the calling code or within each method.
            raise  # Re-raise the exception to signal failure to the caller

    def write_document(self, collection_name, document_id, data):
        """Writes or overwrites a document in a specified collection."""
        if not self.db:
            print("Firestore client not available. Cannot write document.")
            return False
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc_ref.set(data)
            print(f"Successfully wrote '{document_id}' to '{collection_name}'.")
            return True
        except Exception as e:
            print(f"Error writing to Firestore: {e}")
            return False

    def read_document(self, collection_name, document_id):
        """Reads a document from a specified collection."""
        if not self.db:
            print("Firestore client not available. Cannot read document.")
            return None
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc = doc_ref.get()
            if doc.exists:
                print(f"Successfully read '{document_id}':")
                print(f"  Document data: {doc.to_dict()}")
                return doc.to_dict()
            else:
                print(f"'{document_id}' does not exist in '{collection_name}'.")
                return None
        except Exception as e:
            print(f"Error reading from Firestore: {e}")
            return None

    def get_specific_field(self, collection_name, document_id, field_name):
        """Gets a specific field from a Firestore document."""
        if not self.db:
            print("Firestore client not available.")
            return None
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()
                if field_name in data:
                    print(f"Field '{field_name}': {data[field_name]}")
                    return data[field_name]
                else:
                    print(f"Field '{field_name}' not found in document '{document_id}'.")
            else:
                print(f"Document '{document_id}' does not exist.")
        except Exception as e:
            print(f"Error getting specific field: {e}")
        return None

    def change_specific_field(self, collection_name, document_id, field_to_change, new_value):
        """Changes a specific field in a Firestore document."""
        if not self.db:
            print("Firestore client not available.")
            return False
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc_ref.update({
                field_to_change: new_value
            })
            print(f"Successfully updated field '{field_to_change}' in document '{document_id}'.")
            return True
        except Exception as e:
            print(f"Error updating specific field: {e}")
            return False

    def add_new_field(self, collection_name, document_id, new_field_name, new_field_value):
        """Adds a new field to a Firestore document."""
        if not self.db:
            print("Firestore client not available.")
            return False
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc_ref.update({
                new_field_name: new_field_value
            })
            print(f"Successfully added field '{new_field_name}' to document '{document_id}'.")
            return True
        except Exception as e:
            print(f"Error adding new field: {e}")
            return False
        
    def signup_user(self, username, password): 
        """Adds a new user to the 'users' collection."""
        if not self.db:
            print("Firestore client not available. Cannot sign up user.")
            return False
        try:
            # Using username as document ID for simplicity, ensure usernames are unique.
            # Alternatively, use auto-generated IDs and store username as a field.
            user_ref = self.db.collection('users').document(username) # Changed: uses self.db
            # Check if user already exists
            if user_ref.get().exists:
                print(f"Username '{username}' already exists.")
                return False
            user_ref.set({
                'username': username,
                'password': password  # WARNING: Storing plain text password
            })
            print(f"User '{username}' signed up successfully.")
            return True
        except Exception as e:
            print(f"Error signing up user: {e}")
            return False
        
    def login_user(self, username, password): 
        """Checks if a user with the given username and password exists."""
        if not self.db:
            print("Firestore client not available. Cannot log in user.")
            return False
        try:
            user_ref = self.db.collection('users').document(username) # Changed: uses self.db
            doc = user_ref.get()
            if doc.exists:
                user_data = doc.to_dict()
                # WARNING: Comparing plain text password
                if user_data.get('password') == password:
                    print(f"User '{username}' logged in successfully.")
                    return True
                else:
                    print("Invalid password.")
                    return False
            else:
                print(f"Username '{username}' not found.")
                return False
        except Exception as e:
            print(f"Error logging in user: {e}")
            return False

if __name__ == "__main__":
    try:
        # Initialize the handler
        db_handler = FirestoreHandler(SERVICE_ACCOUNT_KEY_PATH)

        # Proceed only if db_handler.db is not None (i.e., initialization was successful)
        if db_handler.db:
            # Test: Write a document
            test_data_to_write = {
                'message': 'Hello from Python OOP Style!',
                'timestamp': firestore.firestore.SERVER_TIMESTAMP,  # Corrected path to SERVER_TIMESTAMP
                'version': 2.0
            }
            db_handler.write_document('test_collection', 'oop_document', test_data_to_write)

            # Test: Read the document
            db_handler.read_document('test_collection', 'oop_document')

            # Test: Get a specific field
            db_handler.get_specific_field('test_collection', 'oop_document', 'message')
            db_handler.get_specific_field('test_collection', 'oop_document', 'non_existent_field')


            # Test: Change a specific field
            db_handler.change_specific_field('test_collection', 'oop_document', 'message', 'Updated message from OOP!')
            db_handler.read_document('test_collection', 'oop_document') # Read again to see change

            # Test: Delete a specific field
            db_handler.change_specific_field('test_collection', 'oop_document', 'message', firestore.firestore.DELETE_FIELD)  # Delete the field
            db_handler.read_document('test_collection', 'oop_document') # Read again to see change

            # Test: Add a new field
            db_handler.add_new_field('test_collection', 'oop_document', 'status', 'active')
            db_handler.read_document('test_collection', 'oop_document') # Read again to see new field




            # Test: Signup a new user
            print("\n\n--- Testing User Signup ---")
            signup_success = db_handler.signup_user('testuser1', 'password123')
            if signup_success:
                print("Signup test successful for testuser1.")
            else:
                print("Signup test FAILED for testuser1.")
            
            # Try signing up the same user again (should fail)
            db_handler.signup_user('testuser1', 'password123')


            # Test: Login user
            print("\n--- Testing User Login ---")
            # Test successful login
            login_success = db_handler.login_user('testuser1', 'password123')
            if login_success:
                print("Login test successful for testuser1.")
            else:
                print("Login test FAILED for testuser1.")

            # Test login with wrong password
            db_handler.login_user('testuser1', 'wrongpassword')

            # Test login with non-existent user
            db_handler.login_user('nonexistentuser', 'password123')

        else:
            print("Firestore handler could not be initialized. Exiting tests.")

    except Exception as e:
        # This will catch the exception re-raised from __init__ if initialization fails
        print(f"An error occurred during script execution: {e}")