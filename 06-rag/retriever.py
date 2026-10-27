import os

import psycopg
from pgvector.psycopg import register_vector
from pgvector import Vector
from embedder import generate_embedding

def retrieve_chunks(question: str, top_k: int = 5):

    # 1. Convert the question into an embedding
    question_embedding = generate_embedding(
        question,
        task_type="RETRIEVAL_QUERY"
    )
    question_embedding = Vector(question_embedding)
    
    # 2. Connect to PostgreSQL through the Cloud SQL Auth Proxy
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

            # 3. Find the most similar document chunks
            cursor.execute(
                """
                SELECT
                    id,
                    document_name,
                    chunk_number,
                    content,
                    embedding <=> %s AS distance
                FROM document_chunks
                ORDER BY embedding <=> %s
                LIMIT %s
                """,
                (question_embedding, question_embedding, top_k)
            )

            results = cursor.fetchall()

        # 4. Return the retrieved chunks
        return [
            {
                "id": row[0],
                "document_name": row[1],
                "chunk_number": row[2],
                "content": row[3],
                "distance": row[4]
            }
            for row in results
        ]

    finally:
        connection.close()

if __name__ == "__main__":

    question = "How much annual earned leave are employees entitled to?"

    results = retrieve_chunks(question)

    for result in results:
        print(f"\nDocument: {result['document_name']}")
        print(f"Chunk number: {result['chunk_number']}")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Content:\n{result['content']}")