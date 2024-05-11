import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import json
from datetime import datetime
import hashlib
import wmi
import os
import socket
import re

class BackgroundManager:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root, width=300, height=200)
        self.canvas.pack()
        self.background_image = None

    def set_background_image(self, image_path):
        if self.background_image:
            self.canvas.delete(self.background_image)
        image = Image.open(image_path)
        image.thumbnail((300, 200))
        photo = ImageTk.PhotoImage(image)
        self.background_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

    def clear_background_image(self):
        if self.background_image:
            self.canvas.delete(self.background_image)

class UserAuthenticationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CryptGuardian")
        self.root.geometry("400x420")
        self.root.resizable(False, False)
        self.background_manager = BackgroundManager(root)
        self.background_manager.set_background_image("background_image.jpg")
        self.create_login_gui()

    def create_login_gui(self):
        self.frame = ttk.Frame(self.root, borderwidth=2, relief="groove", padding=(20, 20))
        self.frame.pack(expand=True, side=tk.LEFT)
        self.label_username = ttk.Label(self.frame, text="Username:", font=("Helvetica", 12, "bold"))
        self.label_username.grid(row=0, column=0, sticky="w")
        self.entry_username = ttk.Entry(self.frame, font=("Helvetica", 12))
        self.entry_username.grid(row=0, column=1, sticky="ew")
        self.label_password = ttk.Label(self.frame, text="Password:", font=("Helvetica", 12, "bold"))
        self.label_password.grid(row=1, column=0, sticky="w")
        self.entry_password = ttk.Entry(self.frame, show="*", font=("Helvetica", 12))
        self.entry_password.grid(row=1, column=1, sticky="ew")
        self.frame.columnconfigure(1, weight=1)
        self.style = ttk.Style()
        self.style.configure("BlueGradient.TButton", background="#4A90E2", foreground="black", borderwidth=0,
                             font=("Helvetica", 12))
        self.button_login = ttk.Button(self.frame, text="Login", width=10, style="BlueGradient.TButton", command=self.login)
        self.button_login.grid(row=2, column=0, pady=10, padx=(0, 5), sticky="ew")
        self.style.configure("RedGradient.TButton", background="#E74C3C", foreground="black", borderwidth=0,
                             font=("Helvetica", 12))
        self.button_register = ttk.Button(self.frame, text="Register", width=10, style="RedGradient.TButton", command=self.register)
        self.button_register.grid(row=2, column=1, pady=10, padx=(5, 0), sticky="ew")
        self.button_change_password = ttk.Button(self.frame, text="Change Password", width=15, command=self.change_password)
        self.button_change_password.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        self.button_view_login_history = ttk.Button(self.frame, text="View Login History", width=15, command=self.view_login_history)
        self.button_view_login_history.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")


    def login(self):
        u, p = self.entry_username.get(), self.entry_password.get()
        if u and p:
            if self.authenticate(u, p):
                self.root.withdraw()
                welcome_window = WelcomeWindow(self.root, u, self.show_main_window)
            else:
                messagebox.showerror("Error", "Incorrect username or password")
        else:
            messagebox.showerror("Error", "Please enter username and password")

    def register(self):
        self.root.withdraw()
        register_window = tk.Toplevel(self.root)
        register_window.title("Register")
        frame_register = ttk.Frame(register_window, borderwidth=2, relief="groove", padding=(20, 20))
        frame_register.pack(expand=True, side=tk.LEFT)
        label_username = ttk.Label(frame_register, text="Username:", font=("Helvetica", 12, "bold"))
        label_username.grid(row=0, column=0, sticky="w")
        entry_username = ttk.Entry(frame_register, font=("Helvetica", 12))
        entry_username.grid(row=0, column=1, sticky="ew")
        label_password = ttk.Label(frame_register, text="Password:", font=("Helvetica", 12, "bold"))
        label_password.grid(row=1, column=0, sticky="w")
        entry_password = ttk.Entry(frame_register, show="*", font=("Helvetica", 12))
        entry_password.grid(row=1, column=1, sticky="ew")
        button_register = ttk.Button(frame_register, text="Register", width=15, style="RedGradient.TButton",
                                     command=lambda: self.register_user(entry_username.get(), entry_password.get(), register_window))
        button_register.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        button_show_tips = ttk.Button(frame_register, text="Show Password Tips", width=15, command=self.show_password_tips)
        button_show_tips.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        register_window.protocol("WM_DELETE_WINDOW", lambda: register_window.destroy() or self.show_main_window())

    def show_password_tips(self):
        messagebox.showinfo("Password Tips", "Choose a password that is at least 6 characters long and includes special characters.")

    def change_password(self):
        u = simpledialog.askstring("Change Password", "Enter your username:")
        if u and self.is_username_exists(u):
            old_password = simpledialog.askstring("Change Password", "Enter your old password:")
            if old_password:
                if self.authenticate(u, old_password):
                    new_password = simpledialog.askstring("Change Password", "Enter your new password:")
                    if new_password:
                        if not self.validate_password_complexity(new_password):
                            messagebox.showerror("Error", "Password must contain at least 6 characters and include special characters")
                        else:
                            if not os.path.exists("user_credentials.json"):
                                messagebox.showerror("Error", "User credentials file not found")
                            else:
                                with open("user_credentials.json", "r+") as f:
                                    data = json.load(f)
                                    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                                    for user in data["users"]:
                                        if user["username"] == u:
                                            user["password"] = hashed_password
                                            break
                                    f.seek(0)
                                    json.dump(data, f, indent=4)
                                    messagebox.showinfo("Success", "Password changed successfully!")
                else:
                    messagebox.showerror("Error", "Incorrect old password")
            else:
                messagebox.showerror("Error", "Old password not provided")
        else:
            messagebox.showerror("Error", "Username does not exist" if u else "Username not provided")

    def view_login_history(self):
        u = simpledialog.askstring("View Login History", "Enter your username:")
        if u and self.is_username_exists(u):
            p = simpledialog.askstring("View Login History", f"Enter password for user {u}:")
            if p:
                if self.authenticate(u, p):
                    if not os.path.exists("login_history.json"):
                        messagebox.showerror("Error", "Login history file not found")
                    else:
                        with open("login_history.json", "r") as f:
                            data = json.load(f)
                            if u in data:
                                lh = "\n\n".join([f"Date/Time: {e.get('datetime', '')}\nIP Address: {e.get('ip_address', '')}\nHWID: {e.get('hwid', '')}"
                                                  for e in data[u]])
                                messagebox.showinfo("Login History", f"Login history for {u}:\n\n{lh}")
                            else:
                                messagebox.showinfo("Login History", f"No login history found for {u}")
                else:
                    messagebox.showerror("Error", "Incorrect password")
            else:
                messagebox.showerror("Error", "Password not provided")
        else:
            messagebox.showerror("Error", "Username does not exist" if u else "Username not provided")

    def register_user(self, u, p, w):
        if len(p) < 6 or not self.validate_password_complexity(p):
            messagebox.showerror("Error", "Password must contain at least 6 characters and include special characters")
        else:
            if self.is_username_exists(u):
                messagebox.showerror("Error", "Username already exists")
            else:
                with open("user_credentials.json", "r+") as f:
                    data = json.load(f)
                    hashed_password = hashlib.sha256(p.encode()).hexdigest()
                    data["users"].append({"username": u, "password": hashed_password})
                    f.seek(0)
                    json.dump(data, f, indent=4)
                messagebox.showinfo("Success", "User registered successfully!")
                w.withdraw()
                self.show_main_window()

    def authenticate(self, u, p):
        if not os.path.exists("user_credentials.json"):
            return False
        with open("user_credentials.json", "r") as f:
            data = json.load(f)
            for user in data["users"]:
                if user["username"] == u and user["password"] == hashlib.sha256(p.encode()).hexdigest():
                    self.log_login_history(u)
                    return True
        return False

    def is_username_exists(self, u):
        if not os.path.exists("user_credentials.json"):
            return False
        with open("user_credentials.json", "r") as f:
            data = json.load(f)
            for user in data["users"]:
                if user["username"] == u:
                    return True
        return False

    def log_login_history(self, u):
        ip_address = self.get_ip_address()
        if not os.path.exists("login_history.json"):
            with open("login_history.json", "w") as f:
                json.dump({}, f)
        with open("login_history.json", "r+") as f:
            data = json.load(f)
            if u in data:
                data[u].append({"datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "ip_address": ip_address,
                                "hwid": self.get_hwid()})
            else:
                data[u] = [{"datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "ip_address": ip_address,
                            "hwid": self.get_hwid()}]
            f.seek(0)
            json.dump(data, f, indent=4)

    def get_ip_address(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address

    def get_hwid(self):
        c = wmi.WMI()
        for item in c.Win32_OperatingSystem():
            return hashlib.sha256(item.SerialNumber.encode()).hexdigest()

    def validate_password_complexity(self, p):
        return len(p) >= 6 and re.search(r'[!@#$%^&*()_+{}|:"<>?`~=\[\];\',./-]', p)

    def show_main_window(self):
        self.root.deiconify()

class WelcomeWindow:
    def __init__(self, parent, u, on_logout_callback):
        self.parent = parent
        self.root = tk.Toplevel(parent)
        self.root.title("Welcome")
        self.frame = ttk.Frame(self.root, borderwidth=2, relief="groove", padding=(20, 20))
        self.frame.pack(expand=True)
        self.label_welcome = ttk.Label(self.frame, text=f"Welcome, {u}!", font=("Helvetica", 16, "bold"))
        self.label_welcome.pack()
        self.label_ram_usage = ttk.Label(self.frame, text="", font=("Helvetica", 12))
        self.label_ram_usage.pack()
        self.update_ram_usage()
        self.button_logout = ttk.Button(self.frame, text="Logout", command=self.on_logout)
        self.button_logout.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.on_logout)
        self.on_logout_callback = on_logout_callback

    def on_logout(self):
        self.root.destroy()
        self.on_logout_callback()

    def update_ram_usage(self):
        ram_usage = self.get_ram_usage()
        self.label_ram_usage.config(text=f"RAM Usage: {ram_usage} MB")
        self.root.after(1000, self.update_ram_usage)

    def get_ram_usage(self):
        c = wmi.WMI()
        total_memory, free_memory = 0, 0
        for os in c.Win32_OperatingSystem():
            total_memory = int(os.TotalVisibleMemorySize) // (1024 ** 2)
            free_memory = int(os.FreePhysicalMemory) // (1024 ** 2)
        used_memory = total_memory - free_memory
        return used_memory

def main():
    root = tk.Tk()
    app = UserAuthenticationGUI(root)
    root.mainloop()
