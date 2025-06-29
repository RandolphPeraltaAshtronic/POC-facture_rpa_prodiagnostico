import time
import requests


def check_internet_connection(timeout: int = 5, retry_interval: int = 5) -> None:
    """
    Verifica si hay conexión activa a internet realizando una solicitud HTTP a Google.

    Esta función intenta realizar una conexión a http://www.google.com y espera hasta
    obtener una respuesta satisfactoria. En caso de no tener conexión, realiza reintentos
    periódicos hasta lograr el acceso.

    Args:
        timeout (int): Tiempo máximo de espera en segundos por intento.
        retry_interval (int): Tiempo en segundos entre cada intento.

    Returns:
        None

    Raises:
        RuntimeError: Si tras varios intentos no se logra establecer conexión (opcional).
    """
    connected = False
    while not connected:
        try:
            requests.get("http://www.google.com", timeout=timeout)
            print("✅ Conexión a internet establecida.")
            connected = True
        except (requests.ConnectionError, requests.Timeout):
            print("⚠️  Sin conexión a internet. Reintentando...")
            time.sleep(retry_interval)

 
 #check_internet_connection()