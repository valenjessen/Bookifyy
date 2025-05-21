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

#Book Functions

def search_books(search_term):
    """
    Search books by title or author.
    Returns books matching the search criteria.
    """
    query = """
    SELECT * FROM libros 
    WHERE titulo ILIKE %s OR autor ILIKE %s 
    ORDER BY titulo
    """
    params = (f'%{search_term}%', f'%{search_term}%')
    return execute_query(query, params=params)

def get_book_details(numero_de_id):
    """
    Get detailed information about a specific book.
    """
    query = "SELECT * FROM libros WHERE numero_de_id = %s"
    params = (numero_de_id,)
    return execute_query(query, params=params)

def update_book_availability(numero_de_id, is_available):
    """
    Update the availability status of a book.
    """
    query = "UPDATE libros SET disponibilidad = %s WHERE numero_de_id = %s"
    params = (is_available, numero_de_id)
    return execute_query(query, params=params, is_select=False)

def add_new_book(titulo, autor, editoria_edicion, disponibilidad, biblioteca, ubicacion):
    """
    Add a new book to the database.
    """
    query = """
    INSERT INTO libros (titulo, autor, editoria_edicion, disponibilidad, biblioteca, ubicacion)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING numero_de_id
    """
    params = (titulo, autor, editoria_edicion, disponibilidad, biblioteca, ubicacion)
    result = execute_query(query, params=params)
    return result.iloc[0]["numero_de_id"] if not result.empty else None

#Loan Functions

def create_loan(dni, numero_de_id, days=14):
    """
    Create a new book loan.
    """
    today = datetime.now().date()
    end_date = today + timedelta(days=days)
    
    query = """
    INSERT INTO prestamo (dni, numero_de_id, fecha_de_inicio, fecha_de_fin, estado)
    VALUES (%s, %s, %s, %s, 'Vigente')
    """
    params = (dni, numero_de_id, today, end_date)
    success = execute_query(query, params=params, is_select=False)
    
    if success:
        # Update book availability
        update_book_availability(numero_de_id, False)
    
    return success

def get_user_loans(dni):
    """
    Get all loans for a specific user.
    """
    query = """
    SELECT p.*, l.titulo, l.autor
    FROM prestamo p
    JOIN libros l ON p.numero_de_id = l.numero_de_id
    WHERE p.dni = %s
    ORDER BY 
        CASE 
            WHEN p.estado = 'Vencida' THEN 1
            WHEN p.estado = 'Vigente' THEN 2
            WHEN p.estado = 'Solicitada' THEN 3
            ELSE 4
        END,
        p.fecha_de_fin DESC
    """
    params = (dni,)
    return execute_query(query, params=params)

def get_all_loans(filter_state=None):
    """
    Get all loans with optional filtering by state.
    Used by librarians.
    """
    if filter_state:
        query = """
        SELECT p.*, l.titulo, per.nombre
        FROM prestamo p
        JOIN libros l ON p.numero_de_id = l.numero_de_id
        JOIN persona per ON p.dni = per.dni
        WHERE p.estado = %s
        ORDER BY 
            CASE 
                WHEN p.estado = 'Vencida' THEN 1
                WHEN p.estado = 'Vigente' THEN 2
                ELSE 3
            END,
            p.fecha_de_fin DESC
        """
        params = (filter_state,)
    else:
        query = """
        SELECT p.*, l.titulo, per.nombre
        FROM prestamo p
        JOIN libros l ON p.numero_de_id = l.numero_de_id
        JOIN persona per ON p.dni = per.dni
        ORDER BY 
            CASE 
                WHEN p.estado = 'Vencida' THEN 1
                WHEN p.estado = 'Vigente' THEN 2
                ELSE 3
            END,
            p.fecha_de_fin DESC
        """
        params = None
    
    return execute_query(query, params=params)

