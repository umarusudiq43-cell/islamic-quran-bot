# quran_menu.py
# A simple menu to fetch different Quran verses

import requests
import json

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

def show_menu():
    """Displays the menu of available verses"""
    print("\n" + "="*50)
    print("       ISLAMIC QURAN VERSE MENU")
    print("="*50)
    print("1. Al-Fatihah 1:1 (The Opening)")
    print("2. Al-Baqarah 2:255 (Ayat al-Kursi)")
    print("3. Al-Ikhlas 112:1-4 (The Sincerity)")
    print("4. Al-Falaq 113:1-5 (The Daybreak)")
    print("5. An-Nas 114:1-6 (The Mankind)")
    print("6. Exit")
    print("7. Al-Baqarah 2:286 (Allah's Mercy)")
    print("8. Az-Zumar 39:53 (Don't Despair)")
    print("="*50)

def main():
    """Main program loop"""
    print("\n*** Welcome to the Islamic Quran Bot ***\n")
    
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            verse = get_quran_verse(1, 1)
        elif choice == "2":
            verse = get_quran_verse(2, 255)
        elif choice == "3":
            verse = get_quran_verse(112, 1)
        elif choice == "4":
            verse = get_quran_verse(113, 1)
        elif choice == "5":
            verse = get_quran_verse(114, 1)
        elif choice == "2":
            print("\nMay Allah bless you! Goodbye.\n")
        elif choice == "7":
            verse = get_quran_verse(2, 286)
        elif choice == "8":
            verse = get_quran_verse(39, 53)
            break
        else:
            print("Invalid choice. Please enter 1-6.")
            continue
        
        if verse:
            print(f"\n--- {verse['surah']} {verse['ayah']} ---")
            print(verse['text'])
            print()
            
            # Ask if user wants to save
            save = input("Save this verse to file? (y/n): ").lower()
            if save == "y":
                save_to_file(verse)
        else:
            print("Could not fetch verse. Please try again.")

if __name__ == "__main__":
    main()