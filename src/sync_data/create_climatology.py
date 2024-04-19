import numpy as np
import rasterio
import os
from rasterio.io import MemoryFile
import requests
from urllib.parse import urlencode


class CreateClimatology():

    def __init__(self, url_root, workspace, mosaic_name, 
                 geoserver_user, geoserver_password, climatology_outp,
                 array_months, year_start=1981, day=1):
        
        self.url_root = url_root
        self.workspace = workspace
        self.mosaic_name = mosaic_name
        self.geoserver_user = geoserver_user
        self.geoserver_password = geoserver_password
        self.year_start = year_start
        self.day = day
        self.climatology_outp = climatology_outp
        self.array_months = array_months

    def download_and_average_rasters(self, url_root, workspace, mosaic_name, geoserver_user, geoserver_password, year_start, month, day, climatology_outp):
        all_raster_arrays = []
        spatial_info = None
        
        year = year_start
        while True:
            base_url = f"{url_root}{workspace}/ows?"
            params = {
                "service": "WCS",
                "request": "GetCoverage",
                "version": "2.0.1",
                "coverageId": mosaic_name,
                "format": "image/geotiff",
                "subset": f"Time(\"{year}-{month:02d}-{day:02d}T00:00:00.000Z\")"
            }
            url = base_url + urlencode(params)
            response = requests.get(url, auth=(geoserver_user, geoserver_password))
            # Si la respuesta es 404, no se encontró nada, sal del bucle
            if response.status_code == 404:
                break
            
            # Abre el contenido de la respuesta con rasterio
            with MemoryFile(response.content) as memfile:
                with memfile.open() as raster:
                    raster_array = raster.read(1)
                    all_raster_arrays.append(raster_array)
                    spatial_info = raster.profile  # Obtén la información espacial aquí dentro
            
            year += 1
        
        if not all_raster_arrays:
            print("No se encontraron rasters para descargar.")
            return
        
        # Calcular el promedio de los rasters
        average_array = np.mean(all_raster_arrays, axis=0)
        
        # Guardar el raster promedio como un nuevo archivo GeoTIFF
        file_name = f"{mosaic_name}_2000{month:02d}.tif"
        output_file = os.path.join(climatology_outp, file_name)
        with rasterio.open(output_file, 'w', **spatial_info) as dst:
            dst.write(average_array, 1)


    def main(self):

        for month in self.array_months:

            self.download_and_average_rasters(self.url_root, self.workspace, self.mosaic_name,
                                              self.geoserver_user, self.geoserver_password, self.year_start,
                                              month, self.day, self.climatology_outp)


# download_and_average_rasters("https://geo.aclimate.org/geoserver/", 
#                              "historical_climate_hn", 
#                              "PREC", "scalderon", 
#                              "Santi2711.", 2023,2024, 1,1,
#                              "D:\Code\download_historical_data\geo")


