from prompts.prompt_engine import build_prompt
from ai.gemini_api import generate_gemini_response

def handle_query(domain: str, style: str, query: str, file_context: str = "", image_file=None) -> str:
    """
    Orchestrates the prompt building and API calling.
    """
    # Build the comprehensive prompt
    final_prompt = build_prompt(domain, style, query, file_context)
    
    # Generate response
    response_text = generate_gemini_response(final_prompt, image_file=image_file)
    
    return response_text
