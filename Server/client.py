import requests

BASE_URL = "http://127.0.0.1:8000"  # Dirección de la API del servidor

class APIClient:
    def __init__(self):
        self.token = None

    def login(self, username, password):
        """ Inicia sesión y guarda el token JWT """
        url = f"{BASE_URL}/login/"
        data = {"username": username, "password": password}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 200:
            self.token = response.json().get("access_token")
            return {"message": "Login exitoso", "token": self.token}
        else:
            return {"error": response.json().get("detail", "Error desconocido")}

    def get_users(self):
        """ Obtiene la lista de usuarios (requiere autenticación) """
        if not self.token:
            return {"error": "No autenticado"}

        url = f"{BASE_URL}/users/"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Error desconocido")}

    def get_user_by_id(self, user_id):
        """ Obtiene información de un usuario por ID """
        if not self.token:
            return {"error": "No autenticado"}

        url = f"{BASE_URL}/user/{user_id}"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Error desconocido")}

    def create_user(self, username, password):
        """ Crea un nuevo usuario """
        url = f"{BASE_URL}/register/"
        data = {"username": username, "password": password}
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Error desconocido")}

    def delete_user(self, user_id):
        """ Elimina un usuario (requiere autenticación) """
        if not self.token:
            return {"error": "No autenticado"}

        url = f"{BASE_URL}/delete_user/{user_id}"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            return {"message": f"Usuario {user_id} eliminado correctamente"}
        else:
            return {"error": response.json().get("detail", "Error desconocido")}

# Ejemplo de uso
if __name__ == "__main__":
    client = APIClient()

    # Iniciar sesión
    username = input("Username: ")
    password = input("Password: ")
    login_response = client.login(username, password)
    print(login_response)

    if client.token:
        # Obtener lista de usuarios
        print("Lista de usuarios:")
        print(client.get_users())

        # Obtener un usuario por ID
        user_id = input("Ingrese ID de usuario para buscar: ")
        print(client.get_user_by_id(user_id))
