import random

import requests

# --- Parte A: datos de conexion -------------------------------------------
BIBLIOTECA_URL = "http://localhost:8081/api/v1"
USUARIO = "bibliotecario"
PASSWORD = "Cuy6142!"

# --- Parte B: login para obtener el token -----------------------------------
respuesta = requests.post(BIBLIOTECA_URL + "/loginViaBasic", auth=(USUARIO, PASSWORD))
token = respuesta.json()["token"]
headers = {"X-API-KEY": token}
print("Login correcto. Token obtenido.")

# --- Parte C: catalogo actual -------------------------------------------------
respuesta = requests.get(BIBLIOTECA_URL + "/books", headers=headers)
print(f"Libros en el catalogo antes de la carga: {respuesta.headers['X-Total-Count']}")

# --- Parte D: datos para elegir al azar ------------------------------------
nombres = ["Ana", "Luis", "Carla", "Pedro", "Sofia", "Diego", "Marta", "Tomas", "Paula", "Jorge"]
apellidos = ["Rojas", "Soto", "Munoz", "Diaz", "Vera", "Leon", "Silva", "Reyes", "Castro", "Pinto"]
tipos = ["Fundamentos de", "Manual de", "Introduccion a", "Guia practica de", "Taller de"]
temas = ["Redes", "Python", "Seguridad", "VoIP", "Telepresencia", "Linux", "Cloud", "Git", "APIs REST"]
digitos_verificadores = "0123456789K"

# --- Parte E: crear 50 libros al azar, con id del 8 al 57 -----------------
isbn_usados = set()
creados = 0

for libro_id in range(8, 58):
    isbn = str(random.randint(10000000, 25999999)) + "-" + random.choice(digitos_verificadores)
    while isbn in isbn_usados:
        isbn = str(random.randint(10000000, 25999999)) + "-" + random.choice(digitos_verificadores)
    isbn_usados.add(isbn)

    libro = {
        "id": libro_id,
        "title": random.choice(tipos) + " " + random.choice(temas),
        "author": random.choice(nombres) + "_" + random.choice(apellidos),
        "isbn": isbn,
    }

    respuesta = requests.post(BIBLIOTECA_URL + "/books", headers=headers, json=libro)
    if respuesta.status_code == 201:
        creados = creados + 1
        print(f"{libro_id:2d}. Creado  isbn {isbn:<10}  {libro['author']:<12}  {libro['title']}")
    else:
        print(f"{libro_id:2d}. Error {respuesta.status_code}: {respuesta.json()['error']['mensaje']}")

print(f"\nTotal de libros creados: {creados} de 50")
