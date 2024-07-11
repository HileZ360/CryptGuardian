CryptGuardian is a robust tool designed for user security and authentication through a graphical interface. Developed with Python and the Flet library, it allows users to log in, register, and manage access keys, providing a user-friendly interface for administrators and users alike.

Overview
CryptGuardian provides several key features:

Admin Panel: Administrators can add and manage access keys with specified start and end dates, ensuring controlled access.
User Authentication: Users can securely log in with their username and password, which are securely hashed.
User Registration: New users can register, providing a unique username and a password that meets security requirements.
Access Key Verification: After logging in, users can verify access keys to check their validity and get relevant access information.
System Information Display: Users can view detailed system information, including CPU, memory, disk usage, and GPU details.
How It Works
Admin Panel:

Administrators add access keys by entering key details, start date, end date, and access information.
The system validates the input and stores the keys in a JSON file.
User Authentication and Registration:

Users enter their credentials, which are checked against stored data using hashed passwords for security.
New users can register by providing a username and password, which is hashed and stored securely.
Access Key Verification:

Users can input keys to check their validity against stored keys and view associated access information.
GitHub Integration:

Users can navigate to the CryptGuardian GitHub repository for more resources, contributions, or feedback.
Technical Requirements
Python 3.x
Flet Library: For GUI creation
psutil: For system information
GPUtil: For GPU details
bcrypt: For password hashing
JSON: For data storage and manipulation
Usage
Clone the Repository: git clone https://github.com/HileZ360/CryptGuardian.git
Navigate to Project Directory: cd CryptGuardian
Run the Application: python main.py
