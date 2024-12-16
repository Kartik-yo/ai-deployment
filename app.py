from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

app = Flask(__name__)

# Load the GPT4ALL model
MODEL_NAME = "gpt4all/gpt4all-model"
MODEL_PATH = "./model"

tokenizer = None
model = None

try:
    # Ensure model directory exists
    os.makedirs(MODEL_PATH, exist_ok=True)
    
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=MODEL_PATH)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, cache_dir=MODEL_PATH)
    print("Model and tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading model or tokenizer: {e}")

@app.route("/generate", methods=["POST"])
def generate():
    """
    Generate a response to a prompt using GPT4ALL.
    Expects JSON input: { "prompt": "Your prompt here" }
    """
    if tokenizer is None or model is None:
        return jsonify({"error": "Model or tokenizer not loaded"}), 500

    try:
        data = request.json
        prompt = data.get("prompt", "")
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Generate response
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(inputs["input_ids"], max_length=200, num_return_sequences=1)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
