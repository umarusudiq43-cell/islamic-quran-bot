# web_app.py
# Islamic Quran Bot - Beautiful Customized Version

import streamlit as st
import requests
import os

# ============ CUSTOM CSS STYLING ============
def add_custom_css():
    st.markdown("""
    <style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Header styling */
    h1 {
        color: #1e5631 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        font-weight: 700;
    }
    
    h2, h3 {
        color: #2d7a4f !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1e5631;
        color: white;
    }
    
    .sidebar-content {
        background-color: #1e5631;
    }
    
    /* Card styling */
    .verse-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 20px 0;
        border-left: 5px solid #d4af37;
    }
    
    .verse-text {
        font-size: 18px;
        line-height: 2;
        color: #333;
        font-style: italic;
        margin: 20px 0;
    }
    
    .verse-reference {
        color: #1e5631;
        font-weight: bold;
        font-size: 16px;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #1e5631 0%, #2d7a4f 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2d7a4f 0%, #1e5631 100%);
        box-shadow: 0 4px 15px rgba(30, 86, 49, 0.3);
        transform: translateY(-2px);
    }
    
    /* Info boxes */
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
    
    .success-box {
        background: #d4edda;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 15px 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        color: #1e5631;
        font-size: 14px;
        border-top: 2px solid #d4af37;
    }
    
    /* Divider */
    .custom-divider {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #d4af37, transparent);
        margin: 30px 0;
    }
    
    /* Search box */
    .stTextInput>div>div>input {
        border: 2px solid #d4af37;
        border-radius: 8px;
    }
    
    /* Number input */
    .stNumberInput>div>div>input {
        border: 2px solid #d4af37;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# ============ HELPER FUNCTIONS ============

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
        return None

def save_to_file(verse_data, filename="saved_verses.txt"):
    """Saves a verse to a text file"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Quran {verse_data['ayah']}\n")
        f.write(f"Surah: {verse_data['surah']}\n")
        f.write(f"Text: {verse_data['text']}\n")
        f.write(f"{'='*50}\n")

def load_saved_verses(filename="saved_verses.txt"):
    """Loads all saved verses from file"""
    verses = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
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

def get_ai_response(question):
    """Simple AI responses for Islamic questions"""
    question = question.lower()
    
    responses = {
        "allah": "Allah is the One and Only God. See Ayat al-Kursi (2:255) for His attributes.",
        "god": "Allah is the One and Only God. See Ayat al-Kursi (2:255) for His attributes.",
        "prayer": "Prayer (Salah) is one of the 5 pillars of Islam. Perform it 5 times daily.",
        "salah": "Prayer (Salah) is one of the 5 pillars of Islam. Perform it 5 times daily.",
        "fast": "Fasting in Ramadan is obligatory for all adult Muslims. See Quran 2:183-185.",
        "ramadan": "Fasting in Ramadan is obligatory for all adult Muslims. See Quran 2:183-185.",
        "zakat": "Zakat is 2.5% of your savings given to the poor. It purifies your wealth.",
        "charity": "Zakat is 2.5% of your savings given to the poor. It purifies your wealth.",
        "patience": "Allah loves those who are patient. See Quran 2:153: 'Seek help through patience and prayer.'",
        "sabr": "Allah loves those who are patient. See Quran 2:153: 'Seek help through patience and prayer.'",
        "mercy": "Allah is Ar-Rahman (The Merciful) and Ar-Raheem (The Especially Merciful). See Al-Fatihah 1:1.",
        "merciful": "Allah is Ar-Rahman (The Merciful) and Ar-Raheem (The Especially Merciful). See Al-Fatihah 1:1.",
        "help": "I can help you: (1) Fetch Quran verses, (2) Search saved verses, (3) Answer basic Islamic questions."
    }
    
    for key, value in responses.items():
        if key in question:
            return value
    
    return "I'm still learning! Try asking about Allah, prayer, fasting, zakat, patience, or mercy."

# ============ PAGE CONFIGURATION ============
st.set_page_config(
    page_title="🤲 Islamic Quran Bot",
    page_icon="🤲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
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
        ["🏠 Home", "📖 Fetch Verse", "🔍 Search Verses", "🤖 Ask Question", "📚 All Saved Verses"],
        label_visibility="collapsed"
    )
    
    st.markdown("""
    <div style='border-top: 2px solid #d4af37; margin: 20px 0;'></div>
    <div style='text-align: center; color: white; font-size: 12px; padding: 10px;'>
        Educational Tool<br>
        Consult scholars for rulings
    </div>
    """, unsafe_allow_html=True)

# ============ MAIN CONTENT ============

