from transformers import AutoTokenizer, AutoModelForCausalLM
import os

MODEL_NAME = "gpt4all/gpt4all-model"
MODEL_DIR = "./model"

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

try:
    print("Downloading tokenizer and model...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, cache_dir=MODEL_DIR)
    print("Model downloaded successfully.")
except Exception as e:
    print(f"Error downloading the model: {e}")
