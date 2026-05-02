"""
Sanitize LLM-generated wiki page content before writing to disk.

Handles 4 patterns:
1. Whole page wrapped in ```yaml fence
2. Frontmatter in fence, body outside fence (variant we discovered)
3. Leading `frontmatter:` prefix
4. Wikilink lists in frontmatter
"""

import re


def sanitize_page_content(content: str) -> str:
    """Clean up an LLM-generated wiki page body before it hits disk."""
    cleaned = content
    
    # Try outer fence pattern first
    cleaned = strip_outer_code_fence(cleaned)
    
    # If that didn't work, try the variant: fence after frontmatter, before body
    if content.startswith('```'):
        cleaned = strip_fence_after_frontmatter(cleaned)
    
    cleaned = strip_frontmatter_key_prefix(cleaned)
    cleaned = repair_wikilink_lists_in_frontmatter(cleaned)
    
    return cleaned


def strip_outer_code_fence(content: str) -> str:
    """Remove outer ```yaml fence that wraps the entire document."""
    pattern = r'^[ \t]*```(?:yaml|md|markdown)?[ \t]*\r?\n'
    match = re.match(pattern, content, re.MULTILINE)
    if not match:
        return content
    after_open = content[match.end():]
    
    # Closing fence at end of file
    close_pattern = r'\r?\n[ \t]*```[ \t]*\r?\n?\s*$'
    close_match = re.search(close_pattern, after_open)
    if not close_match:
        return content
    return after_open[:close_match.start()]


def strip_fence_after_frontmatter(content: str) -> str:
    """
    Handle variant: opening fence at start, frontmatter, closing fence, body.
    
    Pattern:
        ```yaml
        ---
        frontmatter
        ---
        ```
        # Body
    """
    # Check if starts with opening fence
    open_pattern = r'^[ \t]*```(?:yaml|md|markdown)?[ \t]*\r?\n'
    open_match = re.match(open_pattern, content)
    if not open_match:
        return content
    after_open = content[open_match.end():]
    
    # Find frontmatter block
    fm_pattern = r'^---\s*\r?\n([\s\S]*?)\r?\n---\s*\r?\n'
    fm_match = re.match(fm_pattern, after_open)
    if not fm_match:
        return content
    
    frontmatter = fm_match.group(0)
    after_fm = after_open[fm_match.end():]
    
    # Check for closing fence right after frontmatter
    close_pattern = r'^[ \t]*```[ \t]*\r?\n'
    close_match = re.match(close_pattern, after_fm)
    if not close_match:
        return content
    
    body = after_fm[close_match.end():]
    return frontmatter + body


def strip_frontmatter_key_prefix(content: str) -> str:
    """Strip stray `frontmatter:` line that prefixes the real frontmatter block."""
    pattern = r'^[ \t]*frontmatter\s*:\s*\r?\n(?=[ \t]*---\s*\r?\n)'
    match = re.match(pattern, content, re.MULTILINE)
    if not match:
        return content
    return content[match.end():]


def repair_wikilink_lists_in_frontmatter(content: str) -> str:
    """Repair `key: [[a]], [[b]], [[c]]` lines to valid YAML arrays."""
    fm_pattern = r'^---\s*\r?\n([\s\S]*?)\r?\n---\s*(\r?\n|$)'
    match = re.match(fm_pattern, content, re.MULTILINE)
    if not match:
        return content
    
    frontmatter_body = match.group(1)
    after_fm = match.group(2)
    
    lines = frontmatter_body.split('\n')
    repaired_lines = []
    
    for line in lines:
        wikilink_pattern = r'^(\s*[A-Za-z_][\w-]*\s*:\s*)(\[\[[^\]]+\]\](?:\s*,\s*\[\[[^\]]+\]\])+)\s*$'
        lm = re.match(wikilink_pattern, line)
        if not lm:
            repaired_lines.append(line)
            continue
        
        key_part = lm.group(1)
        wikilinks = lm.group(2)
        
        items = []
        for s in wikilinks.split(','):
            s = s.strip()
            if not s:
                continue
            wm = re.match(r'\[\[([^\]]+)\]\]', s)
            if wm:
                items.append(f'"{wm.group(1)}"')
        
        repaired_line = f'{key_part}[{", ".join(items)}]'
        repaired_lines.append(repaired_line)
    
    repaired_body = '\n'.join(repaired_lines)
    fm_start = content[:match.start()]
    body = content[match.end():]  # preserve body content after frontmatter
    return f'{fm_start}---\n{repaired_body}\n---{after_fm}{body}'
