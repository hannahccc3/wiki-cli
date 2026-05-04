"""
Language directive for LLM prompts.

Reference: nashsu/llm_wiki/src/lib/output-language.ts
"""

from .detect_language import detect_language


def get_output_language(fallback_text: str = "") -> str:
    """Get the effective output language for LLM content generation.

    Currently returns "English" as default since wiki-cli doesn't yet have
    a per-wiki outputLanguage setting in config. This will be enhanced
    when the config system supports it.

    Reference: nashsu/llm_wiki getOutputLanguage()
    """
    # TODO: wire in per-wiki outputLanguage config when available
    return detect_language(fallback_text) if fallback_text else "English"


def build_language_directive(fallback_text: str = "") -> str:
    """Build a strong language directive to inject into system prompts.

    Reference: nashsu/llm_wiki buildLanguageDirective()
    """
    lang = get_output_language(fallback_text)
    return "\n".join([
        f"## ⚠️ MANDATORY OUTPUT LANGUAGE: {lang}",
        "",
        f"You MUST write your entire response (including wiki page titles, content,",
        f"descriptions, summaries, and any generated text) in **{lang}**.",
        f"The source material or wiki content may be in a different language, but",
        f"this is IRRELEVANT to your output language.",
        f"Ignore the language of any source content. Generate everything in {lang} only.",
        f"Proper nouns should use standard {lang} transliteration when appropriate.",
        f"DO NOT use any other language. This overrides all other instructions.",
    ])


def build_language_reminder(fallback_text: str = "") -> str:
    """Short reminder version for placing before user's current message.

    Reference: nashsu/llm_wiki buildLanguageReminder()
    """
    lang = get_output_language(fallback_text)
    return f"REMINDER: All output must be in {lang}. Do not use any other language."
