from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import google.generativeai as genai

# Initialize FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Set up Gemini API Key
genai.configure(api_key="YOUR_API_KEY")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "response": ""})

@app.post("/generate", response_class=HTMLResponse)
async def generate_response(request: Request, prompt: str = Form(...)):
    try:
        # Call Gemini API
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        result = response.text  # Extract the response text
        return templates.TemplateResponse("index.html", {"request": request, "response": result})
    except Exception as e:
        return templates.TemplateResponse(
            "index.html", {"request": request, "response": f"Error: {str(e)}"}
        )
