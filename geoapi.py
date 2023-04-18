import requests
from config import GEO_API_ESPANIA_KEY
import time
import sys

"""This module contains functions to interact with GeoAPI España (https://geoapi.es)"""

endpoint  = "http://apiv1.geoapi.es"
key = GEO_API_ESPANIA_KEY
type = "JSON"
sandbox = "0"

def codigo_comunidad(comunidad):
    """Devuelve el código de una comunidad autónoma"""

    comunidades = get_comunidades()
    for c in comunidades["data"]:
        if c["COM"] == comunidad.upper():
            return c["CCOM"]
        
def codigo_provincia(provincia):
    """Devuelve el código de una provincia"""

    provincias = get_provincias()
    for p in provincias["data"]:
        if p["PRO"] == provincia.upper():
            return p["CPRO"]



def get_comunidades():
    """Devuelve todas las comunidades autónomas de España"""

    url = "/comunidades"
    request = f"{endpoint}{url}?key={key}&sandbox={sandbox}"
    return requests.get(request).json()


def get_provincias(comunidad=""):
    """Devuelve todas las provincias de una comunidad autónoma
    o de España si no se especifica comunidad"""

    url = f"/provincias"
    request = f"{endpoint}{url}?key={key}&sandbox={sandbox}"
    if comunidad != "":
        ccom = codigo_comunidad(comunidad)
        request += f"&CCOM={ccom}"
    return requests.get(request).json()


def get_municipios(provincia):
    """Devuelve todas las municipios de una provincia"""

    url = f"/municipios"
    request = f"{endpoint}{url}?key={key}&sandbox={sandbox}"
    cpro = codigo_provincia(provincia)
    request += f"&CPRO={cpro}"
    return requests.get(request).json()



# comunidades = get_municipios("comunidad de madrid")
# pretty_json = json.dumps(comunidades, indent=4, ensure_ascii=False)
# print(pretty_json)

# print(f"Un total de {len(comunidades['data'])} municipios")
print("hola")
total = 38
bar_len = 30
for i in range(total):
    time.sleep(0.5)
    progress_percentage = int((i / (total-1) * 100))
    bar_items = int(progress_percentage / (100/bar_len))
    progress = "[" + "█" * bar_items + " " * (bar_len-bar_items) + "] " +  str(progress_percentage) + "%"
    sys.stdout.write("\r" + progress)


print("\nadios")