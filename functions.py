import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv("data.env")

def connect_to_supabase():
    """
    Connects to the Supabase PostgreSQL database using transaction pooler details
    and credentials stored in environment variables.
    """
    try:
        # Retrieve connection details from environment variables
        host = os.getenv("SUPABASE_DB_HOST")
        port = os.getenv("SUPABASE_DB_PORT")
        dbname = os.getenv("SUPABASE_DB_NAME")
        user = os.getenv("SUPABASE_DB_USER")
        password = os.getenv("SUPABASE_DB_PASSWORD")

        # Check if all required environment variables are set
        if not all([host, port, dbname, user, password]):
            print("Error: One or more Supabase environment variables are not set.")
            print("Please set SUPABASE_DB_HOST, SUPABASE_DB_PORT, SUPABASE_DB_NAME, SUPABASE_DB_USER, and SUPABASE_DB_PASSWORD.")
            return None

        # Establish the connection
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
        )
        print("Successfully connected to Supabase database.")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to Supabase database: {e}")
        return None

def execute_query(query, params=None, conn=None, is_select=True):
    """
    Executes a SQL query and returns the results as a pandas DataFrame for SELECT queries,
    or executes DML operations (INSERT, UPDATE, DELETE) and returns success status.
    
    Args:
        query (str): The SQL query to execute
        conn (psycopg2.extensions.connection, optional): Database connection object.
            If None, a new connection will be established.
        is_select (bool, optional): Whether the query is a SELECT query (True) or 
            a DML operation like INSERT/UPDATE/DELETE (False). Default is True.
            
    Returns:
        pandas.DataFrame or bool: A DataFrame containing the query results for SELECT queries,
            or True for successful DML operations, False otherwise.
    """
    try:
        # Create a new connection if one wasn't provided
        close_conn = False
        if conn is None:
            conn = connect_to_supabase()
            close_conn = True
        
        # Create cursor and execute query
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if is_select:
            # Fetch all results for SELECT queries
            results = cursor.fetchall()
            
            # Get column names from cursor description
            colnames = [desc[0] for desc in cursor.description]
            
            # Create DataFrame
            df = pd.DataFrame(results, columns=colnames)
            result = df
        else:
            # For DML operations, commit changes and return success
            conn.commit()
            result = True
        
        # Close cursor and connection if we created it
        cursor.close()
        if close_conn:
            conn.close()
            
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        # Rollback any changes if an error occurred during DML operation
        if conn and not is_select:
            conn.rollback()
        return pd.DataFrame() if is_select else False

def add_person(dni, user_type, name, password, mail, gender):
    query = """
    INSERT INTO persona (dni, clasificacion, carrera, facultad, nombre, contrasena, mail_institucional, sexo)
    VALUES (%s, %s, NULL, NULL, %s, %s, %s, %s)
    """
    params = (dni, user_type, name, password, mail, gender)
    return execute_query(query, params=params, is_select=False)

def verify_credentials(email, password):
    query = "SELECT EXISTS(SELECT 1 FROM persona WHERE mail_institucional = %s AND contrasena = %s)"
    params = (email, password)
    result = execute_query(query, params, is_select=True)

    if not result.empty and result.iloc[0, 0] == 1:
        return True
    else:
        return False

def verify_credentials_with_type(email, password, user_type):
    query = """
        SELECT 1 FROM persona 
        WHERE mail_institucional = %s AND contrasena = %s AND clasificacion = %s
    """
    params = (email, password, user_type)
    result = execute_query(query, params, is_select=True)
    return result is not None and not result.empty

def get_user_info(email):
    query = "SELECT nombre, sexo FROM persona WHERE mail_institucional = %s"
    params = (email,)
    result = execute_query(query, params, is_select=True)

    if not result.empty:
        nombre = result.iloc[0]["nombre"]
        sexo = result.iloc[0]["sexo"]
        return {"nombre": nombre, "sexo": sexo}
    else:
        return {"nombre": "Usuario", "sexo": ""}

#user funciones nuevas

# Funciones adicionales para agregar al archivo functions.py

def get_user_complete_info(email):
    """Obtiene toda la información completa de un usuario por su email"""
    query = "SELECT * FROM persona WHERE mail_institucional = %s"
    params = (email,)
    return execute_query(query, params, is_select=True)

def update_user_password(new_password, email):
    """Actualiza la contraseña de un usuario"""
    query = "UPDATE persona SET contrasena = %s WHERE mail_institucional = %s"
    params = (new_password, email)
    return execute_query(query, params, is_select=False)

