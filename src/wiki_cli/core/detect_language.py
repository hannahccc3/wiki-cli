"""
Language detection via Unicode script ranges + Latin-language pattern heuristics.

Supports 20+ major languages. Returns an English language name string.

Reference: nashsu/llm_wiki/src/lib/detect-language.ts
"""

import re
from typing import Optional


def detect_language(text: str) -> str:
    """Detect the primary language of a text string based on Unicode script ranges.

    Supports: Chinese, Japanese, Korean, Arabic, Hebrew, Hindi, Bengali, Tamil,
    Telugu, Kannada, Malayalam, Gujarati, Punjabi, Burmese, Khmer, Lao,
    Georgian, Armenian, Ethiopic, Tibetan, Sinhala, Cyrillic (Russian), Greek,
    and all major Latin-script languages (English, French, German, Spanish,
    Portuguese, Italian, Dutch, Swedish, Norwegian, Danish, Finnish, Polish,
    Czech, Hungarian, Romanian, Turkish, Vietnamese, Indonesian, Swahili).

    Returns an English language name (e.g. "English", "Chinese", "Japanese").
    """
    if not text:
        return "English"

    # Count characters in each script range
    counts: dict[str, int] = {}

    for ch in text:
        cp = ord(ch)
        if cp < 0x80:  # Skip ASCII
            continue

        script = _get_script(cp)
        if script:
            counts[script] = counts.get(script, 0) + 1

    # Special case: Japanese uses BOTH Hiragana/Katakana and Kanji. Pure
    # Chinese uses ONLY Kanji. If we see any Japanese script characters at
    # all alongside Kanji, the language is Japanese, regardless of which
    # count dominates. (Kanji-heavy Japanese text would otherwise be
    # misclassified as Chinese.)
    if (counts.get("Japanese", 0) > 0) and (counts.get("Chinese", 0) > 0):
        return "Japanese"

    # If non-Latin scripts detected, return the dominant one
    max_script = ""
    max_count = 0
    for script, count in counts.items():
        if script not in ("Latin", "Unknown") and count > max_count:
            max_script = script
            max_count = count

    if max_script and max_count >= 2:
        return max_script

    # For Latin-script languages, use diacritics and common word patterns
    latin_lang = _detect_latin_language(text)
    if latin_lang:
        return latin_lang

    return "English"


def _get_script(cp: int) -> Optional[str]:
    """Map a Unicode codepoint to a script name, or None if unhandled."""
    # CJK Unified Ideographs (Chinese/Japanese Kanji)
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or (cp >= 0x3400 and cp <= 0x4DBF) or
            (cp >= 0x20000 and cp <= 0x2A6DF) or (cp >= 0xF900 and cp <= 0xFAFF)):
        return "Chinese"
    # Japanese Hiragana + Katakana
    if ((cp >= 0x3040 and cp <= 0x309F) or (cp >= 0x30A0 and cp <= 0x30FF) or
            (cp >= 0x31F0 and cp <= 0x31FF) or (cp >= 0xFF65 and cp <= 0xFF9F)):
        return "Japanese"
    # Korean Hangul
    if ((cp >= 0xAC00 and cp <= 0xD7AF) or (cp >= 0x1100 and cp <= 0x11FF) or
            (cp >= 0x3130 and cp <= 0x318F)):
        return "Korean"
    # Arabic
    if ((cp >= 0x0600 and cp <= 0x06FF) or (cp >= 0x0750 and cp <= 0x077F) or
            (cp >= 0x08A0 and cp <= 0x08FF) or (cp >= 0xFB50 and cp <= 0xFDFF) or
            (cp >= 0xFE70 and cp <= 0xFEFF)):
        return "Arabic"
    # Hebrew
    if (cp >= 0x0590 and cp <= 0x05FF) or (cp >= 0xFB1D and cp <= 0xFB4F):
        return "Hebrew"
    # Thai
    if 0x0E00 <= cp <= 0x0E7F:
        return "Thai"
    # Devanagari (Hindi, Sanskrit, Marathi, Nepali)
    if 0x0900 <= cp <= 0x097F:
        return "Hindi"
    # Bengali
    if 0x0980 <= cp <= 0x09FF:
        return "Bengali"
    # Tamil
    if 0x0B80 <= cp <= 0x0BFF:
        return "Tamil"
    # Telugu
    if 0x0C00 <= cp <= 0x0C7F:
        return "Telugu"
    # Kannada
    if 0x0C80 <= cp <= 0x0CFF:
        return "Kannada"
    # Malayalam
    if 0x0D00 <= cp <= 0x0D7F:
        return "Malayalam"
    # Gujarati
    if 0x0A80 <= cp <= 0x0AFF:
        return "Gujarati"
    # Gurmukhi (Punjabi)
    if 0x0A00 <= cp <= 0x0A7F:
        return "Punjabi"
    # Myanmar (Burmese)
    if 0x1000 <= cp <= 0x109F:
        return "Burmese"
    # Khmer (Cambodian)
    if 0x1780 <= cp <= 0x17FF:
        return "Khmer"
    # Lao
    if 0x0E80 <= cp <= 0x0EFF:
        return "Lao"
    # Georgian
    if ((cp >= 0x10A0 and cp <= 0x10FF) or (cp >= 0x2D00 and cp <= 0x2D2F)):
        return "Georgian"
    # Armenian
    if 0x0530 <= cp <= 0x058F:
        return "Armenian"
    # Ethiopic (Amharic)
    if 0x1200 <= cp <= 0x137F:
        return "Ethiopic"
    # Tibetan
    if 0x0F00 <= cp <= 0x0FFF:
        return "Tibetan"
    # Sinhala
    if 0x0D80 <= cp <= 0x0DFF:
        return "Sinhala"
    # Cyrillic (Russian, Ukrainian, Bulgarian, etc.)
    if ((cp >= 0x0400 and cp <= 0x04FF) or (cp >= 0x0500 and cp <= 0x052F)):
        return "Russian"
    # Greek
    if ((cp >= 0x0370 and cp <= 0x03FF) or (cp >= 0x1F00 and cp <= 0x1FFF)):
        return "Greek"

    return None


