# 🎉 Welcome to **CryptGuardian** 🎉

**CryptGuardian** is a cutting-edge tool designed to ensure **user security and authentication** through a sleek and intuitive graphical interface. With robust features and a user-friendly design, it offers a seamless experience for both administrators and users.

## ✨ Overview ✨

### 🔐 Key Features
1. **Admin Panel**: 🛠
   - Administrators can **add and manage access keys** with specified start and end dates, ensuring controlled access and enhanced security.
2. **User Authentication**: 🛡
   - Users can securely **log in** with their username and password, which are securely hashed for maximum protection.
3. **User Registration**: 📝
   - New users can **register** by providing a unique username and a password that meets stringent security requirements.
4. **Access Key Verification**: 🔑
   - After logging in, users can verify access keys to check their validity and get relevant access information.
5. **System Information Display**: 💻
   - Users can view detailed **system information**, including CPU, memory, disk usage, and GPU details.
6. **Password Management**: 🔄
   - Users can **change their passwords** securely, ensuring ongoing protection of their accounts.
7. **Login History**: 📜
   - Users and administrators can **view login history** for auditing and security purposes.
8. **Brute Force Protection**: 🛡
   - Enhanced security measures to protect against brute force attacks.

## 🎨 How It Works 🎨

### 🛠 Admin Panel
- **Adding Access Keys**:
  - Administrators input key details, start date, end date, and access information.
  - The system **validates the input** and stores the keys in a JSON file.
  - This ensures **controlled access** and detailed monitoring of key usage.

### 🛡 User Authentication and Registration
- **Login Process**:
  - Users enter their credentials, which are checked against stored data using **hashed passwords** for security.
  - Successful login grants access, while incorrect credentials trigger appropriate error messages.
- **Registration Process**:
  - New users can register by providing a username and password.
  - Passwords are hashed before storage, ensuring **maximum security**.

### 🔑 Access Key Verification
- **Key Verification**:
  - Users input keys to check their validity against stored keys.
  - The system displays access status and relevant information, ensuring transparency and security.

### 💻 System Information Display
- **Viewing System Info**:
  - Users can access detailed system information including CPU model, core and thread count, memory usage, disk space, and GPU details.
  - This information helps in monitoring system performance and resources.

### 🔄 Password Management
- **Changing Password**:
  - Users can change their password by providing the old password and setting a new one.
  - The system ensures the new password meets security requirements and updates it securely.

### 📜 Login History
- **Viewing Login History**:
  - Users and administrators can view the login history to monitor access and detect any suspicious activity.

### 🛡 Brute Force Protection
- **Enhanced Security**:
  - The system includes measures to protect against brute force attacks, such as logging attempts and locking accounts after repeated failures.

### 🌐 GitHub Integration
- **Seamless Navigation**:
  - Users can navigate to the CryptGuardian GitHub repository for more resources, contributions, or feedback.
  - This integration fosters community involvement and continuous improvement.

## 💻 Technical Requirements 💻

- **Python 3.x**: Core programming language.
- **Flet Library**: For creating the graphical user interface.
- **psutil**: For gathering system information.
- **GPUtil**: For detailed GPU information.
- **bcrypt**: For secure password hashing.
- **JSON**: For data storage and manipulation.

## 🚀 Usage 🚀

1. **Clone the Repository**: `git clone https://github.com/HileZ360/CryptGuardian.git`
2. **Navigate to Project Directory**: `cd CryptGuardian`
3. **Run the Application**: `python main.py`
or use **pip install -r requirements.txt**

For detailed information and the source code, you can visit the [CryptGuardian GitHub repository](https://github.com/HileZ360/CryptGuardian).

## 🌟 Future Enhancements 🌟

Future enhancements could include extending the functionality to integrate with other systems, improving the user interface, and adding more detailed system monitoring capabilities.
