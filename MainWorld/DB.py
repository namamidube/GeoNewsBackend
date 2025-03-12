import psycopg2

def connect_db():
    """Function to connect to the database and return the connection and cursor."""
    try:
        conn = psycopg2.connect(database="geonews", 
                                user="namami", 
                                host="dpg-cv8o5j5umphs73crc9eg-a.singapore-postgres.render.com", 
                                password="UrKsbG9Q14HvcPp6WRNZcX4vlDvZaMEv", 
                                port=5432)
        return conn, conn.cursor()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None, None


def insert_cluster(place_name, latitude, longitude, country):
    conn, cur = connect_db()
    if conn is None:
        return

    try:
        place_name = place_name.title()

        cur.execute("SELECT COUNT(*) FROM clusters_world WHERE place_name = %s;", (place_name,))
        count = cur.fetchone()[0]

        if count == 0:
            insert_query = """
            INSERT INTO clusters_world (place_name, latitude, longitude, country)
            VALUES (%s, %s, %s, %s);
            """
            cur.execute(insert_query, (place_name, latitude, longitude, country))
            conn.commit()
            print(f"{place_name} cluster inserted successfully.")
        else:
            print(f"{place_name} cluster already exists in the database.")
    except Exception as e:
        print(f"Error inserting cluster '{place_name}': {e}")
    finally:
        cur.close()
        conn.close()


def insert_article(title, summary, source_url, published_date, keyword, category, image, country):
    conn, cur = connect_db()
    if conn is None:
        return

    try:
        keyword = keyword.title()
        title = title.strip()

        # Check if the cluster exists
        cur.execute("SELECT cluster_id FROM clusters_world WHERE place_name = %s;", (keyword,))
        cluster = cur.fetchone()

        if not cluster:
            print(f"Cluster for place '{keyword}' not found.")
            return

        cluster_id = cluster[0]

        # Check if the title already exists
        cur.execute("SELECT 1 FROM articles_world WHERE title = %s;", (title,))
        if cur.fetchone():
            print(f"Skipping insertion. Article with title '{title}' already exists.")
            return

        # Insert the article if title is unique
        insert_query = """
        INSERT INTO articles_world (cluster_id, title, summary, source_url, published_date, keyword, category, image_url, country)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, (cluster_id, title, summary, source_url, published_date, keyword, category, image, country))
        conn.commit()

        print(f"Article '{title}' inserted successfully into the database.")
    except Exception as e:
        print(f"Error inserting article '{title}': {e}")
    finally:
        cur.close()
        conn.close()


def insert_general_article(title, summary, source_url, published_date, category, image):
    conn, cur = connect_db()
    if conn is None:
        return

    try:
        title = title.strip()

        # Check if the title already exists
        cur.execute("SELECT 1 FROM general_article_world WHERE title = %s;", (title,))
        if cur.fetchone():
            print(f"Skipping insertion. General article with title '{title}' already exists.")
            return

        # Insert the general article if title is unique
        insert_query = """
        INSERT INTO general_article_world (title, summary, source_url, published_date, category, image_url)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, (title, summary, source_url, published_date, category, image))
        conn.commit()

        print(f"General article '{title}' inserted successfully into the database.")
    except Exception as e:
        print(f"Error inserting general article '{title}': {e}")
    finally:
        cur.close()
        conn.close()

