import ollama
import logging

MODEL_NAME = "llama3.2:3b"
VALIDATOR_MODEL = "llama3.2:3b"  # Could use a different model if available

logger = logging.getLogger(__name__)

_ollama_available = None


def _check_ollama() -> bool:
    global _ollama_available
    if _ollama_available is not None:
        return _ollama_available
    try:
        ollama.list()
        _ollama_available = True
    except Exception:
        _ollama_available = False
    return _ollama_available


def translate_to_english(text: str, source_lang: str) -> str:
    if source_lang == "en":
        return text
    
    lang_names = {
        "hi": "Hindi",
        "bn": "Bengali",
    }
    
    lang_name = lang_names.get(source_lang, source_lang)
    
    if _check_ollama():
        prompt = f"""Translate the following {lang_name} text to English. 
Only return the English translation, nothing else.

Text to translate:
{text}"""
        
        try:
            response = ollama.chat(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.1}
            )
            return response["message"]["content"].strip()
        except Exception as e:
            logger.warning(f"Ollama translation failed: {e}. Returning original text.")
            return f"[TRANSLATION FAILED - {lang_name}] {text}"
    else:
        logger.warning("Ollama not available. Install Ollama and run 'ollama serve' for translations.")
        return f"[NO TRANSLATION - {lang_name}] {text}"


def validate_translation(original_text: str, translated_text: str, source_lang: str) -> dict:
    if source_lang == "en":
        return {"score": 100, "reason": "Original is already English"}
    
    if not _check_ollama():
        return {"score": 0, "reason": "Ollama not available for validation"}
    
    lang_names = {
        "hi": "Hindi",
        "bn": "Bengali",
    }
    lang_name = lang_names.get(source_lang, source_lang)
    
    prompt = f"""You are a translation quality evaluator. Compare the original {lang_name} text with its English translation and rate the translation quality on a scale of 0-100.

Original ({lang_name}):
{original_text}

English Translation:
{translated_text}

Evaluation criteria:
- Accuracy: Does the translation convey the same meaning?
- Completeness: Is all content translated?
- Fluency: Is the English natural and grammatically correct?
- Cultural nuance: Are idioms/expressions properly adapted?

Return ONLY a JSON object with:
{{
  "score": <integer 0-100>,
  "reason": "<brief explanation>"
}}"""
    
    try:
        response = ollama.chat(
            model=VALIDATOR_MODEL,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.1, "format": "json"}
        )
        import json
        result = json.loads(response["message"]["content"])
        return {
            "score": int(result.get("score", 0)),
            "reason": result.get("reason", "No reason provided")
        }
    except Exception as e:
        logger.warning(f"Validation failed: {e}")
        return {"score": 0, "reason": f"Validation error: {str(e)}"}


def translate_transcript_entries(entries: list, source_lang: str) -> list:
    if source_lang == "en":
        return entries
    
    full_text = " ".join([entry["text"] for entry in entries])
    translated = translate_to_english(full_text, source_lang)
    
    words = translated.split()
    total_duration = sum(entry.get("duration", 0) for entry in entries)
    words_per_entry = len(words) // len(entries) if entries else 0
    
    translated_entries = []
    word_idx = 0
    
    for entry in entries:
        entry_words = words[word_idx:word_idx + words_per_entry]
        if not entry_words and word_idx < len(words):
            entry_words = [words[word_idx]]
            word_idx += 1
        elif entry_words:
            word_idx += len(entry_words)
        
        translated_entries.append({
            "text": " ".join(entry_words),
            "start": entry.get("start", 0),
            "duration": entry.get("duration", 0)
        })
    
    if word_idx < len(words):
        translated_entries[-1]["text"] += " " + " ".join(words[word_idx:])
    
    return translated_entries