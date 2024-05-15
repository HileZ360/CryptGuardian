# CryptGuardian by HileZ (https://t.me/h1lez)

CryptGuardian is a user authentication and access management tool created with Python and the Flet GUI library.

Overview:

CryptGuardian offers a user-friendly interface for administrators to manage access keys and for users to log in, register, and verify access using provided keys. It ensures secure access to resources by implementing cryptographic hashing for password storage and validation.

Features:

- Admin Panel: Allows administrators to add access keys with specified start and end dates.
- User Authentication: Users can securely log in using their username and password.
- User Registration: New users can register with a unique username and password.
- Access Key Verification: Users can enter keys to check for access validity.
- GitHub Integration: Provides a button to navigate users to the GitHub repository for CryptGuardian.

How it Works:

1. Admin Panel:
   - Administrators access the admin panel to add new access keys.
   - They input the key, start date, end date, and access information.
   - The program validates the input and adds the key to the list of keys stored in a JSON file.

2. User Authentication and Registration:
   - Users enter their username and password in the provided fields.
   - CryptGuardian verifies the credentials against stored user data, utilizing hashed passwords for security.
   - If the credentials are correct, users are granted access; otherwise, appropriate error messages are displayed.
   - New users register by providing a unique username and a password meeting length requirements.
   - Passwords are hashed before storage, ensuring security.

3. Access Key Verification:
   - After logging in, users can input access keys to check for validity.
   - The program compares the entered key against stored keys and displays access status and information accordingly.

4. GitHub Integration:
   - Users can navigate to the GitHub repository for CryptGuardian using a provided button.
   - This integration allows users to access additional resources, contribute to the project, or provide feedback.

Requirements:

- Python 3.x
- Flet (Python library for creating GUI applications)
- hashlib (Python library for cryptographic hashing)
- datetime (Python library for working with dates and times)
- json (Python library for JSON manipulation)

Usage:

1. Clone the repository: git clone https://github.com/HileZ360/CryptGuardian.git
2. Navigate to the project directory: cd CryptGuardian
3. Run the application: python main.py
