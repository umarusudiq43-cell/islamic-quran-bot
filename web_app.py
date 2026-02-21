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
    font-size: 48px !important;  /* ← Much larger! */
    line-height: 3.2 !important;  /* ← Better spacing */
    text-align: right !important;
    color: #1e5631 !important;
    font-family: 'Traditional Arabic', 'Arabic Typesetting', Arial, sans-serif !important;
    margin: 25px 0 !important;
    direction: rtl !important;
    font-weight: 600 !important;  /* ← Bolder */
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
        /* ============ MOBILE OPTIMIZATION ============ */
    
    /* Responsive adjustments for tablets and phones */
    @media (max-width: 768px) {
        /* Adjust header size */
        h1 {
            font-size: 32px !important;
        }
        
        h2 {
            font-size: 24px !important;
        }
        
        /* Make cards more compact */
        .verse-card, .hadith-card, .aqeedah-card {
            padding: 20px !important;
            margin: 15px 0 !important;
        }
        
        /* Arabic text slightly smaller on mobile but still readable */
        .arabic-text {
            font-size: 36px !important;
            line-height: 2.8 !important;
        }
        
        /* Make buttons larger for touch */
        .stButton>button {
            padding: 15px 40px !important;
            font-size: 16px !important;
            min-height: 50px !important;
        }
        
        /* Adjust columns to stack on mobile */
        .stColumns {
            flex-direction: column !important;
        }
        
        /* Sidebar adjustments */
        section[data-testid="stSidebar"] {
            width: 280px !important;
        }
        
        /* Make input fields larger for touch */
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input {
            font-size: 16px !important;
            min-height: 45px !important;
        }
        
        /* Topic tags */
        .topic-tag {
            padding: 8px 20px !important;
            font-size: 14px !important;
        }
        
        /* Footer */
        .footer {
            font-size: 12px !important;
            padding: 15px !important;
        }
    }
    
    /* Extra small phones */
    @media (max-width: 480px) {
        h1 {
            font-size: 26px !important;
        }
        
        h2 {
            font-size: 20px !important;
        }
        
        .arabic-text {
            font-size: 30px !important;
        }
        
        .verse-card, .hadith-card, .aqeedah-card {
            padding: 15px !important;
        }
        
        /* Full width buttons on very small screens */
        .stButton>button {
            width: 100% !important;
        }
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
    # ============ AI KNOWLEDGE FUNCTIONS ============

def load_islamic_knowledge():
    """Load Islamic knowledge base"""
    try:
        with open("islamic_knowledge.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"topics": {}, "common_questions": []}

def ai_search_answer(question, knowledge_db):
    """Smart AI search that finds relevant topics"""
    question_lower = question.lower()
    
    # Check common questions first
    for qa in knowledge_db.get("common_questions", []):
        for keyword in qa["keywords"]:
            if keyword in question_lower:
                topic_key = qa["answer_topic"]
                if topic_key in knowledge_db.get("topics", {}):
                    return knowledge_db["topics"][topic_key]
    
    # Search topic keywords
    for topic_key, topic_data in knowledge_db.get("topics", {}).items():
        if (topic_key in question_lower or 
            topic_data.get("english", "").lower()[:50] in question_lower):
            return topic_data
    
    # No match found
    return None

def get_topic_suggestions(knowledge_db):
    """Get list of available topics for navigation"""
    topics = []
    for key, data in knowledge_db.get("topics", {}).items():
        topics.append({
            "key": key,
            "title": data.get("english", "").split(" ")[0],  # First word
            "arabic": data.get("arabic", "")
        })
    return topics

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
    layout="centered",  # Changed from "wide" to "centered" for mobile
    initial_sidebar_state="collapsed"  # Sidebar collapsed by default on mobile
)

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
        ["🏠 Home", "📖 Quran", "📚 Hadith", "🕌 Aqeedah", "🤖 AI Q&A","🔍 Search All", "💾 My Saved"],
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
            # Mobile-friendly tip
    st.markdown("""
    <div class='info-box' style='text-align: center;'>
        <strong>📱 Mobile Tip:</strong> Tap the menu icon (☰) to access all sections!
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
            # ============ AI Q&A SECTION ============
elif section == "🤖 AI Q&A":
    st.markdown("<h2>🤖 Ask Islamic Questions</h2>", unsafe_allow_html=True)
    
    knowledge_db = load_islamic_knowledge()
    
    # Show topic suggestions
    st.markdown("### 💡 Popular Topics:")
    topics = get_topic_suggestions(knowledge_db)
    
    # Display topic chips
    cols = st.columns(3)
    for i, topic in enumerate(topics[:6]):  # Show first 6
        with cols[i % 3]:
            if st.button(f"{topic['arabic']} {topic['title']}"):
                st.session_state.selected_topic = topic['key']
    
    # Check if topic selected from chips
    if 'selected_topic' in st.session_state:
        topic_data = knowledge_db["topics"].get(st.session_state.selected_topic)
        if topic_data:
            st.markdown(f"""
            <div class='aqeedah-card'>
                <div class='verse-reference'>🕌 {topic_data['english'].split(' ')[0]}</div>
                <div style='font-weight:bold;color:#1e5631;margin:15px 0 10px 0'>
                    🇸🇦 {topic_data['arabic']}:
                </div>
                <div class='arabic-text'>{topic_data['english']}</div>
                <div style='font-weight:bold;color:#1e5631;margin:15px 0 10px 0'>
                    🇬🇧 English:
                </div>
                <div class='english-text'>{topic_data['english']}</div>
            """, unsafe_allow_html=True)
            
            if topic_data.get('luganda'):
                st.markdown(f"""
                <div style='font-weight:bold;color:#2d7a4f;margin:15px 0 10px 0'>
                    🇺🇬 Luganda:
                </div>
                <div class='luganda-text'>{topic_data['luganda']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("</div>", unsafe_allow_html=True)
            
            if topic_data.get('quran_refs'):
                st.caption(f"📖 References: {', '.join(topic_data['quran_refs'])}")
            
            if st.button("✅ Got It!"):
                st.session_state.selected_topic = None
    
    st.markdown("---")
    
    # Ask question input
    st.markdown("### ❓ Or Ask Your Question:")
    question = st.text_input(
        "Type your question:",
        placeholder="e.g., How many times do we pray? What is Zakat?",
        label_visibility="collapsed"
    )
    
    if st.button("🔍 Get Answer"):
        if question:
            with st.spinner("🤖 Thinking..."):
                answer = ai_search_answer(question, knowledge_db)
                
                if answer:
                    st.success("✅ Found relevant answer!")
                    st.markdown(f"""
                    <div class='aqeedah-card'>
                        <div style='font-weight:bold;color:#1e5631;margin:15px 0 10px 0'>
                            🇸🇦 Arabic:
                        </div>
                        <div class='arabic-text'>{answer['arabic']}</div>
                        <div style='font-weight:bold;color:#1e5631;margin:15px 0 10px 0'>
                            🇬🇧 English:
                        </div>
                        <div class='english-text'>{answer['english']}</div>
                    """, unsafe_allow_html=True)
                    
                    if answer.get('luganda'):
                        st.markdown(f"""
                        <div style='font-weight:bold;color:#2d7a4f;margin:15px 0 10px 0'>
                            🇺🇬 Luganda:
                        </div>
                        <div class='luganda-text'>{answer['luganda']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    if answer.get('quran_refs'):
                        st.caption(f"📖 Quran: {', '.join(answer['quran_refs'])}")
                    if answer.get('hadith_refs'):
                        st.caption(f"📚 Hadith: {', '.join(answer['hadith_refs'])}")
                else:
                    st.warning("⚠️ I'm still learning! Try asking about: Prayer, Fasting, Zakat, Hajj, Tawheed, Patience, Charity, Parents, Truthfulness, or Repentance.")
                    st.info("💡 Tip: Browse the topic chips above for quick answers!")
        else:
            st.warning("⚠️ Please type a question first.")
    
    st.markdown("""
    <div class='warning-box'>
        <strong>⚠️ Disclaimer:</strong> This is educational guidance only. 
        For personal fatwas, consult a qualified scholar.
    </div>
    """, unsafe_allow_html=True)
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