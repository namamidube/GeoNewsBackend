import psycopg2

# Connection settings for Render
host = 'dpg-cv8o5j5umphs73crc9eg-a.singapore-postgres.render.com'
port = '5432'
dbname = 'geonews'
user = 'namami'
password = 'UrKsbG9Q14HvcPp6WRNZcX4vlDvZaMEv'

try:
    # Establish connection
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    
    print("✅ Connection successful!")
    
    # Close connection
    conn.close()

except Exception as e:
    print(f"❌ Connection failed: {e}")
