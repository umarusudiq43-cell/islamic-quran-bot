# get_verse.py
import requests

def get_quran_verse(surah_number, verse_number):
    """
    Fetches a Quran verse in English (Sahih International translation)
    """
    url = f"https://api.alquran.cloud/v1/ayah/{surah_number}:{verse_number}/en.sahih"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('code') == 200:
            verse = data['data']
            print(f"\nQuran {surah_number}:{verse_number}")
            print(f"Text: {verse['text']}")
            print(f"Surah: {verse['surah']['englishName']}")
            return True
        else:
            print("Could not fetch verse. Please check the numbers.")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        print("Tip: Make sure you're connected to the internet.")
        return False

if __name__ == "__main__":
    print("Fetching Al-Fatihah, verse 1...\n")
    get_quran_verse(2, 255)