# web_app.py
# Islamic Quran Bot - Arabic + English + Luganda

import streamlit as st
import requests
import json
import os

# ============ CUSTOM CSS STYLING ============
def add_custom_css():
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    h1 {
        color: #1e5631 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        font-weight: 700;
    }
    
    h2, h3 {
        color: #2d7a4f !important;
    }
    
    .verse-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 20px 0;
        border-left: 5px solid #d4af37;
    }
    
    .arabic-text {
        font-size: 28px;
        line-height: 2.5;
        text-align: right;
        color: #1e5631;
        font-family: 'Traditional Arabic', 'Arabic Typesetting', Arial, sans-serif;
        margin: 20px 0;
        direction: rtl;
    }
    
    .english-text {
        font-size: 16px;
        line-height: 1.8;
        color: #333;
        font-style: italic;
        margin: 15px 0;
        padding: 15px;
        background: #f8f9fa;
        border-radius: 8px;
    }
    
    .luganda-text {
        font-size: 16px;
        line-height: 1.8;
        color: #2d7a4f;
        font-weight: 500;
        margin: 15px 0;
        padding: 15px;
        background: #e8f5e9;
        border-radius: 8px;
        border-left: 4px solid #1e5631;
    }
    
    .verse-reference {
        color: #d4af37;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 15px;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #1e5631 0%, #2d7a4f 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        color: #1e5631;
        font-size: 14px;
        border-top: 2px solid #d4af37;
    }
    
    .custom-divider {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #d4af37, transparent);
        margin: 30px 0;
    }
    
    .info-box {
        background: #e8f5e9;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #1e5631;
        margin: 15px 0;
    }
    
    .warning-box {
        background: #fff3cd;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ============ HELPER FUNCTIONS ============

def load_luganda_verses():
    """Loads Luganda translations from JSON file"""
    try:
        with open("luganda_verses.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def get_quran_verse_multi(surah_number, verse_number):
    """Fetches Quran verse in Arabic, English, and Luganda"""
    luganda_db = load_luganda_verses()
    verse_key = f"{surah_number}:{verse_number}"
    
    arabic_url = f"https://api.alquran.cloud/v1/ayah/{surah_number}:{verse_number}/ar.alafasy"
    english_url = f"https://api.alquran.cloud/v1/ayah/{surah_number}:{verse_number}/en.sahih"
    
    try:
        arabic_resp = requests.get(arabic_url)
        english_resp = requests.get(english_url)
        
        arabic_data = arabic_resp.json()
        english_data = english_resp.json()
        
        if arabic_data.get('code') == 200 and english_data.get('code') == 200:
            arabic_verse = arabic_data['data']
            english_verse = english_data['data']
            
            luganda_text = ""
            if verse_key in luganda_db:
                luganda_text = luganda_db[verse_key]['luganda']
            
            return {
                "surah": english_verse['surah']['englishName'],
                "ayah": f"{surah_number}:{verse_number}",
                "arabic": arabic_verse['text'],
                "english": english_verse['text'],
                "luganda": luganda_text,
                "has_luganda": verse_key in luganda_db
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
        if 'arabic' in verse_data:
            f.write(f"Arabic: {verse_data['arabic']}\n")
        f.write(f"English: {verse_data['english']}\n")
        if verse_data.get('luganda'):
            f.write(f"Luganda: {verse_data['luganda']}\n")
        f.write(f"{'='*50}\n")

def load_saved_verses(filename="saved_verses.txt"):
    """Loads all saved verses from file"""
    verses = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            blocks = content.split("=" * 50)
            for block in blocks:
                if "Quran" in block and ("English" in block or "Arabic" in block):
                    verses.append(block.strip())
    return verses

def search_verses(keyword, verses):
    """Searches saved verses for a keyword"""
    results = []
    for verse in verses:
        if keyword.lower() in verse.lower():
            results.append(verse)
    return results

# ============ PAGE CONFIGURATION ============
st.set_page_config(
    page_title="🤲 Islamic Quran Bot - Arabic & Luganda",
    page_icon="🤲",
    layout="wide",
    initial_sidebar_state="expanded"
)

add_custom_css()

# ============ SIDEBAR ============
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h2 style='color: white; margin: 0;'>🤲 Menu</h2>
        <div style='border-top: 2px solid #d4af37; margin: 15px 0;'></div>
    </div>
    """, unsafe_allow_html=True)
    
    option = st.selectbox(
        "Choose a feature:",
        ["🏠 Home", "📖 Fetch Verse", "🔍 Search Verses", "📚 All Saved Verses"],
        label_visibility="collapsed"
    )
    
    st.markdown("""
    <div style='border-top: 2px solid #d4af37; margin: 20px 0;'></div>
    <div style='text-align: center; color: white; font-size: 12px; padding: 10px;'>
        🇸 Arabic | 🇬 English | 🇺 Luganda<br>
        Educational Tool
    </div>
    """, unsafe_allow_html=True)

# ============ MAIN CONTENT ============

st.markdown("""
<div style='text-align: center; padding: 30px 0;'>
    <h1 style='font-size: 48px; margin: 0;'>🤲 Islamic Quran Bot</h1>
    <p style='color: #666; font-size: 16px; margin: 10px 0;'>
        🇸🇦 Arabic | 🇬🇧 English | 🇺🇬 Luganda
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# ============ HOME PAGE ============
if option == "🏠 Home":
    st.markdown("""
    <div style='text-align: center; padding: 40px;'>
        <h2 style='color: #1e5631;'>Welcome to Islamic Quran Bot</h2>
        <p style='font-size: 18px; color: #555; line-height: 1.8;'>
            Read the Quran in Arabic (original), English, and Luganda.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🇺🇬 **Luganda Translation**: We're building the Luganda database verse by verse.")

# ============ FETCH VERSE ============
elif option == "📖 Fetch Verse":
    st.markdown("<h2>📖 Fetch Quran Verse</h2>", unsafe_allow_html=True)
    st.markdown("<p>Get verse in Arabic, English, and Luganda</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        surah = st.number_input("Surah Number", min_value=1, max_value=114, value=1)
    with col2:
        verse_num = st.number_input("Verse Number", min_value=1, max_value=300, value=1)
    
    if st.button("📖 Get Verse"):
        with st.spinner("Fetching verse..."):
            result = get_quran_verse_multi(surah, verse_num)
            
            if result:
                st.markdown(f"""
                <div class='verse-card'>
                    <div class='verse-reference'>📖 {result['surah']} {result['ayah']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style='font-weight: bold; color: #1e5631; margin: 15px 0 10px 0;'>
                    🇸🇦 Arabic (Original):
                </div>
                <div class='arabic-text'>{result['arabic']}</div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style='font-weight: bold; color: #1e5631; margin: 15px 0 10px 0;'>
                    🇬🇧 English Translation:
                </div>
                <div class='english-text'>{result['english']}</div>
                """, unsafe_allow_html=True)
                
                if result['has_luganda']:
                    st.markdown(f"""
                    <div style='font-weight: bold; color: #2d7a4f; margin: 15px 0 10px 0;'>
                        🇺🇬 Luganda Translation:
                    </div>
                    <div class='luganda-text'>{result['luganda']}</div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("🇺 **Luganda translation not available yet**")
                
                if st.button("💾 Save This Verse"):
                    save_to_file(result)
                    st.success("✅ Verse saved successfully!")
            else:
                st.error("❌ Could not fetch verse.")

# ============ SEARCH VERSES ============
elif option == "🔍 Search Verses":
    st.markdown("<h2>🔍 Search Saved Verses</h2>", unsafe_allow_html=True)
    
    keyword = st.text_input("Enter keyword:", placeholder="e.g., 'Allah', 'mercy'")
    
    if st.button("🔍 Search"):
        verses = load_saved_verses()
        if not verses:
            st.warning("⚠️ No saved verses yet.")
        else:
            results = search_verses(keyword, verses)
            if results:
                st.success(f"✅ Found {len(results)} result(s)!")
                for i, result in enumerate(results, 1):
                    st.markdown(f"<div class='verse-card'>{result}</div>", unsafe_allow_html=True)
            else:
                st.warning(f"⚠️ No verses found.")

# ============ VIEW ALL VERSES ============
elif option == "📚 All Saved Verses":
    st.markdown("<h2>📚 All Saved Verses</h2>", unsafe_allow_html=True)
    
    verses = load_saved_verses()
    if verses:
        st.success(f"✅ You have {len(verses)} saved verse(s)!")
        for verse in verses:
            st.markdown(f"<div class='verse-card'>{verse}</div>", unsafe_allow_html=True)
    else:
        st.warning("📭 No saved verses yet.")

# ============ FOOTER ============
st.markdown("""
<div class='footer'>
    <p style='margin: 0;'>
        Built with ❤️ for Islamic knowledge | 🇸🇬🇧🇬<br>
        <small>May Allah make this beneficial for all</small> 🤲
    </p>
</div>
""", unsafe_allow_html=True)