import tkinter as tk
from gui import UserAuthenticationGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = UserAuthenticationGUI(root)
    root.mainloop()
