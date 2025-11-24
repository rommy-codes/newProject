import oracledb
from datetime import datetime
from conexion import get_connection


class Empleado:
    def __init__(self, rut_empleado, nombre, direccion,
                 telefono, email, fecha_inicio,
                 salario, codigo_cargo, id_departamento):
        self.rut_empleado = rut_empleado
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.fecha_inicio = fecha_inicio     # datetime.date o str
        self.salario = salario
        self.codigo_cargo = codigo_cargo
        self.id_departamento = id_departamento

    
    # crear o create
    def create(self):
        connection = get_connection()
        if not connection:
            return

        cursor = None
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO empleado (
                    rut_empleado, nombre, direccion,
                    telefono, email, fecha_inicio,
                    salario, codigo_cargo, id_departamento
                )
                VALUES (
                    :rut_empleado, :nombre, :direccion,
                    :telefono, :email, :fecha_inicio,
                    :salario, :codigo_cargo, :id_departamento
                )
            """
            cursor.execute(query, {
                "rut_empleado": self.rut_empleado,
                "nombre": self.nombre,
                "direccion": self.direccion,
                "telefono": self.telefono,
                "email": self.email,
                "fecha_inicio": self.fecha_inicio,
                "salario": self.salario,
                "codigo_cargo": self.codigo_cargo,
                "id_departamento": self.id_departamento
            })
            connection.commit()
            print("Empleado creado correctamente.")
        except oracledb.IntegrityError as e:
            error, = e.args
            print("Error de integridad al crear empleado:", error.message)
        except oracledb.DatabaseError as e:
            error, = e.args
            print("Error al crear empleado:", error.message)
        finally:
            if cursor:
                cursor.close()
            connection.close()

    
    # actualizar o update
    def update(self):
        connection = get_connection()
        if not connection:
            return

        cursor = None
        try:
            cursor = connection.cursor()
            query = """
                UPDATE empleado
                SET nombre = :nombre,
                    direccion = :direccion,
                    telefono = :telefono,
                    email = :email,
                    fecha_inicio = :fecha_inicio,
                    salario = :salario,
                    codigo_cargo = :codigo_cargo,
                    id_departamento = :id_departamento
                WHERE rut_empleado = :rut_empleado
            """
            cursor.execute(query, {
                "rut_empleado": self.rut_empleado,
                "nombre": self.nombre,
                "direccion": self.direccion,
                "telefono": self.telefono,
                "email": self.email,
                "fecha_inicio": self.fecha_inicio,
                "salario": self.salario,
                "codigo_cargo": self.codigo_cargo,
                "id_departamento": self.id_departamento
            })
            if cursor.rowcount == 0:
                print("No se encontró el empleado para actualizar.")
            else:
                connection.commit()
                print("Empleado actualizado correctamente.")
        except oracledb.DatabaseError as e:
            error, = e.args
            print("Error al actualizar empleado:", error.message)
        finally:
            if cursor:
                cursor.close()
            connection.close()


#read funcion externa
def read_empleado(rut_empleado):
    connection = get_connection()
    if not connection:
        return None

    cursor = None
    try:
        cursor = connection.cursor()
        query = """
            SELECT rut_empleado, nombre, direccion,
                   telefono, email, fecha_inicio,
                   salario, codigo_cargo, id_departamento
            FROM empleado
            WHERE rut_empleado = :rut_empleado
        """
        cursor.execute(query, {"rut_empleado": rut_empleado})
        row = cursor.fetchone()
        if row:
            return Empleado(*row)
        else:
            return None
    except oracledb.DatabaseError as e:
        error, = e.args
        print("Error al leer empleado:", error.message)
        return None
    finally:
        if cursor:
            cursor.close()
        connection.close()


#borrar delete
def delete_empleado(rut_empleado):
    connection = get_connection()
    if not connection:
        return

    cursor = None
    try:
        cursor = connection.cursor()
        query = "DELETE FROM empleado WHERE rut_empleado = :rut_empleado"
        cursor.execute(query, {"rut_empleado": rut_empleado})
        if cursor.rowcount == 0:
            print("No se encontró el empleado para eliminar.")
        else:
            connection.commit()
            print("Empleado eliminado correctamente.")
    except oracledb.DatabaseError as e:
        error, = e.args
        print("Error al eliminar empleado:", error.message)
    finally:
        if cursor:
            cursor.close()
        connection.close()



# lista empleados
def listar_empleados():
    connection = get_connection()
    if not connection:
        return

    cursor = None
    try:
        cursor = connection.cursor()
        query = """
            SELECT rut_empleado, nombre, telefono,
                   email, fecha_inicio, salario
            FROM empleado
            ORDER BY nombre
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            print("No hay empleados registrados.")
            return

        print("\nLista de empleados")
        print("-" * 70)
        for rut, nombre, telefono, email, fecha, salario in rows:
            fecha_str = fecha.strftime("%Y-%m-%d") if fecha else "-"
            print(f"RUT: {rut:<15} | Nombre: {nombre:<25} | Tel: {telefono:<12} | "
                  f"Email: {email:<25} | Inicio: {fecha_str} | Salario: {salario}")
    except oracledb.DatabaseError as e:
        error, = e.args
        print("Error al listar empleados:", error.message)
    finally:
        if cursor:
            cursor.close()
        connection.close()


