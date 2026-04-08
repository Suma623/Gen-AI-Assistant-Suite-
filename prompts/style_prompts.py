def get_style_prompt(style: str) -> str:
    styles = {
        "Default": "Provide a balanced and naturally flowing response.",
        "Simple": "Explain using simple language, suitable for a 10-year-old.",
        "Detailed": "Provide an in-depth, comprehensive explanation covering all nuances.",
        "Bullet Points": "Format the response strictly as a list of bullet points.",
        "Professional": "Use formal, corporate, and highly professional language.",
        "Beginner Friendly": "Assume the user has zero prior knowledge. Start with the basics.",
        "Exam Style": "Structure the response like an exam answer, highlighting key definitions and concepts."
    }
    return styles.get(style, styles["Default"])
