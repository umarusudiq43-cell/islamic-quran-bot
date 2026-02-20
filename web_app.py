# web_app.py
# Islamic Quran Bot - Web Interface

import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Islamic Quran Bot",
    page_icon="🤲",
    layout="centered"
)

# Title and description
st.title("🤲 Islamic Quran Bot")
st.write("Educational tool - Consult scholars for personal rulings")
st.divider()

# Sidebar menu
st.sidebar.title("Menu")
option = st.sidebar.selectbox(
    "Choose a feature:",
    ["Fetch Verse", "Search Saved Verses", "Ask Question", "View All Verses"]
)

# ============ FETCH VERSE ============
if option == "Fetch Verse":
    st.header("📖 Fetch Quran Verse")
    
    col1, col2 = st.columns(2)
    with col1:
        surah = st.number_input("Surah Number", min_value=1, max_value=114, value=1)
    with col2:
        verse = st.number_input("Verse Number", min_value=1, max_value=300, value=1)
    
    if st.button("Get Verse"):
        with st.spinner("Fetching verse..."):
            url = f"https://api.alquran.cloud/v1/ayah/{surah}:{verse}/en.sahih"
            response = requests.get(url)
            data = response.json()
            
            if data['code'] == 200:
                verse_data = data['data']
                st.success(f"**{verse_data['surah']['englishName']} {surah}:{verse}**")
                st.write(verse_data['text'])
                
                # Save button
                if st.button("Save to File"):
                    with open("saved_verses.txt", "a", encoding="utf-8") as f:
                        f.write(f"\n{'='*50}\n")
                        f.write(f"Quran {surah}:{verse}\n")
                        f.write(f"Surah: {verse_data['surah']['englishName']}\n")
                        f.write(f"Text: {verse_data['text']}\n")
                        f.write(f"{'='*50}\n")
                    st.toast("✓ Verse saved!")
            else:
                st.error("Could not fetch verse. Please check the numbers.")

# ============ SEARCH SAVED VERSES ============
elif option == "Search Saved Verses":
    st.header("🔍 Search Saved Verses")
    
    keyword = st.text_input("Enter keyword (e.g., 'Allah', 'mercy'):")
    
    if st.button("Search"):
        import os
        if os.path.exists("saved_verses.txt"):
            with open("saved_verses.txt", "r", encoding="utf-8") as f:
                content = f.read()
                blocks = content.split("=" * 50)
                results = [b.strip() for b in blocks if keyword.lower() in b.lower() and "Quran" in b]
                
                if results:
                    st.success(f"Found {len(results)} result(s)!")
                    for result in results:
                        st.info(result)
                else:
                    st.warning("No verses found.")
        else:
            st.warning("No saved verses file found. Fetch some verses first!")

# ============ ASK QUESTION ============
elif option == "Ask Question":
    st.header("🤖 Ask Islamic Question")
    
    question = st.text_input("Your question:")
    
    if st.button("Get Answer"):
        # Simple keyword-based AI
        q = question.lower()
        if "allah" in q or "god" in q:
            answer = "Allah is the One and Only God. See Ayat al-Kursi (2:255) for His attributes."
        elif "prayer" in q or "salah" in q:
            answer = "Prayer (Salah) is one of the 5 pillars of Islam. Perform it 5 times daily."
        elif "fast" in q or "ramadan" in q:
            answer = "Fasting in Ramadan is obligatory for all adult Muslims. See Quran 2:183-185."
        elif "zakat" in q or "charity" in q:
            answer = "Zakat is 2.5% of your savings given to the poor. It purifies your wealth."
        elif "patience" in q or "sabr" in q:
            answer = "Allah loves those who are patient. See Quran 2:153."
        elif "mercy" in q or "merciful" in q:
            answer = "Allah is Ar-Rahman and Ar-Raheem. See Al-Fatihah 1:1."
        else:
            answer = "I'm still learning! Try asking about Allah, prayer, fasting, zakat, patience, or mercy."
        
        st.info(f"🤖 **Bot:** {answer}")
        st.caption("⚠️ This is educational guidance. Consult a scholar for personal rulings.")

# ============ VIEW ALL VERSES ============
elif option == "View All Verses":
    st.header("📚 All Saved Verses")
    
    import os
    if os.path.exists("saved_verses.txt"):
        with open("saved_verses.txt", "r", encoding="utf-8") as f:
            content = f.read()
            blocks = content.split("=" * 50)
            verses = [b.strip() for b in blocks if "Quran" in b]
            
            if verses:
                st.success(f"You have {len(verses)} saved verse(s)!")
                for verse in verses:
                    st.markdown(verse)
                    st.divider()
            else:
                st.warning("No saved verses yet.")
    else:
        st.warning("No saved verses file found.")

# Footer
st.divider()
st.caption("Built with ❤️ for Islamic knowledge | Educational tool only")