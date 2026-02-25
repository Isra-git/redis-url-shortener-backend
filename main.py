import os
import random 
import string
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse 

# Para conectar backend y Frontend 
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
import redis
from dotenv import load_dotenv


# cargar variables de entorno
load_dotenv()

# inicializar la app
app = FastAPI()


""" 
Configuramos CORS 
"""
origins = [
    "http://localhost:5173" # Puerto por defecto vite
    "*" # permite que se conecten desde
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

""" 
Fin Configuracion CORS
"""




# Conectarla a Redis
redis_url = os.getenv("REDIS_URL") 
if not redis_url:
    raise ValueError("No se encontro REDIS_URL en el archivo.env")

# creamos el cliente
# decode_responses=True es para recibir el texto y no bytes
r = redis.from_url(redis_url, decode_responses=True)

# Con Pydantic definimos el modelo de los datos que esperamos recibir
class URLInput(BaseModel):
    url: str

# Generamos un codigo aleatorio, para acortar la URL
def generar_codigo(length=5):
    # Hacemos una mezcla de numeros y letras
    caracteres= string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range (length))

# ----- Empezamos los Endpoints---------

# Endpoint principal
@app.get("/")
def read_root():
    return {"mensaje" : "API funcionando"}

@app.post("/shorten")
def shorten_url(item: URLInput):
    # recibe URL, genera un codigo corto y lo guardamos en Redis
    # Usamos SETNX para evitar sobreescribir codigos existentes
    
    # Generamos un codigo unico
    codigo=generar_codigo()
    
    # La clave de Redis seguira un patron {links:codigo}
    clave_redis = f"links:{codigo}"
    
    # Guardamos en Redis {True:se guardo, False:no}
    guardado = r.setnx(clave_redis, item.url)
    
    # Si el codgo ya existe (guardao=False), generamos otro
    while not guardado:
        codigo = generar_codigo()
        clave_redis = f"links:{codigo}"
        guardado = r.setnx(clave_redis, item.url)
    
    # Devolvemos el resultado
    return {
        "url_original":item.url,
        "short_code":codigo,
        "short_url":f"/{codigo}" #url relativa 
    }
    
""" 
Recuperamos todos los enlaces
"""
@app.get("/links")
def get_all_links():
    
    # Recuperamos el historial de enlaces
    
    try:
        # Buscamos las claves que empiecen por links:
        claves = r.keys("links:*")
        resultados = []
        
        for clave in claves:
            codigo = clave.replace("links:", "")
            url_original = r.get(clave)
            resultados.append({
                "short_code": codigo,
                "url_original": url_original
            })
        return resultados 
    except Exception as e:
        return {"Error": str(e)}


""" 
Recuperamos el enlace acortado que solicitan y redireccionamos a la url original
"""

@app.get("/{short_code}")
def redirect_to_url(short_code:str):
    
    clave_redis = f"links:{short_code}"
    
    # Buscamos en redis clave_redis
    url_original = r.get(clave_redis)
    
    # si no la encontramos -> Gestionamos el error
    if url_original is None:
        raise HTTPException(status_code=404, detail="Enlace no encontrado")
    
    # si la encontramos -> Redirigimos
    return RedirectResponse(url=url_original)
    
    