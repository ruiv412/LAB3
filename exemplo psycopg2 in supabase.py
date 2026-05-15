import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # carrega o ficheiro .env

# exemplo #
#("postgresql://postgres.abc:password@://aws-0-us-east-1.pooler.supabase.com")#
# Use the session pooler connection string (Port 5432)

conn_str = os.getenv("DATABASE_URL")
try:
    conn = psycopg2.connect(conn_str)
    print("Successfully connected!")
except psycopg2.OperationalError as e:
    print(f"Connection failed: {e}")

cur = conn.cursor()
cur.execute("SELECT version();")
print("só para eu saber a versão do postgreSQL que estou a usar:")
print(cur.fetchone())
cur.close()
####################################################################
try:
    with conn.cursor() as cur:
        # SQL statement with placeholders
        insert_query = "INSERT INTO tasks(id, title, description, completed) VALUES (%s, %s, %s, %s);"
        record_to_insert = (1, "Teste1", "a ver se funciona", False)
        
        cur.execute(insert_query, record_to_insert)
        
        # IMPORTANT: commit the changes
        conn.commit()
        print("Data inserted successfully!")
except Exception as e:
    print(f"Error: {e}")


##################################################################

conn.close()