# Header
st.markdown("""
<div style='text-align: center; padding: 30px 0;'>
    <h1 style='font-size: 48px; margin: 0;'>🤲 Islamic Quran Bot</h1>
    <p style='color: #666; font-size: 16px; margin: 10px 0;'>
        Your companion for Quranic knowledge and Islamic guidance
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
            A beautiful tool to explore the Quran, save your favorite verses, 
            and learn about Islam.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='verse-card' style='text-align: center;'>
            <h3 style='color: #1e5631;'>📖 Read Quran</h3>
            <p>Fetch any verse from the Holy Quran with English translation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='verse-card' style='text-align: center;'>
            <h3 style='color: #1e5631;'>🔍 Search</h3>
            <p>Search through your saved verses by keywords</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='verse-card' style='text-align: center;'>
            <h3 style='color: #1e5631;'>🤖 Ask AI</h3>
            <p>Get quick answers to basic Islamic questions</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box' style='text-align: center; margin-top: 40px;'>
        <strong>📚 Start your journey by selecting an option from the sidebar!</strong>
    </div>
    """, unsafe_allow_html=True)

# ============ FETCH VERSE ============
elif option == "📖 Fetch Verse":
    st.markdown("<h2>📖 Fetch Quran Verse</h2>", unsafe_allow_html=True)
    st.markdown("<p>Enter the Surah and Verse number to fetch from the Quran</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        surah = st.number_input("Surah Number", min_value=1, max_value=114, value=1, 
                                help="Enter Surah number (1-114)")
    with col2:
        verse_num = st.number_input("Verse Number", min_value=1, max_value=300, value=1,
                                   help="Enter Verse number")
    
    if st.button(" Get Verse"):
        with st.spinner("Fetching verse from the Quran..."):
            result = get_quran_verse(surah, verse_num)
            
            if result:
                st.markdown(f"""
                <div class='verse-card'>
                    <div class='verse-reference'>📖 {result['surah']} {result['ayah']}</div>
                    <div class='verse-text'>{result['text']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("💾 Save This Verse"):
                    save_to_file(result)
                    st.success("✅ Verse saved successfully!")
            else:
                st.error("❌ Could not fetch verse. Please check the numbers.")

# ============ SEARCH VERSES ============
elif option == "🔍 Search Verses":
    st.markdown("<h2>🔍 Search Saved Verses</h2>", unsafe_allow_html=True)
    st.markdown("<p>Search through your saved verses by keyword</p>", unsafe_allow_html=True)
    
    keyword = st.text_input("Enter keyword (e.g., 'Allah', 'mercy', 'prayer'):", 
                           placeholder="Type your search term...")
    
    if st.button("🔍 Search"):
        verses = load_saved_verses()
        if not verses:
            st.warning("⚠️ No saved verses yet. Fetch some verses first!")
        else:
            results = search_verses(keyword, verses)
            if results:
                st.success(f"✅ Found {len(results)} result(s)!")
                for i, result in enumerate(results, 1):
                    st.markdown(f"""
                    <div class='verse-card'>
                        <div style='color: #666; font-size: 14px;'>Result {i}</div>
                        {result}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(f"⚠️ No verses found matching '{keyword}'")

# ============ ASK QUESTION ============
elif option == "🤖 Ask Question":
    st.markdown("<h2>🤖 Ask Islamic Question</h2>", unsafe_allow_html=True)
    st.markdown("<p>Get quick answers to basic Islamic questions</p>", unsafe_allow_html=True)
    
    question = st.text_input("Your question:", 
                            placeholder="e.g., What is prayer? How many times do we pray?")
    
    if st.button("💬 Get Answer"):
        if question:
            with st.spinner("Thinking..."):
                answer = get_ai_response(question)
                st.markdown(f"""
                <div class='info-box'>
                    <strong>🤖 Bot:</strong><br>
                    {answer}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class='warning-box'>
                    <strong>⚠️ Disclaimer:</strong> This is educational guidance only. 
                    For personal rulings, please consult a qualified scholar.
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter a question first.")

# ============ VIEW ALL VERSES ============
elif option == "📚 All Saved Verses":
    st.markdown("<h2>📚 All Saved Verses</h2>", unsafe_allow_html=True)
    st.markdown("<p>View all the verses you've saved</p>", unsafe_allow_html=True)
    
    verses = load_saved_verses()
    if verses:
        st.success(f"✅ You have {len(verses)} saved verse(s)!")
        for i, verse in enumerate(verses, 1):
            st.markdown(f"""
            <div class='verse-card'>
                <div style='color: #d4af37; font-size: 14px; margin-bottom: 10px;'>
                    ⭐ Saved Verse {i}
                </div>
                {verse}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='warning-box' style='text-align: center; padding: 40px;'>
            <h3 style='color: #856404;'>📭 No saved verses yet</h3>
            <p>Start by fetching verses from the Quran using the "Fetch Verse" option!</p>
        </div>
        """, unsafe_allow_html=True)

# ============ FOOTER ============
st.markdown("""
<div class='footer'>
    <p style='margin: 0;'>
        Built with ❤️ for Islamic knowledge | Educational tool only<br>
        <small>May Allah make this beneficial for all</small> 🤲
    </p>
</div>
""", unsafe_allow_html=True)