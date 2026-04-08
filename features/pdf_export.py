from fpdf import FPDF
import io

def create_pdf(domain: str, timestamp: str, query: str, response: str):
    """
    Generates a PDF bytes object containing the chat details.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'GenAI Assistant Suite - Report', ln=True, align='C')
    pdf.ln(5)
    
    # Metadata
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 6, f"Domain: {domain}", ln=True)
    pdf.cell(0, 6, f"Time: {timestamp}", ln=True)
    pdf.ln(10)
    
    # Query
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, "User Query:", ln=True)
    pdf.set_font('Arial', '', 11)
    
    # UTF-8 handling workaround for FPDF by replacing problematic chars
    safe_query = query.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, safe_query)
    pdf.ln(5)
    
    # Response
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, "AI Response:", ln=True)
    pdf.set_font('Arial', '', 11)
    
    safe_response = response.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, safe_response)
    
    # Output to bytes
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    return pdf_bytes
