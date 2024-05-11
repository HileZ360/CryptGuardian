# CryptGuardian

CryptGuardian is a user authentication and security management tool built with Python and Tkinter.

## Overview

CryptGuardian provides a graphical user interface (GUI) for user authentication, registration, password management, and login history viewing. It ensures secure access to a system by implementing cryptographic methods for password storage and validation.

## Features

- **User Authentication:** Users can log in securely using their username and password.
- **User Registration:** New users can register with a unique username and password.
- **Password Management:** Users can change their passwords, ensuring strong password complexity.
- **Login History:** CryptGuardian keeps track of user login history, including timestamps, IP addresses, and hardware identifiers.
- **Memory Usage Monitoring:** The program monitors memory usage to ensure efficient resource management.

## How it Works

1. **User Authentication:**
   - Users enter their username and password in the provided fields.
   - CryptGuardian verifies the entered credentials against stored user data in a JSON file.
   - If the credentials are correct, the user is granted access to the system.
   - Otherwise, an error message is displayed.

2. **User Registration:**
   - New users click the "Register" button and provide a unique username and password.
   - CryptGuardian checks the username availability and password complexity.
   - If the username is available and the password meets complexity requirements, the user is registered, and the credentials are stored securely in a JSON file.
   - Otherwise, appropriate error messages are displayed.

3. **Password Management:**
   - Users click the "Change Password" button and enter their current and new passwords.
   - CryptGuardian validates the current password, checks the complexity of the new password, and updates the password if all requirements are met.
   - The updated credentials are securely stored in the JSON file.

4. **Login History:**
   - Users can view their login history by clicking the "View Login History" button.
   - CryptGuardian retrieves the login history data from a JSON file and displays it in a formatted message box.

5. **Memory Usage Monitoring:**
   - CryptGuardian continuously monitors memory usage using the WMI (Windows Management Instrumentation) library.
   - It calculates the total memory and free memory available on the system.
   - The program then displays the used memory in megabytes (MB) in the welcome window.

## Requirements

- Python 3.x
- Tkinter (standard Python interface to the Tk GUI toolkit)
- Pillow (PIL Fork, Python Imaging Library)
- WMI (Windows Management Instrumentation)

## Usage

1. Clone the repository: `git clone https://github.com/HileZ360/CryptGuardian.git`
2. Navigate to the project directory: `cd CryptGuardian`
3. Run the application: `python main.py`
