import oracledb
from conexion import get_connection

class Cliente:
    def __init__(self, rut_cliente, rut_vendedor, razon_social,
                 cantidad_trabajadores, nombre_contacto,
                 email_contacto, telefono_contacto):
        self.rut_cliente = rut_cliente
        self.rut_vendedor = rut_vendedor
        self.razon_social = razon_social
        self.cantidad_trabajadores = cantidad_trabajadores
        self.nombre_contacto = nombre_contacto
        self.email_contacto = email_contacto
        self.telefono_contacto = telefono_contacto

    def create(self):
        connection = get_connection()
        if not connection:
            return

        cursor = None
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO cliente (
                rut_cliente, rut_vendedor, razon_social,
                cantidad_trabajadores, nombre_contacto,
                email_contacto, telefono_contacto
            )
            VALUES (
                :rut_cliente, :rut_vendedor, :razon_social,
                :cantidad_trabajadores, :nombre_contacto,
                :email_contacto, :telefono_contacto
            )
            """
            cursor.execute(query, {
                'rut_cliente': self.rut_cliente,
                'rut_vendedor': self.rut_vendedor,
                'razon_social': self.razon_social,
                'cantidad_trabajadores': self.cantidad_trabajadores,
                'nombre_contacto': self.nombre_contacto,
                'email_contacto': self.email_contacto,
                'telefono_contacto': self.telefono_contacto
            })
            connection.commit()
            print("Cliente creado exitosamente.")
        except oracledb.IntegrityError:
            print("Error: El RUT del cliente ya existe en la base de datos.")
        except oracledb.DatabaseError as e:
            print(f"Error al crear el cliente: {e}")
        finally:
            if cursor:
                cursor.close()
            connection.close()

    def update(self):
        connection = get_connection()
        if not connection:
            return

        cursor = None
        try:
            cursor = connection.cursor()
            query = """
            UPDATE cliente
            SET rut_vendedor = :rut_vendedor,
                razon_social = :razon_social,
                cantidad_trabajadores = :cantidad_trabajadores,
                nombre_contacto = :nombre_contacto,
                email_contacto = :email_contacto,
                telefono_contacto = :telefono_contacto
            WHERE rut_cliente = :rut_cliente
            """
            cursor.execute(query, {
                'rut_cliente': self.rut_cliente,
                'rut_vendedor': self.rut_vendedor,
                'razon_social': self.razon_social,
                'cantidad_trabajadores': self.cantidad_trabajadores,
                'nombre_contacto': self.nombre_contacto,
                'email_contacto': self.email_contacto,
                'telefono_contacto': self.telefono_contacto
            })
            if cursor.rowcount == 0:
                print("No se encontró el cliente para actualizar.")
            else:
                connection.commit()
                print("Cliente actualizado exitosamente.")
        except oracledb.DatabaseError as e:
            print(f"Error al actualizar el cliente: {e}")
        finally:
            if cursor:
                cursor.close()
            connection.close()


def read_cliente(rut_cliente):
    connection = get_connection()
    if not connection:
        return None

    cursor = None
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM cliente WHERE rut_cliente = :rut_cliente"
        cursor.execute(query, {'rut_cliente': rut_cliente})
        result = cursor.fetchone()
        if result:
            return Cliente(*result)
        else:
            return None
    except oracledb.DatabaseError as e:
        print(f"Error al leer el cliente: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        connection.close()


def delete_cliente(rut_cliente):
    connection = get_connection()
    if not connection:
        return

    cursor = None
    try:
        cursor = connection.cursor()
        query = "DELETE FROM cliente WHERE rut_cliente = :rut_cliente"
        cursor.execute(query, {'rut_cliente': rut_cliente})
        if cursor.rowcount == 0:
            print("No se encontró el cliente para eliminar.")
        else:
            connection.commit()
            print("Cliente eliminado exitosamente.")
    except oracledb.DatabaseError as e:
        print(f"Error al eliminar el cliente: {e}")
    finally:
        if cursor:
            cursor.close()
        connection.close()


def print_menu():
    print("\nMenú CRUD Cliente")
    print("1. Crear Cliente")
    print("2. Leer Cliente")
    print("3. Actualizar Cliente")
    print("4. Eliminar Cliente")
    print("5. Salir")


def main():
    while True:
        print_menu()
        choice = input("Elige una opción (1-5): ")

        if choice == '1':
            try:
                rut_cliente = input("Ingrese RUT del cliente: ")
                rut_vendedor = input("Ingrese RUT del vendedor: ")
                razon_social = input("Ingrese razón social: ")
                cantidad_trabajadores = int(input("Ingrese cantidad de trabajadores: "))
                nombre_contacto = input("Ingrese nombre del contacto: ")
                email_contacto = input("Ingrese email de contacto: ")
                telefono_contacto = input("Ingrese teléfono de contacto: ")

                cliente = Cliente(
                    rut_cliente, rut_vendedor, razon_social,
                    cantidad_trabajadores, nombre_contacto,
                    email_contacto, telefono_contacto
                )
                cliente.create()
            except ValueError:
                print("Error: La cantidad de trabajadores debe ser un número entero.")

        elif choice == '2':
            rut_cliente = input("Ingrese RUT del cliente a buscar: ")
            cliente = read_cliente(rut_cliente)
            if cliente:
                print("\nCliente encontrado:")
                print(f"RUT Cliente: {cliente.rut_cliente}")
                print(f"RUT Vendedor: {cliente.rut_vendedor}")
                print(f"Razón Social: {cliente.razon_social}")
                print(f"Cantidad Trabajadores: {cliente.cantidad_trabajadores}")
                print(f"Nombre Contacto: {cliente.nombre_contacto}")
                print(f"Email Contacto: {cliente.email_contacto}")
                print(f"Teléfono Contacto: {cliente.telefono_contacto}")
            else:
                print("Cliente no encontrado.")

        elif choice == '3':
            rut_cliente = input("Ingrese RUT del cliente a actualizar: ")
            cliente = read_cliente(rut_cliente)
            if cliente:
                print("Ingrese los nuevos valores (deje en blanco para no cambiar):")
                rut_vendedor = input(f"Nuevo RUT del vendedor ({cliente.rut_vendedor}): ") or cliente.rut_vendedor
                razon_social = input(f"Nueva razón social ({cliente.razon_social}): ") or cliente.razon_social
                cantidad_trabajadores = input(f"Nueva cantidad de trabajadores ({cliente.cantidad_trabajadores}): ")
                cantidad_trabajadores = int(cantidad_trabajadores) if cantidad_trabajadores else cliente.cantidad_trabajadores
                nombre_contacto = input(f"Nuevo nombre del contacto ({cliente.nombre_contacto}): ") or cliente.nombre_contacto
                email_contacto = input(f"Nuevo email de contacto ({cliente.email_contacto}): ") or cliente.email_contacto
                telefono_contacto = input(f"Nuevo teléfono de contacto ({cliente.telefono_contacto}): ") or cliente.telefono_contacto

                cliente.rut_vendedor = rut_vendedor
                cliente.razon_social = razon_social
                cliente.cantidad_trabajadores = cantidad_trabajadores
                cliente.nombre_contacto = nombre_contacto
                cliente.email_contacto = email_contacto
                cliente.telefono_contacto = telefono_contacto
                cliente.update()
            else:
                print("Cliente no encontrado.")

        elif choice == '4':
            rut_cliente = input("Ingrese RUT del cliente a eliminar: ")
            delete_cliente(rut_cliente)

        elif choice == '5':
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Por favor, elige una opción entre 1 y 5.")


if __name__ == "__main__":
    main()
