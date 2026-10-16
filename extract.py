from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3", device="cuda")  # or "cpu"

embeddings = model.encode(["Hello world", "This is a test"])
print(embeddings.shape)