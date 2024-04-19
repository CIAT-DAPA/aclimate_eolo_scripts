import requests
from urllib.parse import urlencode
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

class GetDateGeoserver():

    def __init__(self, geo_url, workspace, store, user, passw, year=1700, month=1, day=1):
        self.geo_url = geo_url
        self.workspace = workspace
        self.store = store
        self.user = user
        self.passw = passw
        self.year = year
        self.month = month
        self.day = day

        self.start_date = self.get_coverage_url(self.geo_url, self.workspace, self.store, self.user, self.passw, self.year, self.month, self.day)


    def extract_date_from_xml(self, xml_content):
        # Convertir el contenido XML a una cadena de texto
        xml_string = xml_content.decode('utf-8')  # Decodificar bytes a cadena de texto

        # Buscar todas las fechas en el texto del XML usando expresiones regulares
        matches = re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z', xml_string)
        
        # Si hay al menos dos fechas encontradas, seleccionamos la segunda
        if len(matches) >= 2:
            full_date = matches[1]  # Segunda fecha encontrada
            
            # Obtener solo el año y el mes (2024-02)
            year_month = full_date[:7]
            
            # Convertir la cadena de fecha en un objeto de fecha
            date_obj = datetime.strptime(year_month, '%Y-%m')
            
            # Sumar un mes
            date_obj += relativedelta(months=1)
            
            # Formatear la nueva fecha
            new_year_month = date_obj.strftime('%Y-%m')
            
            return full_date, new_year_month
        else:
            return None, None

    def get_coverage_url(self, url_root, workspace, mosaic_name, geoserver_user, geoserver_password, year, month, day):
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
        
        return self.extract_date_from_xml(response.content)[1]


        

#get_coverage_url("https://geo.aclimate.org/geoserver/", "historical_climate_hn", "PREC", "scalderon", "Santi2711.", 1700, 1, 1)