# add_luganda_verses.py
# Helper script to add Luganda translations easily

import json
import os

def load_luganda_db(filename="luganda_verses.json"):
    """Load existing Luganda database"""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"metadata": {"language": "Luganda", "verses": {}}, "verses": {}}

def add_verse(surah, verse, luganda_text, surah_name, surah_name_luganda="", verified=True):
    """Add a single verse to the database"""
    db = load_luganda_db()
    
    verse_key = f"{surah}:{verse}"
    db["verses"][verse_key] = {
        "luganda": luganda_text,
        "surah_name": surah_name,
        "surah_name_luganda": surah_name_luganda,
        "verified": verified
    }
    
    # Update metadata
    db["metadata"]["total_verses"] = len(db["verses"])
    
    # Save
    with open("luganda_verses.json", "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Added {verse_key}: {luganda_text[:50]}...")

# Example usage:
if __name__ == "__main__":
    # Add Al-Fatihah 1:1-7
    add_verse(1, 1, "Mu linnya lya Allah, Omusaasira, Omusaasira ennyo", "Al-Fatiha", "Okutandika")
    add_verse(1, 2, "Ensiimbi zonna za Allah, Omusaasira, Omusaasira ennyo", "Al-Fatiha", "Okutandika")
    # Add more as you get translations...
    
    print("🎉 Done! Check luganda_verses.json")