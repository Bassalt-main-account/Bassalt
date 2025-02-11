import requests
from getpass import getpass

# Configuración de URLs
API_BASE_URL = "http://127.0.0.1:8000"  # API principal
FILE_MANAGER_URL = "http://127.0.0.1:8001"  # File Manager

class APIClient:
    def __init__(self):
        self.token = None

    def login(self, username, password):
        """ Inicia sesión y guarda el token JWT """
        url = f"{API_BASE_URL}/login/"
        data = {"username": username, "password": password}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 200:
            self.token = response.json().get("access_token")
            print("X - Login exitoso")
            return True
        else:
            print("❌ Error de autenticación:", response.json().get("detail", "Error desconocido"))
            return False

    def get_users(self):
        """ Obtiene la lista de usuarios """
        if not self.token:
            print("⚠ No autenticado")
            return

        url = f"{API_BASE_URL}/users/"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            users = response.json()
            print("\n👥 Usuarios en la base de datos:")
            for user in users:
                print(f"- ID: {user['id']}, Username: {user['username']}")
        else:
            print("❌ Error al obtener usuarios:", response.json().get("detail", "Error desconocido"))

    def get_folders(self):
        """ Obtiene la lista de carpetas """
        if not self.token:
            print("⚠ No autenticado")
            return

        url = f"{API_BASE_URL}/folders/"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            folders = response.json()
            print("\n📂 Carpetas en la base de datos:")
            for folder in folders:
                print(f"- ID: {folder['id']}, Nombre: {folder['name']}")
        else:
            print("❌ Error al obtener carpetas:", response.json().get("detail", "Error desconocido"))

    def get_files(self):
        """ Obtiene la lista de archivos """
        if not self.token:
            print("⚠ No autenticado")
            return

        url = f"{API_BASE_URL}/files/"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            files = response.json()
            print("\n📄 Archivos en la base de datos:")
            for file in files:
                print(f"- ID: {file['id']}, Nombre: {file['name']}, Folder ID: {file['folder_id']}")
        else:
            print("❌ Error al obtener archivos:", response.json().get("detail", "Error desconocido"))

    def say_hello_fm(self):
        """ Envía una solicitud al File Manager y obtiene su respuesta """
        url = f"{FILE_MANAGER_URL}/"
        response = requests.get(url)

        if response.status_code == 200:
            print("\n🖥 File Manager dice:", response.json().get("message", "Sin respuesta"))
        else:
            print("❌ Error al conectar con File Manager")

def main():
    client = APIClient()

    # Autenticación antes de entrar al menú
    username = input("Username: ")
    password = getpass("Password: ")

    if not client.login(username, password):
        print("❌ No se pudo iniciar sesión. Saliendo...")
        return

    # Menú interactivo
    while True:
        print("\nMenú Principal: ============")
        print("1️- Ver cuentas")
        print("2️- Ver carpetas")
        print("3️- Ver archivos")
        print("4️- Decir 'Hola' a File Manager")
        print("0️- Salir")
        print("\n====================================")

        opcion = input("➢ Elige una opción: ")

        if opcion == "1":
            client.get_users()
        elif opcion == "2":
            client.get_folders()
        elif opcion == "3":
            client.get_files()
        elif opcion == "4":
            client.say_hello_fm()
        elif opcion == "0":
            break
        else:
            print("❌ Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()
