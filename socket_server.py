import socket
import pyodbc

# MSSQL připojení
conn_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=your_sql_server.database.windows.net;"
    "DATABASE=your_database;"
    "UID=your_username;"
    "PWD=your_password;"
)
conn = pyodbc.connect(conn_string)
cursor = conn.cursor()

# Funkce pro uložení dat do MSSQL
def save_to_db(values):
    try:
        query = """
        INSERT INTO cdr_table (
            historyid, callid, duration, time_start, time_answered, time_end, reason_terminated, 
            from_no, to_no, from_dn, to_dn, dial_no, reason_changed, final_number, final_dn, 
            bill_code, bill_rate, bill_cost, bill_name, chain, from_type, to_type, final_type, 
            from_dispname, to_dispname, final_dispname, missed_queue_calls
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, *values)
        conn.commit()
        print("Uloženo:", values)
    except Exception as e:
        print(f"Chyba při ukládání: {e}")

# Socket server
HOST = "0.0.0.0"  # Naslouchá na všech IP
PORT = 5000       # Port pro příjem dat

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server naslouchá na {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        with conn:
            print(f"Připojeno z {addr}")
            data = conn.recv(4096).decode("utf-8")  # Předpokládá se větší buffer
            if data:
                # Předpokládáme, že data jsou oddělená čárkami
                values = data.split(",")
                if len(values) == 27:  # Počet sloupců v CDR
                    save_to_db(values)
                else:
                    print("Nesprávný formát dat:", data)
