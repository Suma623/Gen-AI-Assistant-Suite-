def get_suggested_prompts(domain: str):
    """Returns a list of suggested prompts depending on the selected domain."""
    suggestions = {
        "Education": [
            "Create a 5-question pop quiz on World War II.",
            "Summarize the key differences between mitosis and meiosis.",
            "Generate flashcards for learning basic Python syntax."
        ],
        "Healthcare": [
            "Explain the common symptoms of seasonal allergies.",
            "Suggest a balanced diet plan for high blood pressure.",
            "What are general precautions when taking antibiotics?"
        ],
        "Finance": [
            "Explain the difference between a SIP and a Fixed Deposit.",
            "Give me 5 practical tips for personal budget planning.",
            "What is compound interest and how does it work?"
        ],
        "Marketing": [
            "Write an engaging Instagram caption for a new coffee brand.",
            "Generate 3 ad copy variations for a summer shoe sale.",
            "List 5 campaign ideas to increase email newsletter signups."
        ]
    }
    
    return suggestions.get(domain, ["Ask a question..."])