def _detect_latin_language(text: str) -> Optional[str]:
    """Detect Latin-script languages via diacritics and common word patterns.

    Reference: nashsu/llm_wiki/src/lib/detect-language.ts _detectLatinLanguage()
    """
    lower = text.lower()

    # Vietnamese — VN-EXCLUSIVE tone/hook marks only.
    # Earlier versions included shared Latin diacritics (à á â ã è é ê ì í ò ó ô õ
    # ù ú ă ý) which made any French / Portuguese / Spanish / Italian / Romanian
    # text with common diacritics false-positive as Vietnamese. The chars below
    # are Vietnamese-specific tone/hook/horn composites that don't appear in
    # other major languages detected here.
    if re.search(
        r"[ảạắằẳẵặấầẩẫậđẻẽẹếềểễệỉĩịỏọốồổỗộơớờởỡợủũụưứừửữựỷỹỵ]",
        lower,
    ):
        return "Vietnamese"

    # Turkish — require Turkish-unique chars (ğ, ı dotless, ş). Earlier versions
    # also matched ç/ö/ü, which are shared with French/German/Portuguese/Hungarian
    # and caused false positives on PT text like "coração".
    if re.search(r"[ğış]", lower) and re.search(
        r"\b(bir|ve|için|ile|bu|da|de|değil|ama)\b", lower
    ):
        return "Turkish"

    # Polish — distinctive characters
    if re.search(r"[ąćęłńóśźż]", lower):
        return "Polish"

    # Czech/Slovak — háčky and čárky
    if re.search(r"[ěšžřďťňů]", lower):
        return "Czech"

    # Romanian — distinctive characters
    if re.search(r"[ăâîșț]", lower) and re.search(
        r"\b(și|este|sau|care|pentru)\b", lower
    ):
        return "Romanian"

    # Hungarian — double acute accents
    if re.search(r"[őű]", lower):
        return "Hungarian"

    # German — common patterns
    if re.search(r"[äöüß]", lower) or re.search(
        r"\b(und|der|die|das|ist|nicht|ein|eine)\b", lower
    ):
        if re.search(r"\b(und|der|die|das|ist)\b", lower):
            return "German"

    # French — common patterns
    if re.search(r"[àâçéèêëïîôùûüÿœæ]", lower) or re.search(
        r"\b(le|la|les|de|des|est|et|un|une|du|au)\b", lower
    ):
        if re.search(r"\b(le|la|les|est|une|des)\b", lower):
            return "French"

    # Portuguese — must run BEFORE Spanish: PT has stricter char requirements
    # ([ãõç]) than ES, and their common-word sets overlap heavily (`que`, `de`,
    # `um`, etc.). Running ES first steals legitimate PT text.
    if re.search(r"[ãõç]", lower) and re.search(
        r"\b(o|a|os|as|de|do|da|é|em|um|uma|não|que)\b", lower
    ):
        return "Portuguese"

    # Spanish — common patterns. The stage-2 word set is intentionally narrow
    # (words NOT shared with Portuguese): del/por/las/ñ-bearing/inverted-punct.
    if re.search(r"[áéíóúñ¿¡]", lower) or re.search(
        r"\b(el|la|los|las|de|del|es|en|por|que|un|una)\b", lower
    ):
        if (re.search(r"\b(el|los|las|del|por)\b", lower) or
                re.search(r"[ñ¿¡]", lower)):
            return "Spanish"

    # Italian — common patterns
    if re.search(r"\b(il|lo|la|gli|le|di|della|è|e|un|una|che|non|per)\b", lower):
        if re.search(r"\b(il|della|gli|che|è)\b", lower):
            return "Italian"

    # Dutch — common patterns
    if re.search(r"\b(het|de|een|van|en|in|is|dat|op|te|met)\b", lower):
        if re.search(r"\b(het|een|van|dat)\b", lower):
            return "Dutch"

    # Swedish — common patterns
    if re.search(r"[åäö]", lower) and re.search(
        r"\b(och|att|det|en|ett|är|för|med)\b", lower
    ):
        return "Swedish"

    # Norwegian — common patterns
    if re.search(r"[åæø]", lower) and re.search(
        r"\b(og|er|det|en|et|for|med|på)\b", lower
    ):
        return "Norwegian"

    # Danish — similar to Norwegian
    if re.search(r"[åæø]", lower) and re.search(
        r"\b(og|er|det|en|et|til|med|af)\b", lower
    ):
        return "Danish"

    # Finnish — common patterns
    if re.search(r"[äö]", lower) and re.search(
        r"\b(ja|on|ei|se|että|tai|kun|niin)\b", lower
    ):
        return "Finnish"

    # Indonesian/Malay — common patterns
    if re.search(
        r"\b(dan|yang|di|dari|untuk|dengan|ini|itu|adalah|tidak|ada)\b", lower
    ):
        if re.search(r"\b(yang|dari|untuk|dengan|adalah)\b", lower):
            return "Indonesian"

    # Swahili — common patterns
    if re.search(r"\b(na|ya|wa|ni|kwa|katika|hii|hiyo)\b", lower):
        return "Swahili"

    return None
