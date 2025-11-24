import oracledb

def get_connection():
    try:
        dsn = oracledb.makedsn("195.26.252.168", 1521, service_name="XEPDB1")
        conn = oracledb.connect(
            user="PAOLA_TORRENT",
            password="12345",
            dsn=dsn
        )
        return conn
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Error al conectar con la base de datos: {error.message}")
        return None
