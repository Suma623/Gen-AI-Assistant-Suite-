import os
import google.generativeai as genai
from dotenv import load_dotenv
from utils.constants import MODEL_NAME

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

def generate_gemini_response(prompt_text: str, image_file=None) -> str:
    """
    Calls the Gemini API. 
    Handles pure text OR text + image using gemini-2.5-flash.
    """
    if not API_KEY:
        return "⚠️ Error: Gemini API Key is missing. Please check your .env file."
        
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        
        if image_file:
            # If an image is passed (PIL Image or direct file representation that Gemini accepts)
            response = model.generate_content([prompt_text, image_file])
        else:
            response = model.generate_content(prompt_text)
            
        return response.text
    except Exception as e:
        return f"⚠️ Error generating response from Gemini: {str(e)}\nPlease try again later."
