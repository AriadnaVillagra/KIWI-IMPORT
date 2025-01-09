# login.py

import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")
        self.on_success = on_success  # Callback para manejar el login exitoso

        # Etiquetas y campos de texto
        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Botón de login
        tk.Button(
            self.root,
            text="Login",
            command=self.verify_login
        ).pack(pady=20)

    def verify_login(self):
        # Obtener las credenciales ingresadas
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            # Si las credenciales son correctas, llamar a on_success (pasar las credenciales)
            try:
                self.on_success(username, password)
            except:
                messagebox.showerror("Login Fallido", "Por favor ingrese un nombre de usuario y contraseña válidos.")
            
        else:
            messagebox.showerror("Login Fallido", "Por favor ingrese un nombre de usuario y contraseña válidos.")



