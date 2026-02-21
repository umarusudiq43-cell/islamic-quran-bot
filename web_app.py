# web_app.py
# Islamic Quran Bot - Quran + Hadith + Aqeedah (Arabic/English/Luganda)

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
    .verse-card, .hadith-card, .aqeedah-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 20px 0;
        border-left: 5px solid #d4af37;
    }
    .arabic-text {
    font-size: 40px;  /* ← Increased from 28px to 40px */
    line-height: 3;   /* ← Increased for better spacing */
    text-align: right;
    color: #1e5631;
    font-family: 'Traditional Arabic', 'Arabic Typesetting', Arial, sans-serif;
    margin: 20px 0;
    direction: rtl;
    font-weight: 500;  /* ← Slightly bolder for clarity */
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
    .narrator {
        font-size: 14px;
        color: #666;
        font-style: italic;
        margin: 10px 0;
    }
    .topic-tag {
        display: inline-block;
        background: #d4af37;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        margin: 5px 0;
    }
    .verse-reference, .hadith-reference {
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

# ============ LOAD DATABASES ============

def load_luganda_verses():
    try:
        with open("luganda_verses.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("verses", data)
    except:
        return {}

def load_hadith_db():
    try:
        with open("hadith_db.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"hadiths": {}}

def load_aqeedah_db():
    try:
        with open("aqeedah_db.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"articles_of_faith": [], "tawheed_basics": []}

# ============ QURAN FUNCTIONS ============

def get_quran_verse_multi(surah_number, verse_number):
    luganda_db = load_luganda_verses()
    verse_key = f"{surah_number}:{verse_number}"
    
    # ✅ FIXED: Removed extra spaces in URLs
    arabic_url = f"https://api.alquran.cloud/v1/ayah/{surah_number}:{verse_number}/ar.alafasy"
    english_url = f"https://api.alquran.cloud/v1/ayah/{surah_number}:{verse_number}/en.sahih"
    
    try:
        arabic_resp = requests.get(arabic_url)
        english_resp = requests.get(english_url)
        
        if arabic_resp.json().get('code') == 200 and english_resp.json().get('code') == 200:
            arabic_data = arabic_resp.json()['data']
            english_data = english_resp.json()['data']
            
            luganda_text = luganda_db.get(verse_key, {}).get('luganda', '')
            
            return {
                "surah": english_data['surah']['englishName'],
                "ayah": f"{surah_number}:{verse_number}",
                "arabic": arabic_data['text'],
                "english": english_data['text'],
                "luganda": luganda_text,
                "has_luganda": bool(luganda_text)
            }
    except Exception as e:
        print(f"Quran Error: {e}")
    return None

# ============ HADITH FUNCTIONS ============

def get_hadith_by_id(hadith_id, hadith_db):
    return hadith_db.get("hadiths", {}).get(hadith_id)

def search_hadiths(keyword, hadith_db):
    results = []
    for hid, hadith in hadith_db.get("hadiths", {}).items():
        if (keyword.lower() in hadith.get('english', '').lower() or
            keyword.lower() in hadith.get('luganda', '').lower() or
            keyword.lower() in hadith.get('topic', '').lower()):
            results.append((hid, hadith))
    return results

# ============ AQEEDAH FUNCTIONS ============

def get_aqeedah_items(aqeedah_db):
    articles = aqeedah_db.get("articles_of_faith", [])
    tawheed = aqeedah_db.get("tawheed_basics", [])
    return articles + tawheed

def search_aqeedah(keyword, aqeedah_db):
    results = []
    for item in get_aqeedah_items(aqeedah_db):
        if (keyword.lower() in item.get('title_english', '').lower() or
            keyword.lower() in item.get('content_english', '').lower() or
            keyword.lower() in item.get('title_luganda', '').lower()):
            results.append(item)
    return results

# ============ SAVE FUNCTIONS ============

def save_quran_verse(verse_data):
    with open("saved_quran.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\n[QURAN] {verse_data['ayah']}\n")
        f.write(f"Surah: {verse_data['surah']}\n")
        f.write(f"Arabic: {verse_data['arabic']}\n")
        f.write(f"English: {verse_data['english']}\n")
        if verse_data.get('luganda'):
            f.write(f"Luganda: {verse_data['luganda']}\n")

def save_hadith(hadith_data):
    with open("saved_hadith.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\n[HADITH] {hadith_data['id']}\n")
        f.write(f"Narrator: {hadith_data['narrator']}\n")
        f.write(f"Topic: {hadith_data['topic']}\n")
        f.write(f"Arabic: {hadith_data['arabic']}\n")
        f.write(f"English: {hadith_data['english']}\n")
        if hadith_data.get('luganda'):
            f.write(f"Luganda: {hadith_data['luganda']}\n")

def save_aqeedah(aqeedah_data):
    with open("saved_aqeedah.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\n[AQEEDAH] {aqeedah_data['title_english']}\n")
        f.write(f"Arabic: {aqeedah_data['content_arabic']}\n")
        f.write(f"English: {aqeedah_data['content_english']}\n")
        if aqeedah_data.get('content_luganda'):
            f.write(f"Luganda: {aqeedah_data['content_luganda']}\n")

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="🤲 Tawheed Academy Bot",
    page_icon="🤲",
    layout="wide",
    initial_sidebar_state="expanded"
)
add_custom_css()

# ============ SIDEBAR ============
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h2 style='color: white; margin: 0;'>🤲 Tawheed Academy</h2>
        <div style='border-top: 2px solid #d4af37; margin: 15px 0;'></div>
    </div>
    """, unsafe_allow_html=True)
    
    section = st.selectbox(
        "Choose a section:",
        ["🏠 Home", "📖 Quran", "📚 Hadith", "🕌 Aqeedah", "🔍 Search All", "💾 My Saved"],
        label_visibility="collapsed"
    )
    
    st.markdown("""
    <div style='border-top: 2px solid #d4af37; margin: 20px 0;'></div>
    <div style='text-align: center; color: white; font-size: 12px; padding: 10px;'>
        🇸🇦 Arabic | 🇬🇧 English | 🇺🇬 Luganda<br>
        Educational Tool | Consult scholars for fatwas
    </div>
    """, unsafe_allow_html=True)

# ============ HEADER ============
st.markdown("""
<div style='text-align: center; padding: 30px 0;'>
    <h1 style='font-size: 48px; margin: 0;'>🤲 Tawheed Academy Bot</h1>
    <p style='color: #666; font-size: 16px; margin: 10px 0;'>
        🇸🇦 Arabic | 🇬🇧 English | 🇺🇬 Luganda
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# ============ HOME ============
if section == "🏠 Home":
    st.markdown("""
    <div style='text-align: center; padding: 40px;'>
        <h2 style='color: #1e5631;'>Welcome to Tawheed Academy</h2>
        <p style='font-size: 18px; color: #555; line-height: 1.8;'>
            Learn Quran, Hadith, and Aqeedah in Arabic, English, and Luganda.
            A comprehensive Islamic knowledge platform.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='verse-card' style='text-align: center;'>
            <h3>📖 Quran</h3>
            <p>Read verses in 3 languages with beautiful formatting</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='hadith-card' style='text-align: center;'>
            <h3>📚 Hadith</h3>
            <p>Learn from Sahih Bukhari & Muslim in your language</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='aqeedah-card' style='text-align: center;'>
            <h3>🕌 Aqeedah</h3>
            <p>Understand the 6 Articles of Faith & Tawheed</p>
        </div>
        """, unsafe_allow_html=True)

# ============ QURAN SECTION ============
elif section == "📖 Quran":
    st.markdown("<h2>📖 Fetch Quran Verse</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        surah = st.number_input("Surah", 1, 114, 1)
    with col2:
        verse = st.number_input("Verse", 1, 300, 1)
    
    if st.button("📖 Get Verse"):
        with st.spinner("Fetching..."):
            result = get_quran_verse_multi(surah, verse)
            if result:
                st.markdown(f"""
                <div class='verse-card'>
                    <div class='verse-reference'>📖 {result['surah']} {result['ayah']}</div>
                    <div style='font-weight:bold;color:#1e5631'>🇸🇦 Arabic:</div>
                    <div class='arabic-text'>{result['arabic']}</div>
                    <div style='font-weight:bold;color:#1e5631'>🇬🇧 English:</div>
                    <div class='english-text'>{result['english']}</div>
                """, unsafe_allow_html=True)
                if result['has_luganda']:
                    st.markdown(f"""
                    <div style='font-weight:bold;color:#2d7a4f'>🇺 Luganda:</div>
                    <div class='luganda-text'>{result['luganda']}</div></div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.info("🇺🇬 Luganda translation coming soon!")
                
                if st.button("💾 Save"):
                    save_quran_verse(result)
                    st.success("✅ Saved!")
            else:
                st.error("❌ Could not fetch verse")

# ============ HADITH SECTION ============
elif section == "📚 Hadith":
    st.markdown("<h2>📚 Hadith Collection</h2>", unsafe_allow_html=True)
    
    hadith_db = load_hadith_db()
    hadith_ids = list(hadith_db.get("hadiths", {}).keys())
    
    if hadith_ids:
        selected_id = st.selectbox("Select a Hadith:", hadith_ids)
        hadith = get_hadith_by_id(selected_id, hadith_db)
        
        if hadith:
            st.markdown(f"### 📚 {hadith['id']}")
            st.markdown(f"**🗣️ Narrator:** {hadith['narrator']}")
            st.markdown(f"<span class='topic-tag'>🏷️ {hadith['topic']}</span>", unsafe_allow_html=True)
            st.markdown("")  # Empty line
            
            # Arabic
            st.markdown("**🇸🇦 Arabic:**")
            st.markdown(f"<p class='arabic-text'>{hadith['arabic']}</p>", unsafe_allow_html=True)
            
            # English
            st.markdown("**🇬🇧 English:**")
            st.info(hadith['english'])
            
            # Luganda
            if hadith.get('luganda'):
                st.markdown("**🇺🇬 Luganda:**")
                st.success(hadith['luganda'])
            
            if st.button("💾 Save Hadith"):
                save_hadith(hadith)
                st.success("✅ Hadith saved!")
    else:
        st.info("📚 Hadith database is being built. Check back soon!")
# ============ AQEEDAH SECTION ============
elif section == "🕌 Aqeedah":
    st.markdown("<h2>🕌 Islamic Creed (Aqeedah)</h2>", unsafe_allow_html=True)
    
    aqeedah_db = load_aqeedah_db()
    items = get_aqeedah_items(aqeedah_db)
    
    if items:
        selected = st.selectbox("Select a topic:", [i['title_english'] for i in items])
        item = next((i for i in items if i['title_english'] == selected), None)
        
        if item:
            st.markdown(f"### 🕌 {item['title_english']}")
            
            # Arabic
            st.markdown(f"**🇸🇦 {item['title_arabic']}:**")
            st.markdown(f"<p class='arabic-text'>{item['content_arabic']}</p>", unsafe_allow_html=True)
            
            # English
            st.markdown("**🇬 English:**")
            st.info(item['content_english'])
            
            # Luganda
            if item.get('content_luganda'):
                st.markdown(f"**🇺 {item['title_luganda']}:**")
                st.success(item['content_luganda'])
            
            # Reference
            if item.get('quran_ref'):
                st.caption(f"📖 Reference: {item['quran_ref']}")
            
            if st.button("💾 Save Aqeedah"):
                save_aqeedah(item)
                st.success("✅ Saved!")
    else:
        st.info("🕌 Aqeedah content is being prepared.")
# ============ SEARCH ALL ============
elif section == "🔍 Search All":
    st.markdown("<h2>🔍 Search Islamic Knowledge</h2>", unsafe_allow_html=True)
    
    keyword = st.text_input("Search keyword:", placeholder="e.g., 'Allah', 'prayer', 'faith'")
    
    if st.button("🔍 Search"):
        results_found = False
        
        if os.path.exists("saved_quran.txt"):
            with open("saved_quran.txt", "r", encoding="utf-8") as f:
                if keyword.lower() in f.read().lower():
                    st.markdown("<div class='verse-card'>📖 Found in Quran</div>", unsafe_allow_html=True)
                    results_found = True
        
        hadith_db = load_hadith_db()
        hadith_results = search_hadiths(keyword, hadith_db)
        if hadith_results:
            st.markdown(f"<div class='hadith-card'>📚 Found {len(hadith_results)} Hadith(s)</div>", unsafe_allow_html=True)
            for hid, hadith in hadith_results:
                st.markdown(f"""
                <div class='hadith-card'>
                    <strong>{hadith['id']}</strong> - {hadith['topic']}<br>
                    <em>{hadith['english'][:100]}...</em>
                </div>
                """, unsafe_allow_html=True)
            results_found = True
        
        aqeedah_db = load_aqeedah_db()
        aqeedah_results = search_aqeedah(keyword, aqeedah_db)
        if aqeedah_results:
            st.markdown(f"<div class='aqeedah-card'>🕌 Found {len(aqeedah_results)} Aqeedah topic(s)</div>", unsafe_allow_html=True)
            for item in aqeedah_results:
                st.markdown(f"""
                <div class='aqeedah-card'>
                    <strong>{item['title_english']}</strong><br>
                    <em>{item['content_english'][:100]}...</em>
                </div>
                """, unsafe_allow_html=True)
            results_found = True
        
        if not results_found:
            st.warning("⚠️ No results found. Try different keywords.")

# ============ MY SAVED ============
elif section == "💾 My Saved":
    st.markdown("<h2>💾 My Saved Content</h2>", unsafe_allow_html=True)
    
    saved_files = {
        "📖 Quran": "saved_quran.txt",
        "📚 Hadith": "saved_hadith.txt", 
        "🕌 Aqeedah": "saved_aqeedah.txt"
    }
    
    for label, filename in saved_files.items():
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip():
                    with st.expander(f"{label} ({filename})"):
                        st.markdown(f"<pre>{content}</pre>", unsafe_allow_html=True)
        else:
            st.info(f"{label}: Nothing saved yet")

# ============ FOOTER ============
st.markdown("""
<div class='footer'>
    <p style='margin:0'>
        Built with ❤️ for Islamic knowledge | 🇸🇬🇧🇬<br>
        <small>Educational tool only | Consult scholars for personal rulings 🤲</small>
    </p>
</div>
""", unsafe_allow_html=True)