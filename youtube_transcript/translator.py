import json
import logging
import re

import ollama

MODEL_NAME = "llama3.2:3b"

VALIDATOR_MODEL = "llama3.2:3b"

TRANSLATION_CHUNK_SIZE = 6000

logger = logging.getLogger(__name__)

_ollama_available = None


def _check_ollama() -> bool:
    global _ollama_available

    if _ollama_available is not None:
        return _ollama_available

    try:
        ollama.list()
        _ollama_available = True
    except Exception as error:
        logger.warning("Ollama unavailable: %s", error)
        _ollama_available = False

    return _ollama_available


def _split_text_into_chunks(
    text: str,
    max_chars: int = TRANSLATION_CHUNK_SIZE,
) -> list[str]:
    if not text:
        return []

    paragraphs = re.split(r"\n\s*\n", text)

    chunks = []
    current = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        if len(paragraph) > max_chars:
            sentences = re.split(r"(?<=[.!?।])\s+", paragraph)

            for sentence in sentences:
                sentence = sentence.strip()

                if not sentence:
                    continue

                if len(current) + len(sentence) + 1 <= max_chars:
                    if current:
                        current += " "

                    current += sentence
                else:
                    if current:
                        chunks.append(current.strip())

                    current = sentence

            continue

        if len(current) + len(paragraph) + 2 <= max_chars:
            if current:
                current += "\n\n"

            current += paragraph
        else:
            if current:
                chunks.append(current.strip())

            current = paragraph

    if current:
        chunks.append(current.strip())

    return chunks


def _translate_chunk(
    text: str,
    source_lang: str,
) -> str:
    lang_names = {
        "hi": "Hindi",
        "bn": "Bengali",
    }

    lang_name = lang_names.get(source_lang, source_lang)

    prompt = f"""
Translate the following {lang_name} transcript into natural English.

Rules:
- Preserve the original meaning.
- Do not summarize.
- Do not omit information.
- Do not add information.
- Preserve names, technical terms, numbers and examples.
- Return ONLY the English translation.

Transcript:
{text}
""".strip()

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        options={
            "temperature": 0.1,
        },
    )

    return response["message"]["content"].strip()


def translate_to_english(
    text: str,
    source_lang: str,
) -> str:
    if source_lang == "en":
        return text

    if not text.strip():
        return ""

    if not _check_ollama():
        raise RuntimeError("Ollama is not available. Start Ollama before translating.")

    chunks = _split_text_into_chunks(text)

    if not chunks:
        return ""

    translated_chunks = []
    total = len(chunks)

    print(f"Translating {total} chunk(s)...")

    for index, chunk in enumerate(chunks, start=1):
        print(f"  Translating chunk {index}/{total}...")

        try:
            translated = _translate_chunk(chunk, source_lang)
            translated_chunks.append(translated)
        except Exception as error:
            logger.warning("Translation failed for chunk %s: %s", index, error)
            raise RuntimeError(
                f"Translation failed on chunk {index}/{total}: {error}"
            ) from error

    return "\n\n".join(translated_chunks).strip()


def validate_translation(
    original_text: str,
    translated_text: str,
    source_lang: str,
) -> dict:
    if source_lang == "en":
        return {
            "score": 100,
            "reason": "Original is already English",
        }

    if not _check_ollama():
        return {
            "score": 0,
            "reason": "Ollama not available for validation",
        }

    lang_names = {
        "hi": "Hindi",
        "bn": "Bengali",
    }

    lang_name = lang_names.get(source_lang, source_lang)

    validation_limit = 12000

    original_for_validation = original_text[:validation_limit]
    translated_for_validation = translated_text[:validation_limit]

    prompt = f"""
You are a translation quality evaluator.

Compare the original {lang_name} text with
its English translation.

Original:
{original_for_validation}

English translation:
{translated_for_validation}

Evaluate:

1. Accuracy
2. Completeness
3. Fluency
4. Preservation of meaning
5. Preservation of important details

Return ONLY valid JSON:

{{
  "score": <integer from 0 to 100>,
  "reason": "<brief explanation>"
}}
""".strip()

    try:
        response = ollama.chat(
            model=VALIDATOR_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            options={
                "temperature": 0.1,
                "format": "json",
            },
        )

        content = response["message"]["content"].strip()
        result = json.loads(content)

        score = int(result.get("score", 0))
        score = max(0, min(100, score))

        reason = result.get("reason", "No reason provided")

        return {
            "score": score,
            "reason": str(reason),
        }
    except Exception as error:
        logger.warning("Translation validation failed: %s", error)

        return {
            "score": 0,
            "reason": f"Validation error: {error}",
        }


def translate_transcript_entries(
    entries: list,
    source_lang: str,
) -> list:
    if source_lang == "en":
        return entries

    if not entries:
        return []

    if not _check_ollama():
        raise RuntimeError("Ollama is not available.")

    groups = []
    current_group = []
    current_length = 0

    for entry in entries:
        text = entry.get("text", "").strip()

        if not text:
            continue

        if current_group and current_length + len(text) > TRANSLATION_CHUNK_SIZE:
            groups.append(current_group)
            current_group = []
            current_length = 0

        current_group.append(entry)
        current_length += len(text) + 1

    if current_group:
        groups.append(current_group)

    translated_entries = []
    total_groups = len(groups)

    for group_index, group in enumerate(groups, start=1):
        source_text = " ".join(entry["text"] for entry in group)

        print(f"Translating timestamp group {group_index}/{total_groups}...")

        translated_text = _translate_chunk(source_text, source_lang)

        translated_words = translated_text.split()

        original_lengths = [max(1, len(entry["text"])) for entry in group]

        total_original_length = sum(original_lengths)

        word_index = 0

        for entry_index, entry in enumerate(group):
            if entry_index == len(group) - 1:
                assigned_words = translated_words[word_index:]
            else:
                ratio = original_lengths[entry_index] / total_original_length
                assigned_count = max(1, round(len(translated_words) * ratio))
                assigned_words = translated_words[
                    word_index : word_index + assigned_count
                ]
                word_index += len(assigned_words)

            translated_entries.append(
                {
                    "text": " ".join(assigned_words),
                    "start": entry.get("start", 0),
                    "duration": entry.get("duration", 0),
                }
            )

    return translated_entries
