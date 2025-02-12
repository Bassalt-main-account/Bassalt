from getpass import getpass
from sysAccess.sysAccessLib import APIClient

def main():
    client = APIClient()
    available = client.service_available()
    
    if not available:
        print("[X] - Servicios no estan funcionando o apagados")
        return

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
            users = client.get_users()
            if users:
                print("\n👥 Usuarios registrados:")
                for user in users:
                    permiso_id = user.get("default_role")
                    permission_name = client.get_permission_name(permiso_id)
                    print(f"- ID: {user['id']}, Nombre: {user['username']}, Permisos: {permission_name}")
            else:
                print("❌ No se pudieron obtener los usuarios.")

        elif opcion == "2":
            folders = client.get_folders()
            if folders:
                print("\n📂 Carpetas en la base de datos:")
                for folder in folders:
                    print(f"- ID: {folder['id']}, Nombre: {folder['name']}, Parent-id: {folder.get('parent_id', 'N/A')}")
            else:
                print("❌ No se pudieron obtener las carpetas.")

        elif opcion == "3":
            files = client.get_files()
            if files:
                print("\n📄 Archivos en la base de datos:")
                for file in files:
                    print(f"- ID: {file['id']}, Nombre: {file['name']}, Folder ID: {file['folder_id']}")
            else:
                print("❌ No se pudieron obtener los archivos.")

        elif opcion == "4":
            message = client.say_hello_fm()
            if message:
                print(f"\n🖥 File Manager dice: {message.get("message")}")
            else:
                print("❌ Error al conectar con File Manager")

        elif opcion == "0":
            print("👋 Saliendo del programa...")
            break

        else:
            print("❌ Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()