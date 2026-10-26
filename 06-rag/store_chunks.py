import os
import psycopg
from pgvector.psycopg import register_vector
from embedder import generate_embedding

def store_chunks_in_db(chunks: list[str], document_name: str):
    connection = psycopg.connect(
        host="127.0.0.1",
        port=5432,
        dbname="organic_shop",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

    try:
        register_vector(connection)
        
        with connection.cursor() as cursor:
            for chunk_number, chunk in enumerate(chunks, start=1):
                embedding = generate_embedding(chunk)
                cursor.execute(
                    "INSERT INTO document_chunks (document_name,chunk_number,content, embedding) VALUES (%s,%s,%s, %s)",
                    (document_name,chunk_number,chunk, embedding)
                )

    # Commit all inserted chunks
        connection.commit()

        print(f"Successfully stored {len(chunks)} chunks.")

    except Exception as e:
        connection.rollback()
        print(f"Error storing chunks: {e}")
    finally:
        connection.close()

    
    
    
    

    
    

