import oracledb
import bcrypt
from datetime import datetime
from conexion import get_connection


# ==============================
# CREAR USUARIO
# ==============================
def crear_usuario():
    connection = get_connection()
    if not connection:
        return

    rut = input("Ingrese RUT del usuario: ").strip()
    password = input("Ingrese contraseña: ").strip()
    codigo_rol = input("Ingrese código de rol (por ejemplo: ADMIN o USER): ").strip().upper()

    # Hashear contraseña
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuario (rut_usuario, password_hash, codigo_rol)
            VALUES (:rut, :hash, :rol)
        """, {
            'rut': rut,
            'hash': password_hash.decode('utf-8'),
            'rol': codigo_rol
        })
        connection.commit()
        print("Usuario creado exitosamente.")
    except oracledb.IntegrityError:
        print("El RUT ingresado ya existe.")
    except oracledb.DatabaseError as e:
        print(f"Error al crear usuario: {e}")
    finally:
        cursor.close()
        connection.close()


# ==============================
# LOGIN (AUTENTICACIÓN)
# ==============================
def login_usuario():
    connection = get_connection()
    if not connection:
        return

    rut = input("Ingrese RUT de usuario: ").strip()
    password = input("Ingrese contraseña: ").strip()

    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT password_hash, estado FROM usuario WHERE rut_usuario = :rut",
            {'rut': rut}
        )
        result = cursor.fetchone()
        if result:
            stored_hash, estado = result
            if estado == 'I':
                print("El usuario está inactivo.")
            elif bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                print("Autenticación exitosa.")
            else:
                print("Contraseña incorrecta.")
        else:
            print("Usuario no encontrado.")
    except oracledb.DatabaseError as e:
        print(f"Error al autenticar: {e}")
    finally:
        cursor.close()
        connection.close()


# ==============================
# LISTAR USUARIOS
# ==============================
def listar_usuarios():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT rut_usuario, codigo_rol, fecha_ingreso, estado 
            FROM usuario 
            ORDER BY fecha_ingreso DESC
        """)
        rows = cursor.fetchall()
        if rows:
            print("\nUsuarios registrados:")
            print("-" * 60)
            for rut, rol, fecha, estado in rows:
                estado_str = "Activo" if estado == 'A' else "Inactivo"
                fecha_fmt = fecha.strftime("%Y-%m-%d %H:%M:%S") if fecha else "-"
                print(f"RUT: {rut:<15} | Rol: {rol:<8} | Fecha: {fecha_fmt} | Estado: {estado_str}")
        else:
            print("No hay usuarios registrados.")
    except oracledb.DatabaseError as e:
        print(f"Error al listar usuarios: {e}")
    finally:
        cursor.close()
        connection.close()


# ==============================
# DESACTIVAR USUARIO
# ==============================
def desactivar_usuario():
    connection = get_connection()
    if not connection:
        return

    rut = input("Ingrese RUT del usuario a desactivar: ").strip()

    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE usuario SET estado = 'I' WHERE rut_usuario = :rut",
            {'rut': rut}
        )
        if cursor.rowcount == 0:
            print("No se encontró el usuario.")
        else:
            connection.commit()
            print("Usuario desactivado correctamente.")
    except oracledb.DatabaseError as e:
        print(f"Error al desactivar usuario: {e}")
    finally:
        cursor.close()
        connection.close()


# ==============================
# MENÚ PRINCIPAL
# ==============================
def print_menu():
    print("\nMenú de Usuarios")
    print("1. Crear Usuario")
    print("2. Iniciar Sesión (Login)")
    print("3. Listar Usuarios")
    print("4. Desactivar Usuario")
    print("5. Salir")


def main():
    while True:
        print_menu()
        opcion = input("Seleccione una opción (1-5): ")

        if opcion == '1':
            crear_usuario()
        elif opcion == '2':
            login_usuario()
        elif opcion == '3':
            listar_usuarios()
        elif opcion == '4':
            desactivar_usuario()
        elif opcion == '5':
            print("Saliendo del sistema de usuarios.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()
