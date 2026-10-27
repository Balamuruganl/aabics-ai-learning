from google import genai
from google.genai.types import EmbedContentConfig

client = genai.Client(
    vertexai=True,
    project="aabics-ai-learning",
    location="global"
)

def generate_embedding(text: str,  task_type: str = "RETRIEVAL_DOCUMENT") -> list[float]:

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=EmbedContentConfig(
            task_type= task_type,
            output_dimensionality=1536
        )
    )

    return response.embeddings[0].values

if __name__ == "__main__":

    sample_text = "Employees are entitled to annual leave."

    embedding = generate_embedding(sample_text)

    print("Vector dimensions:", len(embedding))
    print("First five values:", embedding[:5])