# smart_quran_bot.py
# Islamic Quran Bot with Search & AI Features

import requests
import json
import os

# ============ QURAN API FUNCTIONS ============

def get_quran_verse(surah_number, verse_number):
    """Fetches a Quran verse in English"""
    url = f"https://api.alquran.cloud/v1/ayah/{surah_number}:{verse_number}/en.sahih"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('code') == 200:
            verse = data['data']
            return {
                "surah": verse['surah']['englishName'],
                "ayah": f"{surah_number}:{verse_number}",
                "text": verse['text']
            }
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_to_file(verse_data, filename="saved_verses.txt"):
    """Saves a verse to a text file"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Quran {verse_data['ayah']}\n")
        f.write(f"Surah: {verse_data['surah']}\n")
        f.write(f"Text: {verse_data['text']}\n")
        f.write(f"{'='*50}\n")
    print(f"✓ Verse saved to {filename}")

def load_saved_verses(filename="saved_verses.txt"):
    """Loads all saved verses from file"""
    verses = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            # Split by separator
            blocks = content.split("=" * 50)
            for block in blocks:
                if "Quran" in block and "Text:" in block:
                    verses.append(block.strip())
    return verses

def search_verses(keyword, verses):
    """Searches saved verses for a keyword"""
    results = []
    for verse in verses:
        if keyword.lower() in verse.lower():
            results.append(verse)
    return results

# ============ SIMPLE AI RESPONSES ============

def get_ai_response(question):
    """
    Simple rule-based AI responses
    (Later we'll add a real LLM)
    """
    question = question.lower()
    
    # Keyword-based responses
    if "allah" in question or "god" in question:
        return "Allah is the One and Only God. See Ayat al-Kursi (2:255) for His attributes."
    elif "prayer" in question or "salah" in question:
        return "Prayer (Salah) is one of the 5 pillars of Islam. Perform it 5 times daily."
    elif "fast" in question or "ramadan" in question:
        return "Fasting in Ramadan is obligatory for all adult Muslims. See Quran 2:183-185."
    elif "zakat" in question or "charity" in question:
        return "Zakat is 2.5% of your savings given to the poor. It purifies your wealth."
    elif "patience" in question or "sabr" in question:
        return "Allah loves those who are patient. See Quran 2:153: 'O you who believe, seek help through patience and prayer.'"
    elif "mercy" in question or "merciful" in question:
        return "Allah is Ar-Rahman (The Merciful) and Ar-Raheem (The Especially Merciful). See Al-Fatihah 1:1."
    elif "help" in question:
        return "I can help you: (1) Fetch Quran verses, (2) Search saved verses, (3) Answer basic Islamic questions."
    else:
        return "I'm still learning! Try asking about Allah, prayer, fasting, zakat, patience, or mercy."

# ============ MENU SYSTEM ============

def show_main_menu():
    print("\n" + "="*60)
    print("         ISLAMIC QURAN BOT - SMART EDITION")
    print("="*60)
    print("1. Fetch a Quran verse by reference")
    print("2. Search saved verses")
    print("3. Ask an Islamic question")
    print("4. View all saved verses")
    print("5. Exit")
    print("="*60)

def main():
    print("\n*** Welcome to the Islamic Quran Bot ***")
    print("Educational tool - Consult scholars for personal rulings\n")
    
    while True:
        show_main_menu()
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            # Fetch verse by reference
            try:
                surah = int(input("Enter Surah number (1-114): "))
                verse = int(input("Enter Verse number: "))
                result = get_quran_verse(surah, verse)
                if result:
                    print(f"\n--- {result['surah']} {result['ayah']} ---")
                    print(result['text'])
                    print()
                    save = input("Save this verse? (y/n): ").lower()
                    if save == "y":
                        save_to_file(result)
                else:
                    print("Could not fetch verse.")
            except ValueError:
                print("Please enter valid numbers.")
        
        elif choice == "2":
            # Search saved verses
            verses = load_saved_verses()
            if not verses:
                print("No saved verses yet. Fetch some verses first!")
                continue
            
            keyword = input("Enter search keyword (e.g., 'Allah', 'mercy'): ")
            results = search_verses(keyword, verses)
            
            if results:
                print(f"\n✓ Found {len(results)} result(s):\n")
                for i, result in enumerate(results, 1):
                    print(f"--- Result {i} ---")
                    print(result)
                    print()
            else:
                print("No verses found matching that keyword.")
        
        elif choice == "3":
            # Ask Islamic question
            question = input("\nAsk your Islamic question: ")
            answer = get_ai_response(question)
            print(f"\n🤖 Bot: {answer}")
            print("\n⚠️  This is educational guidance. Consult a scholar for personal rulings.")
        
        elif choice == "4":
            # View all saved verses
            verses = load_saved_verses()
            if verses:
                print(f"\n📚 You have {len(verses)} saved verse(s):\n")
                for verse in verses:
                    print(verse)
                    print()
            else:
                print("No saved verses yet.")
        
        elif choice == "5":
            print("\nMay Allah bless you! Goodbye.\n")
            break
        
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()