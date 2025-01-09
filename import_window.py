import webbrowser
from ReadCsv import ReadCsv
import threading
from tkinter import messagebox
from tkinter import filedialog
import tkinter as tk


class ImportWindow():
    def __init__(self, root, api_client):
        self.root = root
        self.root.title("Importador de CSV")
        self.root.geometry("400x200")
        self.api_client = api_client  # Guardamos el cliente de la API

        # Botón para seleccionar el archivo CSV
        self.import_button = tk.Button(self.root, text="Seleccionar CSV e Importar", command=self.start_processing)
        self.import_button.pack(pady=20)

        # Etiqueta para mostrar mensajes de estado
        self.status_label = tk.Label(self.root, text="", fg="pink")
        self.status_label.pack()

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
        summary = fields[0]  # RESUMEN(TITULO)
        steps = fields[1]    # PASOS
        expected_result = fields[2]  # EXPECTED RESULT
        notes = fields[3]  # NOTAS
        client_id = int(fields[4])  # ID CLIENTE
        priority_id = int(fields[5])  # ID PRIORIDAD
        author_id = int(fields[6])  # ID AUTOR

        self.api_client.TestCase.create({
            'summary': summary,
            'text': f"**Pasos:**\n{steps}\n\n**Resultado Esperado:**\n{expected_result}\n\n",
            'notes': notes,
            'product': client_id,
            'priority': priority_id,
            'author': author_id,
            'case_status': 2,
            'category': 4,
        })

    def on_import_success(self):
        if messagebox.showinfo("Importación Exitosa", "El archivo CSV se importó con éxito."):
            webbrowser.open("https://kiwitcms.banana-software.com/cases/search/")
            
            
# ID AUTOR: 2 -> bananaqa 3-> NOE 1-> AnonymousUser 4 -> LucasM 5 -> Ari
# PRIORITY: 5 BAJA A 1 MUY ALTA
# PRODUCT: 4 JACARANDA