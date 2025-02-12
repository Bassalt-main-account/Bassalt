import requests
import json 

class APIClient:
    def __init__(self, ip_address, api_port, file_manager_port):
        self.api_base_url = f"http://{ip_address}:{api_port}"
        self.file_manager_url = f"http://{ip_address}:{file_manager_port}"
        self.token = None

    def service_available(self):
        try:
            api_response = requests.get(f"{self.api_base_url}/")
            fm_response = requests.get(f"{self.file_manager_url}/")
            
            if api_response.status_code == 200 and fm_response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        return False

    def login(self, username, password):
        """ Inicia sesión y guarda el token JWT """
        url = f"{self.api_base_url}/login/"
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
        return self._fetch_data("users", "Usuarios")

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
        
        url = f"{self.api_base_url}/permission/{permission_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("name", "Desconocido")
        else:
            return "Desconocido"
        
    def say_hello_fm(self):
        """ Envía una solicitud al File Manager y obtiene su respuesta """
        url = f"{self.file_manager_url}/"
        return requests.get(url).json()
    
    def _fetch_data(self, endpoint, entity_name):
        """ Método privado para obtener datos de la API """
        if not self.token:
            return False

        url = f"{self.api_base_url}/{endpoint}/"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return False
    
    


