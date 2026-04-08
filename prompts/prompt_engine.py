from prompts.education_prompt import get_education_prompt
from prompts.healthcare_prompt import get_healthcare_prompt
from prompts.finance_prompt import get_finance_prompt
from prompts.marketing_prompt import get_marketing_prompt
from prompts.style_prompts import get_style_prompt

def build_prompt(domain: str, style: str, query: str, file_context: str = "") -> str:
    """
    Combines the domain persona, style instructions, optional file context, and the user query
    into a final robust system + user prompt for Gemini.
    """
    
    # 1. Base Domain Prompt
    if domain == "Education":
        system_prompt = get_education_prompt()
    elif domain == "Healthcare":
        system_prompt = get_healthcare_prompt()
    elif domain == "Finance":
        system_prompt = get_finance_prompt()
    elif domain == "Marketing":
        system_prompt = get_marketing_prompt()
    else:
        system_prompt = "You are a helpful AI assistant."

    # 2. Add Style Modifier
    style_prompt = get_style_prompt(style)
    
    # 3. Assemble components
    final_prompt = f"{system_prompt}\n\nSTYLE INSTRUCTIONS: {style_prompt}\n\n"
    
    if file_context:
        final_prompt += f"--- START OF ATTACHED FILE CONTEXT ---\n{file_context}\n--- END OF ATTACHED FILE CONTEXT ---\n\n"
        final_prompt += "Please consider the attached file context when answering the query.\n\n"
        
    final_prompt += f"USER QUERY:\n{query}"
    
    return final_prompt
