import csv

class ReadCsv():
    def readCsv(self, pathOfCsv):
        output = []
        with open(pathOfCsv, mode='r', encoding='utf-8', newline='') as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar='"')
            for idx, row in enumerate(reader):
                if not row:  # Ignorar filas vacías
                    print(f"Fila {idx + 1} está vacía, se omitirá.")
                    continue
                print(f"Fila {idx + 1} leída: {row}")  # Depuración
                output.append(row)
        return output