def update_user_academic_info(facultad, carrera, email):
    """
    Actualiza la información académica de la persona
    referenciando su clave primaria (mail_institucional ).
    """
    query = " UPDATE persona SET facultad = %s, carrera  = %s WHERE mail_institucional = %s"
    params = (facultad, carrera, email)
    return execute_query(query, params, is_select=False)

def solicitar_prestamo_libro(id_libro, dni, dias_prestamo=7):
    """
    Registra un nuevo préstamo de libro para un usuario por DNI.
    """
    fecha_prestamo = datetime.now().date()
    fecha_devolucion = fecha_prestamo + timedelta(days=dias_prestamo)
    query = """
        INSERT INTO prestamo (id_libro, dni, fecha_prestamo, fecha_devolucion, estado)
        VALUES (%s, %s, %s, %s, 'activo')
    """
    params = (id_libro, dni, fecha_prestamo, fecha_devolucion)
    return execute_query(query, params, is_select=False)

def get_user_loans(dni):
    """
    Obtiene todos los préstamos de un usuario por DNI (activos, vencidos y solicitados).
    """
    query = """
        SELECT p.id_libro, l.titulo, l.autor, p.fecha_prestamo, p.fecha_devolucion, p.estado
        FROM prestamo p
        JOIN libros l ON p.id_libro = l.id_libro
        WHERE p.dni = %s
        ORDER BY p.fecha_prestamo DESC
    """
    params = (dni,)
    return execute_query(query, params, is_select=True)


def marcar_libro_no_disponible(id_libro):
    """
    Marca el libro como no disponible en la base de datos.
    """
    query = "UPDATE libros SET disponibilidad = FALSE WHERE id_libro = %s"
    params = (id_libro,)
    return execute_query(query, params, is_select=False)

def lista_de_espera_libro(dni, titulo):
    # 1. Buscar cuántas personas ya están en lista de espera para ese libro
    query_count = "SELECT COUNT(*) AS cantidad FROM lista_de_espera WHERE titulo = %s"
    params_count = (titulo,)
    df_count = execute_query(query_count, params_count, is_select=True)
    if df_count is not None and not df_count.empty:
        orden_de_llegada = int(df_count.iloc[0]['cantidad']) + 1
    else:
        orden_de_llegada = 1

    # 2. Insertar en lista_de_espera con el orden correcto
    query_espera = """
        INSERT INTO lista_de_espera (dni, titulo, orden_de_llegada)
        VALUES (%s, %s, %s)
    """
    params_espera = (dni, titulo, orden_de_llegada)
    result_espera = execute_query(query_espera, params_espera, is_select=False)

    # 3. Buscar id_libro por título
    query_id = "SELECT id_libro FROM libros WHERE titulo = %s"
    params_id = (titulo,)
    df_id = execute_query(query_id, params_id, is_select=True)
    if df_id is not None and not df_id.empty:
        id_libro = int(df_id.iloc[0]['id_libro'])
        # 4. Insertar en prestamo con estado 'solicitado'
        query_prestamo = """
            INSERT INTO prestamo (dni, id_libro, estado)
            VALUES (%s, %s, 'solicitado')
        """
        params_prestamo = (dni, id_libro)
        result_prestamo = execute_query(query_prestamo, params_prestamo, is_select=False)
    else:
        result_prestamo = False

    return result_espera and result_prestamo

# Agrega esta función o modifica la existente para obtener el orden de llegada
def get_user_requested_loans_with_order(dni):
    query = """
        SELECT l.titulo, l.autor, p.estado, le.orden_de_llegada
        FROM prestamo p
        JOIN libros l ON p.id_libro = l.id_libro
        JOIN lista_de_espera le ON le.dni = p.dni AND le.titulo = l.titulo
        WHERE p.dni = %s AND p.estado = 'solicitado'
        ORDER BY le.orden_de_llegada
    """
    params = (dni,)
    return execute_query(query, params, is_select=True)

def marcar_prestamos_vencidos(dni):
    """
    Marca como 'vencido' todos los préstamos activos del usuario cuya fecha_devolucion ya pasó.
    """
    from datetime import datetime
    hoy = datetime.now().date()
    query = """
        UPDATE prestamo
        SET estado = 'vencido'
        WHERE dni = %s AND estado = 'activo' AND fecha_devolucion < %s
    """
    params = (dni, hoy)
    execute_query(query, params, is_select=False)

def get_libro_by_id(id_libro):
    query = "SELECT * FROM libros WHERE id_libro = %s"
    params = (id_libro,)
    return execute_query(query, params, is_select=True)

