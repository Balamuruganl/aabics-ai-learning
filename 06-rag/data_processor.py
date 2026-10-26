from pdf_reader import extract_pdf_text
from chunker import split_into_chunks
#from embedder import generate_embedding
from store_chunks import store_chunks_in_db

pdf_path = "documents/Organic_Shop_HR_Policies_Draft.pdf"

def processor():
    # Extract text from the PDF
    full_text = extract_pdf_text(pdf_path)

    # Split the extracted text into chunks
    chunks = split_into_chunks(full_text, chunk_size=1000, overlap=200)

    # Generate embeddings for each chunk
    #embeddings = [generate_embedding(chunk) for chunk in chunks]

    # Print the number of chunks and the first chunk for verification
    print(f"Number of chunks: {len(chunks)}")
    #print(f"First chunk: {chunks[0]}")
    store_chunks_in_db(chunks,"Organic_Shop_HR_Policies_Draft.pdf")


if __name__ == "__main__":
    processor()