#menu
def print_menu():
    print("\nMenú CRUD Empleado")
    print("1. Crear Empleado")
    print("2. Leer Empleado")
    print("3. Actualizar Empleado")
    print("4. Eliminar Empleado")
    print("5. Listar Empleados")
    print("6. Salir")


def main():
    while True:
        print_menu()
        opcion = input("Elige una opción (1-6): ").strip()

        if opcion == "1":
            rut = input("RUT empleado: ").strip()
            nombre = input("Nombre: ").strip()
            direccion = input("Dirección: ").strip()
            telefono = input("Teléfono: ").strip()
            email = input("Email: ").strip()
            fecha_txt = input("Fecha inicio (YYYY-MM-DD): ").strip()
            try:
                fecha_inicio = datetime.strptime(fecha_txt, "%Y-%m-%d").date()
            except ValueError:
                print("Fecha inválida, se dejará NULL.")
                fecha_inicio = None

            try:
                salario = float(input("Salario: ").strip())
            except ValueError:
                print("Salario inválido, se usará 0.")
                salario = 0.0

            try:
                codigo_cargo = int(input("Código de cargo: ").strip())
            except ValueError:
                codigo_cargo = None

            try:
                id_departamento = int(input("ID de departamento: ").strip())
            except ValueError:
                id_departamento = None

            emp = Empleado(rut, nombre, direccion, telefono, email,
                           fecha_inicio, salario, codigo_cargo, id_departamento)
            emp.create()

        elif opcion == "2":
            rut = input("RUT del empleado a buscar: ").strip()
            emp = read_empleado(rut)
            if emp:
                print("\nEmpleado encontrado:")
                print(f"RUT: {emp.rut_empleado}")
                print(f"Nombre: {emp.nombre}")
                print(f"Dirección: {emp.direccion}")
                print(f"Teléfono: {emp.telefono}")
                print(f"Email: {emp.email}")
                print(f"Fecha inicio: {emp.fecha_inicio}")
                print(f"Salario: {emp.salario}")
                print(f"Código cargo: {emp.codigo_cargo}")
                print(f"ID departamento: {emp.id_departamento}")
            else:
                print("Empleado no encontrado.")

        elif opcion == "3":
            rut = input("RUT del empleado a actualizar: ").strip()
            emp = read_empleado(rut)
            if not emp:
                print("Empleado no encontrado.")
                continue

            print("Deja en blanco para mantener el valor actual.")
            nombre = input(f"Nombre ({emp.nombre}): ").strip() or emp.nombre
            direccion = input(f"Dirección ({emp.direccion}): ").strip() or emp.direccion
            telefono = input(f"Teléfono ({emp.telefono}): ").strip() or emp.telefono
            email = input(f"Email ({emp.email}): ").strip() or emp.email

            fecha_txt = input(f"Fecha inicio ({emp.fecha_inicio}) [YYYY-MM-DD]: ").strip()
            if fecha_txt:
                try:
                    fecha_inicio = datetime.strptime(fecha_txt, "%Y-%m-%d").date()
                except ValueError:
                    print("Fecha inválida, se mantiene la anterior.")
                    fecha_inicio = emp.fecha_inicio
            else:
                fecha_inicio = emp.fecha_inicio

            salario_txt = input(f"Salario ({emp.salario}): ").strip()
            if salario_txt:
                try:
                    salario = float(salario_txt)
                except ValueError:
                    print("Salario inválido, se mantiene el anterior.")
                    salario = emp.salario
            else:
                salario = emp.salario

            cargo_txt = input(f"Código cargo ({emp.codigo_cargo}): ").strip()
            codigo_cargo = emp.codigo_cargo if not cargo_txt else int(cargo_txt)

            depto_txt = input(f"ID departamento ({emp.id_departamento}): ").strip()
            id_departamento = emp.id_departamento if not depto_txt else int(depto_txt)

            emp.nombre = nombre
            emp.direccion = direccion
            emp.telefono = telefono
            emp.email = email
            emp.fecha_inicio = fecha_inicio
            emp.salario = salario
            emp.codigo_cargo = codigo_cargo
            emp.id_departamento = id_departamento

            emp.update()

        elif opcion == "4":
            rut = input("RUT del empleado a eliminar: ").strip()
            delete_empleado(rut)

        elif opcion == "5":
            listar_empleados()

        elif opcion == "6":
            print("Saliendo del programa de empleados.")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()
