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
        SELECT l.titulo, l.autor, p.fecha_prestamo, p.fecha_devolucion, p.estado
        FROM prestamo p
        JOIN libros l ON p.id_libro = l.id_libro
        WHERE p.dni = %s
        ORDER BY p.fecha_prestamo DESC
    """
    params = (dni,)
    return execute_query(query, params, is_select=True)

def extend_loan(loan_id, additional_days=7):
    """
    Extiende la fecha de devolución de un préstamo activo.
    """
    query = """
        UPDATE prestamo
        SET fecha_devolucion = fecha_devolucion + INTERVAL '%s days'
        WHERE id_prestamo = %s AND estado = 'activo'
    """
    params = (additional_days, loan_id)
    return execute_query(query, params, is_select=False)

def marcar_libro_no_disponible(id_libro):
    """
    Marca el libro como no disponible en la base de datos.
    """
    query = "UPDATE libros SET disponibilidad = FALSE WHERE id_libro = %s"
    params = (id_libro,)
    return execute_query(query, params, is_select=False)

def lista_de_espera_libro(dni, titulo):
    # 1. Insertar en lista_de_espera
    query_espera = """
        INSERT INTO lista_de_espera (dni, titulo)
        VALUES (%s, %s)
    """
    params_espera = (dni, titulo)
    result_espera = execute_query(query_espera, params_espera, is_select=False)

    # 2. Buscar id_libro por título
    query_id = "SELECT id_libro FROM libros WHERE titulo = %s"
    params_id = (titulo,)
    df_id = execute_query(query_id, params_id, is_select=True)
    if df_id is not None and not df_id.empty:
        id_libro = int(df_id.iloc[0]['id_libro'])  # <-- Conversión aquí
        # 3. Insertar en prestamo con estado 'solicitado'
        query_prestamo = """
            INSERT INTO prestamo (dni, id_libro, estado)
            VALUES (%s, %s, 'solicitado')
        """
        params_prestamo = (dni, id_libro)
        result_prestamo = execute_query(query_prestamo, params_prestamo, is_select=False)
    else:
        result_prestamo = False

    return result_espera and result_prestamo