import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

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
    # Consulta para verificar si existe el usuario con esas credenciales
    query = "SELECT EXISTS(SELECT 1 FROM persona WHERE mail_institucional = %s AND contrasena = %s)"
    
    # Pasar los parámetros como una tupla
    params = (email, password)
    
    # Ejecutar la consulta
    result = execute_query(query, params, is_select=True)
    
    # Si result tiene datos y el primer valor es 1, entonces existe
    if result and result[0][0] == 1:
        return True
    else:
        return False

def get_user_info(email):
    # Obtener información del usuario de tu base de datos según el email
    # Devolver un diccionario con los detalles del usuario (nombre, sexo, etc.)
    # Esta es una función de marcador de posición
    params= (email)
    query = "SELECT nombre,  FROM persona WHERE mail_institucional = %s )"
    name= execute_query(query, params, is_select=True)
    query = "SELECT sexo,  FROM persona WHERE mail_institucional = %s )"
    gender= execute_query(query, params, is_select=True)
    return {"nombre": name, "sexo": gender}  # Solo para pruebas