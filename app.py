from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

# Initialize FastAPI app and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Model details
MODEL_NAME = "./model"
tokenizer = None
model = None

# Load model and tokenizer
def load_model():
    global tokenizer, model
    try:
        os.makedirs(MODEL_NAME, exist_ok=True)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")

load_model()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the front-end form."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate_response(request: Request, prompt: str = Form(...)):
    """Generate response for a given prompt."""
    if not tokenizer or not model:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "Model not loaded. Please check the backend."},
        )

    try:
        # Tokenize input and generate response
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(inputs["input_ids"], max_length=200, num_return_sequences=1)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Render response
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "prompt": prompt, "response": response},
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html", {"request": request, "error": str(e)}
        )
