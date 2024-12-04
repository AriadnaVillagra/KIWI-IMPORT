import os
import threading
import configparser
from tcms_api import TCMS
from ReadCsv import ReadCsv
import tkinter as tk
from tkinter import filedialog, messagebox

class Main:
    def __init__(self, root):
        self.rpc_client = self.initialize_rpc_client()
        self.root = root
        self.root.title("Importador de CSV")
        self.root.geometry("300x150")
        
        # Botón para seleccionar el archivo CSV
        self.import_button = tk.Button(self.root, text="Importar CSV", command=self.import_csv)
        self.import_button.pack(pady=20)

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

    def import_csv(self):
        # Abrir el cuadro de diálogo para seleccionar el archivo CSV
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        
        if file_path:
            # Mostrar un mensaje indicando que se está importando
            messagebox.showinfo("En Progreso", "Importación en progreso...")
            
            # Usar un hilo separado para manejar la importación sin bloquear la GUI
            threading.Thread(target=self.import_csv_thread, args=(file_path,)).start()

    def import_csv_thread(self, file_path):
        # Leer y procesar el archivo CSV utilizando ReadCsv
        reader = ReadCsv()
        csv_data = reader.readCsv(file_path)

        # Omitir la primera línea (encabezado)
        csv_data = csv_data[1:] if len(csv_data) > 1 else []

        # Subir los datos a Kiwi TCMS
        for idx, row in enumerate(csv_data):
            try:
                self.create_test_case(row[0])  # Pasa cada fila a create_test_case
                print(f"Procesado exitosamente: {row}")
            except Exception as e:
                print(f"Error al procesar la fila {idx + 1}: {e}")

        # Mostrar mensaje de éxito
        self.on_import_success()

    def create_test_case(self, test_case_data):
        # Dividir la línea en campos separados por comas
        fields = test_case_data.split(',')

        # Mapear campos según tu archivo CSV
        summary = fields[0]  # RESUMEN(TITULO)
        steps = fields[1]    # PASOS
        expected_result = fields[2]  # EXPECTED RESULT
        notes = fields[3]  # NOTAS
        client_id = int(fields[4])  # ID CLIENTE
        priority_id = int(fields[5])  # ID PRIORIDAD
        author_id = int(fields[6])  # ID AUTOR
        category = int(fields[6]) #ID CATEGORIA
        

        # Crear un caso de prueba en Kiwi TCMS usando la API
        self.rpc_client.exec.TestCase.create({
            'summary': summary,
            'text': f"**Steps:**\n{steps}\n\n**Expected Result:**\n{expected_result}\n\n**Notes:**\n{notes}",
            'product': client_id,
            'priority': priority_id,
            'author': author_id,
            'case_status': 2,  # CONFIRMED poner los que hay
            'category': 4 # poner las categorias que hay
        })

    def on_import_success(self):
        # Mostrar un cuadro de diálogo de éxito
        messagebox.showinfo("Importación Exitosa", "El archivo CSV se importó con éxito.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
# ID AUTOR: 2 -> bananaqa 3-> NOE
# PRIORITY: 5 BAJA A 1 MUY ALTA