# main.py

import tkinter as tk
from login import LoginWindow
from import_window import ImportWindow
from tcms_api import TCMS


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal inicialmente

    # Esta función se ejecuta cuando el login es exitoso
    def start_main_app(username, password):
        # Crear el cliente de la API y autenticarlo
        try:
            api_client = TCMS(url='https://kiwitcms.banana-software.com/xml-rpc/', username=username, password=password).exec
            print(api_client.__connection)
            # Cerrar la ventana de login
            login_window.destroy()
            # Mostrar la ventana principal y pasar el api_client
            root.deiconify()  # Mostrar la ventana principal
            ImportWindow(root, api_client)  # Pasar el api_client para usarlo en ImportWindow
            root.mainloop() # Ejecutar el bucle principal
        except Exception as e:
                print(f'Error al iniciar sesión: {e}')
                raise Exception()
        
    try:
        login_window = tk.Toplevel()
        LoginWindow(login_window, start_main_app)  # Pasar la función de callback

        # Ejecutar el bucle de eventos para la ventana de login
        login_window.mainloop()

    except Exception as e:
        print(f"Error inesperado: {e}")









