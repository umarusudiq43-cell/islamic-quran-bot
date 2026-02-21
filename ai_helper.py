# ai_helper.py
# Ollama AI Integration for Islamic Q&A

import ollama
import json

# ============ ISLAMIC SYSTEM PROMPT ============
# This ensures AI gives accurate, Islamic-appropriate answers

ISLAMIC_SYSTEM_PROMPT = """
You are an Islamic knowledge assistant. Your role is to provide accurate, beneficial Islamic information based on Quran and Sunnah.

IMPORTANT GUIDELINES:
1. Always base answers on Quran and authentic Hadith when possible
2. If you're uncertain about a ruling, say "Consult a qualified scholar for this matter"
3. Never give personal fatwas - always recommend consulting local scholars
4. Be respectful, clear, and beneficial in your responses
5. If asked about something outside Islamic knowledge, politely redirect
6. Always include Quran/Hadith references when relevant
7. Acknowledge when there are scholarly differences of opinion
8. Prioritize mainstream Sunni scholarship (Ahlus Sunnah wal Jama'ah)

FORMAT YOUR ANSWERS:
- Start with the main ruling/answer
- Provide evidence (Quran verse or Hadith if known)
- Mention if there are scholarly differences
- End with recommendation to consult scholar for personal matters

LANGUAGE: Respond in the same language as the question (English, Arabic, or Luganda if possible).

DISCLAIMER: Always remind users this is educational, not a substitute for scholarly fatwas.
"""

def get_ai_answer(question, model="llama3"):
    """
    Get AI answer from Ollama with Islamic guidelines
    
    Args:
        question (str): User's question
        model (str): Ollama model to use (default: llama3)
    
    Returns:
        dict: Contains answer, success status, and any error message
    """
    try:
        # Call Ollama API
        response = ollama.chat(
            model=model,
            messages=[
                {
                    'role': 'system',
                    'content': ISLAMIC_SYSTEM_PROMPT
                },
                {
                    'role': 'user',
                    'content': question
                }
            ],
            options={
                'temperature': 0.3,  # Lower = more focused, less creative
                'num_predict': 500,  # Max tokens in response
            }
        )
        
        answer = response['message']['content']
        
        return {
            'success': True,
            'answer': answer,
            'model': model,
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'answer': None,
            'model': model,
            'error': str(e)
        }

def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        # Try to list local models
        ollama.list()
        return True
    except:
        return False

def get_available_models():
    """Get list of installed Ollama models"""
    try:
        models = ollama.list()
        return [m['name'] for m in models['models']]
    except:
        return []

# ============ TRANSLATION HELPER ============

def translate_answer(answer, target_language="luganda"):
    """
    Translate AI answer to another language using Ollama
    
    Args:
        answer (str): Original answer (English)
        target_language (str): Target language (luganda, arabic, etc.)
    
    Returns:
        str: Translated text
    """
    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    'role': 'system',
                    'content': f"You are a professional translator. Translate the following Islamic text to {target_language}. Maintain accuracy and respect for religious terminology."
                },
                {
                    'role': 'user',
                    'content': answer
                }
            ],
            options={'temperature': 0.3}
        )
        
        return response['message']['content']
        
    except Exception as e:
        print(f"Translation error: {e}")
        return answer  # Return original if translation fails