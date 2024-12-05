import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import configparser
from tcms_api import TCMS
from ReadCsv import ReadCsv


class Main:
    def __init__(self, root):
        self.rpc_client = self.initialize_rpc_client()
        self.root = root
        self.root.title("Importador de CSV")
        self.root.geometry("400x200")

        # Botón para seleccionar el archivo CSV
        self.import_button = tk.Button(self.root, text="Seleccionar CSV e Importar", command=self.start_processing)
        self.import_button.pack(pady=20)

        # Etiqueta para mostrar mensajes de estado
        self.status_label = tk.Label(self.root, text="", fg="pink")
        self.status_label.pack()

    def initialize_rpc_client(self):
        # Leer configuración desde tcms.conf
        config = configparser.ConfigParser()
        config.read("tcms.conf")  # Asegúrate de que el archivo esté en el mismo directorio o ajusta la ruta.

        try:
            url = config["tcms"]["url"]
            username = config["tcms"]["username"]
            password = config["tcms"]["password"]
        except KeyError as e:
            raise Exception(f"Falta la clave {e} en el archivo tcms.conf")

        # Inicializar el cliente TCMS
        return TCMS(url=url, username=username, password=password)

    def start_processing(self):
        # Mostrar cuadro de diálogo para seleccionar archivo CSV
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo.")
            return

        # Actualizar el mensaje de estado en la ventana principal
        self.status_label.config(text="Procesando archivo CSV, por favor espere...")

        # Usar un hilo separado para manejar la importación
        threading.Thread(target=self.import_csv_thread, args=(file_path,)).start()

    def import_csv_thread(self, file_path):
        try:
            # Leer y procesar el archivo CSV utilizando ReadCsv
            reader = ReadCsv()
            csv_data = reader.readCsv(file_path)

            # Omitir la primera línea (encabezado)
            csv_data = csv_data[1:] if len(csv_data) > 1 else []

            # Subir los datos a Kiwi TCMS
            for idx, row in enumerate(csv_data):
                print(f'row: {row}')
                try:
                    self.create_test_case(row)  # Pasa cada fila a create_test_case
                    print(f"Procesado exitosamente: {row}")
                except Exception as e:
                    print(f"Error al procesar la fila {idx + 1}: {e}")

            # Actualizar el mensaje de estado y mostrar cuadro de diálogo de éxito
            self.status_label.config(text="Archivo procesado con éxito.")
            self.on_import_success()

        except Exception as e:
            self.status_label.config(text="")
            messagebox.showerror("Error", f"Error al procesar el archivo CSV: {e}")

    def create_test_case(self, fields):
        # Dividir la línea en campos separados por comas
        # Mapear campos según tu archivo CSV
        summary = fields[0]  # RESUMEN(TITULO)
        steps = fields[1]    # PASOS
        expected_result = fields[2]  # EXPECTED RESULT
        notes = fields[3]  # NOTAS
        client_id = int(fields[4])  # ID CLIENTE
        priority_id = int(fields[5])  # ID PRIORIDAD
        author_id = int(fields[6])  # ID AUTOR
        print(f'steps: {steps} ')
        # Crear un caso de prueba en Kiwi TCMS usando la API
        self.rpc_client.exec.TestCase.create({
            'summary': summary,
            'text': f"**Pasos:**\n{steps}\n\n**Resultado Esperado:**\n{expected_result}\n\n",
            'notes': notes,
            'product': client_id,
            'priority': priority_id,
            'author': author_id,
            'case_status': 2,  # CONFIRMED
            'category': 4,  # Cambia si es necesario
        })

    def on_import_success(self):
        # Mostrar un cuadro de diálogo de éxito con un botón para redirigir
        if messagebox.showinfo("Importación Exitosa", "El archivo CSV se importó con éxito."):
            # Abrir la página web al aceptar
            webbrowser.open("https://kiwitcms.banana-software.com/cases/search/")


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()



# ID AUTOR: 2 -> bananaqa 3-> NOE 1-> AnonymousUser 4 -> LucasM 5 -> Ari
# PRIORITY: 5 BAJA A 1 MUY ALTA
# PRODUCT: 4 JACARANDA