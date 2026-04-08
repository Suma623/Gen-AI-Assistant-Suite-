import pypdf
from PIL import Image
import io

def extract_text_from_pdf(file_bytes) -> str:
    """Extracts text from a PDF file."""
    try:
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error extracting PDF text: {str(e)}"

def extract_text_from_txt(file_bytes) -> str:
    """Extracts text from a basic txt file."""
    try:
        return file_bytes.decode('utf-8').strip()
    except Exception as e:
        return f"Error reading text file: {str(e)}"

def handle_uploaded_file(uploaded_file):
    """
    Given a Streamlit UploadedFile, returns (extracted_text, image_object, file_type, error).
    """
    if uploaded_file is None:
        return "", None, None, None

    file_name = uploaded_file.name
    file_bytes = uploaded_file.read()
    
    # Avoid reading images as text
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        try:
            image = Image.open(io.BytesIO(file_bytes))
            return "", image, "image", None
        except Exception as e:
            return "", None, "image", f"Failed to load image: {str(e)}"
            
    # Handle Text / PDF
    elif file_name.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_bytes)
        return text, None, "pdf", None
        
    elif file_name.lower().endswith('.txt'):
        text = extract_text_from_txt(file_bytes)
        return text, None, "txt", None
        
    else:
        return "", None, "unknown", "Unsupported file type. Please upload PDF, TXT, or Images (JPG/PNG)."