def update_numero_copias_disponibles(id_libro, nuevo_valor):
    # Obtener el valor anterior para saber si hay que cambiar disponibilidad
    libro = get_libro_by_id(id_libro)
    if libro is not None and not libro.empty:
        anterior = int(libro.iloc[0]['numero_de_copias_disponibles'])
        query = "UPDATE libros SET numero_de_copias_disponibles = %s WHERE id_libro = %s"
        params = (nuevo_valor, id_libro)
        execute_query(query, params, is_select=False)
        # Cambiar disponibilidad si corresponde
        if anterior == 0 and nuevo_valor == 1:
            query_disp = "UPDATE libros SET disponibilidad = TRUE WHERE id_libro = %s"
            execute_query(query_disp, (id_libro,), is_select=False)
        elif anterior == 1 and nuevo_valor == 0:
            query_disp = "UPDATE libros SET disponibilidad = FALSE WHERE id_libro = %s"
            execute_query(query_disp, (id_libro,), is_select=False)

def procesar_prestamo_libro(id_libro):
    """
    Resta 1 a numero_de_copias_disponibles del libro.
    Si el resultado es 0, pone disponibilidad en FALSE.
    Si el resultado es mayor a 0, mantiene disponibilidad en TRUE.
    """
    libro = get_libro_by_id(id_libro)
    if libro is not None and not libro.empty:
        copias_disp = int(libro.iloc[0]['numero_de_copias_disponibles'])
        if copias_disp > 1:
            nuevo_valor = copias_disp - 1
            query = "UPDATE libros SET numero_de_copias_disponibles = %s, disponibilidad = TRUE WHERE id_libro = %s"
            params = (nuevo_valor, id_libro)
            execute_query(query, params, is_select=False)
        elif copias_disp == 1:
            query = "UPDATE libros SET numero_de_copias_disponibles = 0, disponibilidad = FALSE WHERE id_libro = %s"
            params = (id_libro,)
            execute_query(query, params, is_select=False)

def verificar_dni_usuario(email, dni):
    """
    Verifica si el dni corresponde al usuario con ese email.
    """
    query = "SELECT 1 FROM persona WHERE mail_institucional = %s AND dni = %s"
    params = (email, dni)
    result = execute_query(query, params, is_select=True)
    return result is not None and not result.empty

def buscar_prestamos(filtros):
    query = """
        SELECT p.estado, p.fecha_prestamo, p.fecha_devolucion, p.dni, p.id_libro, l.titulo, per.nombre
        FROM prestamos p
        JOIN libro l ON p.id_libro = l.id_libro
        JOIN persona per ON p.dni = per.dni
        WHERE 1=1
    """
    params = []
    if filtros.get("estado"):
        query += " AND p.estado LIKE ?"
        params.append(f"%{filtros['estado']}%")
    if filtros.get("fecha_prestamo"):
        query += " AND p.fecha_prestamo = ?"
        params.append(filtros["fecha_prestamo"])
    if filtros.get("fecha_devolucion"):
        query += " AND p.fecha_devolucion = ?"
        params.append(filtros["fecha_devolucion"])
    if filtros.get("dni"):
        query += " AND p.dni LIKE ?"
        params.append(f"%{filtros['dni']}%")
    if filtros.get("id_libro"):
        query += " AND p.id_libro = ?"
        params.append(filtros["id_libro"])
    if filtros.get("titulo"):
        query += " AND l.titulo LIKE ?"
        params.append(f"%{filtros['titulo']}%")
    return execute_query(query, params, is_select=True)

def get_loans():
    """
    Obtiene todos los préstamos de la biblioteca (activos, vencidos y solicitados), incluyendo el nombre del usuario y el id del libro.
    """
    query = """
        SELECT p.id_libro, l.titulo, l.autor, p.fecha_prestamo, p.fecha_devolucion, p.estado, p.dni, per.nombre
        FROM prestamo p
        JOIN libros l ON p.id_libro = l.id_libro
        JOIN persona per ON p.dni = per.dni
        ORDER BY p.fecha_prestamo DESC
    """
    params = ()
    return execute_query(query, params, is_select=True)

def get_requested_loans_with_order():
    query = """
        SELECT p.id_libro, l.titulo, l.autor, p.estado, le.orden_de_llegada, p.dni, per.nombre
        FROM prestamo p
        JOIN libros l ON p.id_libro = l.id_libro
        LEFT JOIN lista_de_espera le ON le.dni = p.dni AND LOWER(le.titulo) = LOWER(l.titulo)
        JOIN persona per ON p.dni = per.dni
        WHERE LOWER(p.estado) = 'solicitado'
        ORDER BY COALESCE(le.orden_de_llegada, 9999)
    """
    params = ()
    return execute_query(query, params, is_select=True)

