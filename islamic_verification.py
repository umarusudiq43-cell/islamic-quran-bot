# islamic_verification.py
# Extra safety layer for AI Islamic answers

def verify_islamic_answer(answer):
    """
    Basic verification checks for Islamic answers
    
    Returns: dict with verification status and warnings
    """
    warnings = []
    
    # Check for problematic phrases
    red_flags = [
        "i think",  # AI shouldn't give personal opinions on Islamic rulings
        "in my opinion",
        "probably",
        "maybe halal",  # Should be definitive or recommend scholar
        "maybe haram"
    ]
    
    answer_lower = answer.lower()
    for flag in red_flags:
        if flag in answer_lower:
            warnings.append(f"⚠️ Contains uncertain language: '{flag}'")
    
    # Check if recommends scholar (good practice)
    if "consult" not in answer_lower and "scholar" not in answer_lower:
        warnings.append("ℹ️ Consider adding: 'Consult a scholar for personal rulings'")
    
    # Check for Quran/Hadith references (encouraged)
    if "quran" not in answer_lower and "hadith" not in answer_lower:
        warnings.append("ℹ️ Consider adding Quran/Hadith references")
    
    return {
        'verified': len(warnings) == 0,
        'warnings': warnings
    }