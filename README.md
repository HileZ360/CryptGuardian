# 🎉 Welcome to **CryptGuardian** 🎉

**CryptGuardian** is a comprehensive security-focused application providing a user-friendly **GUI** for authentication, key management, and system information display. Below is an in-depth overview of its functionality, technical details, and future enhancements.

---

## 🔒 Project Overview

### 🛡 Key Features

1. **User Authentication**: Secure login with **bcrypt** password hashing, plus brute force protection with account lockouts.  
2. **User Registration**: Enforces unique usernames and ensures basic password requirements.  
3. **Admin Panel**: Add/manage **access keys** with start/end dates and access info.  
4. **System Info**: Retrieve CPU, memory, disk, and GPU stats (via `psutil` and `GPUtil`).  
5. **Password Management**: Users can securely change their passwords by confirming their old one.  
6. **Login History**: Stores successful/failed attempts in a JSON log.  
7. **Brute Force Protection**: Tracks login failures and temporarily locks accounts after excessive attempts.

### 🏗 Project Structure

- **domain/models.py**  
  Defines data models for CPU, Memory, Disk, GPU, SystemInfo, and User.  

- **domain/security.py**  
  Handles password hashing/checking, user authentication, brute force prevention.  

- **domain/services.py**  
  Orchestrates system info retrieval, user credential loading/saving, and password changes.  

- **infrastructure/utils.py**  
  Provides JSON file I/O utilities (load, save) with basic validation and error handling.  

- **presentation/gui.py**  
  Implements the main GUI flow (login, registration, system info display, key verification).  

- **admin.py**  
  A separate admin interface allowing administrators to add and manage access keys.  

- **main.py**  
  Entry point for launching CryptGuardian’s main user interface (login, system info, key verification).  

### ⚙ How It Works

1. **Authentication & Registration**  
   - Passwords are stored only after being **bcrypt-hashed**.  
   - On login, the system checks credentials and logs any failures.  
2. **Key Verification**  
   - Users submit a key; the system checks `data/keys.json` and displays validity info.  
3. **System Information**  
   - Displays real-time CPU, memory, disk usage, and GPU details.  
4. **Password Reset**  
   - Validates old password, checks new password length, then replaces the stored hash.  
5. **Brute Force Protection**  
   - Maintains a global dictionary to count failed logins. Locks accounts after multiple failures until a timeout expires.  

### 📝 Data Storage

- **user_credentials.json**: Stores usernames and hashed passwords.  
- **data/keys.json**: Maintains access keys.  
- **login_history.json**: Contains a record of login attempts.  

While JSON files are easy for smaller projects, transitioning to a robust database with encryption is recommended for production.

---

## 🚀 Getting Started

### 📦 requirements.txt

```txt
bcrypt>=3.2.0
flet>=0.24.0
psutil>=5.9.4
GPUtil>=1.4.0
pytest>=7.2.0
```
 **Clone the Repository**  
   ```bash
   git clone https://github.com/HileZ360/CryptGuardian.git