def marcar_todos_prestamos_vencidos():
    """
    Marca como 'vencido' todos los préstamos activos del usuario cuya fecha_devolucion ya pasó.
    """
    from datetime import datetime
    hoy = datetime.now().date()
    query = """
        UPDATE prestamo
        SET estado = 'vencido'
        WHERE estado = 'activo' AND fecha_devolucion < %s
    """
    params = ( hoy)
    execute_query(query, params, is_select=False)

def libro_devuelto_func(id_libro):
    from datetime import datetime, timedelta
    # 1. Buscar si hay préstamo solicitado para este libro
    query = "SELECT * FROM prestamo WHERE id_libro = %s AND LOWER(estado) = 'solicitado' ORDER BY fecha_prestamo ASC LIMIT 1"
    df_solicitado = execute_query(query, (id_libro,), is_select=True)
    # 2. Borrar el préstamo devuelto de la tabla prestamo (el que está activo o vencido) SIEMPRE
    query_del_prestamo = "DELETE FROM prestamo WHERE id_libro = %s AND (estado = 'activo' OR estado = 'vencido')"
    execute_query(query_del_prestamo, (id_libro,), is_select=False)
    libro = get_libro_by_id(id_libro)
    if df_solicitado is not None and not df_solicitado.empty:
        # Hay alguien en la lista de espera: el libro pasa directamente a esa persona
        prestamo = df_solicitado.iloc[0]
        dni = prestamo['dni']
        titulo = libro.iloc[0]['titulo']
        # Buscar en lista_de_espera el de orden_de_llegada = 1 para este título
        query_espera = "SELECT * FROM lista_de_espera WHERE titulo = %s AND orden_de_llegada = 1"
        df_espera = execute_query(query_espera, (titulo,), is_select=True)
        if df_espera is not None and not df_espera.empty:
            # Eliminar el préstamo solicitado de este usuario
            query_del_solicitado = "DELETE FROM prestamo WHERE id_libro = %s AND dni = %s AND LOWER(estado) = 'solicitado'"
            execute_query(query_del_solicitado, (id_libro, dni), is_select=False)
            # Crear un nuevo préstamo activo para este usuario
            fecha_prestamo = datetime.now().date()
            fecha_devolucion = fecha_prestamo + timedelta(days=7)
            query_insert = """
                INSERT INTO prestamo (id_libro, dni, fecha_prestamo, fecha_devolucion, estado)
                VALUES (%s, %s, %s, %s, 'activo')
            """
            execute_query(query_insert, (id_libro, dni, fecha_prestamo, fecha_devolucion), is_select=False)
            # Borrar de lista_de_espera
            query_del = "DELETE FROM lista_de_espera WHERE titulo = %s AND dni = %s"
            execute_query(query_del, (titulo, dni), is_select=False)
            # Restar 1 a orden_de_llegada de los demás en lista_de_espera para ese título
            query_update_orden = "UPDATE lista_de_espera SET orden_de_llegada = orden_de_llegada - 1 WHERE titulo = %s AND orden_de_llegada > 1"
            execute_query(query_update_orden, (titulo,), is_select=False)
    else:
        # NO hay nadie en la lista de espera: sumar copia y actualizar disponibilidad si corresponde
        if libro is not None and not libro.empty:
            copias_disp = int(libro.iloc[0]['numero_de_copias_disponibles'])
            nuevo_valor = copias_disp + 1
            update_numero_copias_disponibles(id_libro, nuevo_valor)
            # Si disponibilidad era FALSE, poner TRUE si hay al menos 1 copia
            if not libro.iloc[0]['disponibilidad'] and nuevo_valor > 0:
                query = "UPDATE libros SET disponibilidad = TRUE WHERE id_libro = %s"
                execute_query(query, (id_libro,), is_select=False)
    return True

def get_facultades():
    """
    Devuelve la lista de facultades únicas de la tabla carreras_por_facultad.
    """
    query = """
        SELECT DISTINCT facultad
        FROM carreras_por_facultad
        ORDER BY facultad
    """
    return execute_query(query, is_select=True)

def get_carreras_por_facultad(facultad):
    """
    Devuelve la lista de carreras para una facultad dada desde la tabla carreras_por_facultad.
    """
    query = """
        SELECT carrera
        FROM carreras_por_facultad
        WHERE facultad = %s
        ORDER BY carrera
    """
    params = (facultad,)
    return execute_query(query, params, is_select=True)

def get_logo_url():
    """
    Devuelve el URL del logo desde la tabla logo (primer valor de la columna url).
    """
    query = "SELECT url FROM logo LIMIT 1"
    df = execute_query(query, is_select=True)
    if df is not None and not df.empty:
        return df.iloc[0]["url"]
    return None