def extend_loan(dni, numero_de_id, additional_days=7):
    """
    Extend an existing loan if no one is waiting for the book.
    """
    # First check if anyone is waiting for this book
    waiting_query = """
    SELECT COUNT(*) as count
    FROM lista_de_espera
    WHERE titulo = (SELECT titulo FROM libros WHERE numero_de_id = %s)
    """
    waiting_params = (numero_de_id,)
    waiting_result = execute_query(waiting_query, params=waiting_params)
    
    if waiting_result.iloc[0]["count"] > 0:
        return False, "No se puede extender el préstamo porque hay personas en lista de espera"
    
    # If no one is waiting, extend the loan
    query = """
    UPDATE prestamo
    SET fecha_de_fin = fecha_de_fin + INTERVAL '%s days'
    WHERE dni = %s AND numero_de_id = %s AND estado = 'Vigente'
    """
    params = (additional_days, dni, numero_de_id)
    success = execute_query(query, params=params, is_select=False)
    
    return success, "Préstamo extendido exitosamente" if success else "No se pudo extender el préstamo"

def update_loan_status():
    """
    Update loan status for overdue loans.
    This should be run regularly (e.g., once a day).
    """
    today = datetime.now().date()
    query = """
    UPDATE prestamo
    SET estado = 'Vencida'
    WHERE fecha_de_fin < %s AND estado = 'Vigente'
    """
    params = (today,)
    return execute_query(query, params=params, is_select=False)

def return_book(dni, numero_de_id):
    """
    Process a book return.
    """
    # First, mark the loan as returned
    query = """
    DELETE FROM prestamo
    WHERE dni = %s AND numero_de_id = %s
    """
    params = (dni, numero_de_id)
    success = execute_query(query, params=params, is_select=False)
    
    if success:
        # Update book availability
        update_book_availability(numero_de_id, True)
        
        # Check waiting list
        check_waiting_list(numero_de_id)
    
    return success

#Waiting List Functions

def add_to_waiting_list(dni, titulo):
    """
    Add a user to the waiting list for a book.
    """
    # Get the next order number for this book title
    order_query = """
    SELECT COALESCE(MAX(orden_de_llegada), 0) + 1 as next_order
    FROM lista_de_espera
    WHERE titulo = %s
    """
    order_params = (titulo,)
    order_result = execute_query(order_query, params=order_params)
    next_order = order_result.iloc[0]["next_order"] if not order_result.empty else 1
    
    # Add to waiting list
    query = """
    INSERT INTO lista_de_espera (dni, titulo, orden_de_llegada)
    VALUES (%s, %s, %s)
    """
    params = (dni, titulo, next_order)
    return execute_query(query, params=params, is_select=False)

def get_waiting_list(titulo=None):
    """
    Get waiting list for a specific book title or all waiting lists.
    """
    if titulo:
        query = """
        SELECT le.*, p.nombre
        FROM lista_de_espera le
        JOIN persona p ON le.dni = p.dni
        WHERE le.titulo = %s
        ORDER BY le.orden_de_llegada
        """
        params = (titulo,)
    else:
        query = """
        SELECT le.*, p.nombre
        FROM lista_de_espera le
        JOIN persona p ON le.dni = p.dni
        ORDER BY le.titulo, le.orden_de_llegada
        """
        params = None
    
    return execute_query(query, params=params)

def check_waiting_list(numero_de_id):
    """
    Check waiting list when a book becomes available.
    Notify the next person in line if applicable.
    """
    # Get book title
    book_query = "SELECT titulo FROM libros WHERE numero_de_id = %s"
    book_params = (numero_de_id,)
    book_result = execute_query(book_query, params=book_params)
    
    if book_result.empty:
        return False
    
    titulo = book_result.iloc[0]["titulo"]
    
    # Check waiting list
    wait_query = """
    SELECT dni FROM lista_de_espera
    WHERE titulo = %s
    ORDER BY orden_de_llegada
    LIMIT 1
    """
    wait_params = (titulo,)
    wait_result = execute_query(wait_query, params=wait_params)
    
    if not wait_result.empty:
        # Book has someone waiting - notify them (implementation depends on your notification system)
        waiting_user_dni = wait_result.iloc[0]["dni"]
        
        # Here you would implement notification logic
        # For now, we'll just return the DNI of the user to notify
        return waiting_user_dni
    
    return None

def remove_from_waiting_list(dni, titulo):
    """
    Remove a user from a waiting list.
    """
    query = """
    DELETE FROM lista_de_espera
    WHERE dni = %s AND titulo = %s
    """
    params = (dni, titulo)
    return execute_query(query, params=params, is_select=False)