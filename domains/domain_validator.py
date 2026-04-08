def validate_domain_mismatch(domain: str, query: str) -> str:
    """
    Very lightweight intent/keyword classifier to detect if the user asked a question 
    that belongs to a different domain.
    Returns a warning message if a mismatch is strongly suspected, else empty string.
    """
    query_lower = query.lower()
    
    # Define lightweight keyword sets
    healthcare_keywords = {"symptom", "disease", "treatment", "pain", "medical", "doctor", "hospital", "cancer", "diabetes", "headache", "fever", "pill"}
    finance_keywords = {"stock", "investment", "return", "interest rate", "budget", "sip", "fd", "mutual fund", "loan", "tax", "portfolio"}
    education_keywords = {"homework", "quiz", "syllabus", "exam", "student", "teacher", "class", "lecture", "study", "algebra", "calculus"}
    marketing_keywords = {"seo", "campaign", "ad copy", "social media", "conversion", "click", "lead generation", "branding", "instagram"}

    def matches_keywords(text: str, keywords: set) -> bool:
        return any(kw in text for kw in keywords)

    # Check for obvious mismatches
    if domain != "Healthcare" and matches_keywords(query_lower, healthcare_keywords):
        return "⚠️ This question seems related to Healthcare. You might get better results by switching the domain to 'Healthcare'."
        
    if domain != "Finance" and matches_keywords(query_lower, finance_keywords):
        return "⚠️ This question seems related to Finance. You might get better results by switching the domain to 'Finance'."
        
    if domain != "Marketing" and matches_keywords(query_lower, marketing_keywords):
        return "⚠️ This question seems related to Marketing. You might get better results by switching the domain to 'Marketing'."
        
    if domain != "Education" and matches_keywords(query_lower, education_keywords):
        return "⚠️ This question seems related to Education. You might get better results by switching the domain to 'Education'."
        
    return ""
