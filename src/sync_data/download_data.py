import os
import re
import requests
from datetime import datetime, timedelta

class DownloadData():

    def __init__(self, base_url, destination_directory, file_name, start_date, target_name):
        self.start_date = start_date
        self.base_url = base_url
        self.destination_directory = destination_directory
        self.file_name = file_name
        self.target_name = target_name
        self.months = []



    def get_unique_months_in_folder(self, folder_path):
        # Expresión regular para buscar archivos con el formato "xxxx_YYYYMM.tif"
        pattern = re.compile(r'(\d{6})\D*\.tif')

        # Lista para almacenar los meses encontrados
        unique_months = []

        # Obtener todos los archivos en la carpeta
        files = os.listdir(folder_path)

        # Filtrar archivos que coincidan con el formato esperado y extraer los meses
        for file_name in files:
            match = pattern.search(file_name)
            if match:
                month = int(match.group(1)[-2:])
                if month not in unique_months:
                    unique_months.append(month)

        # Ordenar la lista de meses
        unique_months.sort()

        return unique_months



    def exist_tif(self, path, name):

        for file in os.listdir(path):
            if file.endswith(".tif") and name in file:
                return True

        return False


    def rename_files(self, directory, target_name, file_name):
        for filename in os.listdir(directory):
            if filename.endswith(".tif"):
                if target_name in filename:
                    year = filename.split(target_name)[1].split(".")[1]
                    month = filename.split(target_name)[1].split(".")[2]
                    new_filename = f"{file_name}_{year+month}.tif"
                    os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
                    print(f"Renamed {filename} to {new_filename}")


    def download_CHIRPS_data(self, base_url, destination_directory, start_date):
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
        
        current_date = datetime.strptime(start_date, "%Y-%m")
        
        while True:

            filename = f"{self.target_name}.{current_date.year:04d}.{current_date.month:02d}.tif"
            url = base_url + filename
            
            print(f"Downloading {filename}...")
            response = requests.get(url)
            

            if response.status_code == 404:
                print(f"Error 404: {filename} not found. Stopping downloads.")
                break

            filepath = os.path.join(destination_directory, filename)
            with open(filepath, 'wb') as file:
                file.write(response.content)
                
            print(f"{filename} downloaded successfully.")

            next_month = current_date.replace(day=28) + timedelta(days=4)  
            current_date = next_month.replace(day=1) 


    def main(self):

        self.download_CHIRPS_data(self.base_url, self.destination_directory, self.start_date)

        if self.exist_tif(self.destination_directory, self.target_name):
            self.rename_files(self.destination_directory, self.target_name, self.file_name)

            self.months = self.get_unique_months_in_folder(self.destination_directory)
