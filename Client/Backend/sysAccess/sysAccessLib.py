import requests
import json 

# Configuración de URLs
API_BASE_URL = "http://127.0.0.1:8000"  # API principal
FILE_MANAGER_URL = "http://127.0.0.1:8001"  # File Manager

class APIClient:
    def __init__(self):
        self.token = None

    def service_available(self):
        try:
            api_response = requests.get(f"{API_BASE_URL}/")
            fm_response = requests.get(f"{FILE_MANAGER_URL}/")
            
            if api_response.status_code == 200 and fm_response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        return False



    def login(self, username, password):
        """ Inicia sesión y guarda el token JWT """
        url = f"{API_BASE_URL}/login/"
        data = {"username": username, "password": password}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 200:
            self.token = response.json().get("access_token")
            return True
        else:
            return False

    def get_users(self):
        """ Obtiene la lista de usuarios """
        response = self._fetch_data("users", "Usuarios")
        return response if response else []

    def get_folders(self):
        """ Obtiene la lista de carpetas """
        return self._fetch_data("folders", "Carpetas")

    def get_files(self):
        """ Obtiene la lista de archivos """
        return self._fetch_data("files", "Archivos")

    def get_permission_name(self, permission_id):
        """ Obtiene el nombre de un permiso a partir de su ID """
        if not self.token:
            print("⚠ No autenticado: Token es None")
            return "Desconocido"
        
        url = f"{API_BASE_URL}/permission/{permission_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("name", "Desconocido")
        else:
            return "Desconocido"
        
    def say_hello_fm(self):
        """ Envía una solicitud al File Manager y obtiene su respuesta """
        url = f"{FILE_MANAGER_URL}/"
        return requests.get("http://127.0.0.1:8001/").json()
    
        



    def _fetch_data(self, endpoint, entity_name):
        """ Método privado para obtener datos de la API """
        if not self.token:
            print("⚠ No autenticado: Token es None")
            return False

        url = f"{API_BASE_URL}/{endpoint}/"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return False
