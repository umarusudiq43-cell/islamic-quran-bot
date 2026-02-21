# ai_helper.py
# Fallback AI helper for cloud deployment (works without Ollama)

import json

def check_ollama_running():
    """Check if Ollama is running (always False for cloud compatibility)"""
    try:
        import ollama
        ollama.list()
        return True
    except:
        return False

def get_available_models():
    """Get list of Ollama models (empty if not available)"""
    try:
        import ollama
        models = ollama.list()
        return [m['name'] for m in models['models']]
    except:
        return []

def get_ai_answer(question, model="llama3"):
    """
    Get answer from JSON knowledge base (fallback for cloud)
    If Ollama is available locally, it will use that instead
    """
    # Try Ollama first (for local use)
    if check_ollama_running():
        try:
            import ollama
            response = ollama.chat(
                model=model,
                messages=[
                    {'role': 'system', 'content': 'You are an Islamic knowledge assistant. Provide accurate answers based on Quran and Sunnah. Recommend consulting scholars for personal rulings.'},
                    {'role': 'user', 'content': question}
                ],
                options={'temperature': 0.3, 'num_predict': 500}
            )
            return {
                'success': True,
                'answer': response['message']['content'],
                'model': model,
                'source': 'ollama'
            }
        except Exception as e:
            print(f"Ollama error: {e}")
    
    # Fallback to JSON knowledge base
    try:
        with open("islamic_knowledge.json", "r", encoding="utf-8") as f:
            knowledge_db = json.load(f)
        
        question_lower = question.lower()
        
        # Check common questions
        for qa in knowledge_db.get("common_questions", []):
            for keyword in qa["keywords"]:
                if keyword in question_lower:
                    topic_key = qa["answer_topic"]
                    if topic_key in knowledge_db.get("topics", {}):
                        topic = knowledge_db["topics"][topic_key]
                        answer = f"""**{topic.get('english', '')}**

🇸🇦 Arabic: {topic.get('arabic', '')}

🇬🇧 English: {topic.get('english', '')}

🇺🇬 Luganda: {topic.get('luganda', 'Coming soon')}

📖 References: {', '.join(topic.get('quran_refs', []))}"""
                        return {
                            'success': True,
                            'answer': answer,
                            'model': 'json',
                            'source': 'json'
                        }
        
        return {
            'success': False,
            'answer': None,
            'model': 'json',
            'source': 'json',
            'error': 'Topic not found in knowledge base. Try: prayer, fasting, zakat, hajj, tawheed, patience, charity'
        }
    except Exception as e:
        return {'success': False, 'answer': None, 'error': str(e), 'source': 'json'}