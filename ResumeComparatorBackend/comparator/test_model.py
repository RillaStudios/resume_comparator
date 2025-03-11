# Load model directly
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from sentence_transformers import SentenceTransformer
sentences = ["This is an example sentence", "Each sentence is converted"]

model = SentenceTransformer('models/msmarco-distilbert-base-tas-b-resume-fit-v2-epoch-3')

embeddings = model.encode(sentences)

print(embeddings)
