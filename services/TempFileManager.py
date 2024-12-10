import tempfile
import os

class TempFileManager:
    def __init__(self):
        self.temp_file = None

    def create_temp_file(self, data):
        """Crea un archivo temporal y escribe los datos proporcionados."""
        # Si ya existe un archivo temporal, elimínalo primero
        if self.temp_file and not self.temp_file.closed:
            self.delete_temp_file()
        
        # Crear un nuevo archivo temporal
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.tmp')
        self.temp_file.write(data)
        self.temp_file.flush()  # Asegura que los datos se escriben en disco
        #print(f"Archivo temporal creado en: {self.temp_file.name}")

    def read_temp_file(self):
        """Lee los datos almacenados en el archivo temporal."""
        if not self.temp_file or self.temp_file.closed:
            raise ValueError("El archivo temporal no existe o está cerrado.")

        with open(self.temp_file.name, 'r') as f:
            data = f.read()
            #print(f"Datos leídos del archivo temporal: {data}")
            return data

    def delete_temp_file(self):
        """Elimina el archivo temporal."""
        if self.temp_file and not self.temp_file.closed:
            try:
                os.unlink(self.temp_file.name)  # Elimina el archivo del sistema
                print(f"Archivo temporal eliminado: {self.temp_file.name}")
            except FileNotFoundError:
                print("El archivo ya no existe.")
            finally:
                self.temp_file.close()
    
    def temp_file_exists(self):
        """Verifica si el archivo temporal existe."""
        if self.temp_file and os.path.exists(self.temp_file.name):
            return True
        return False