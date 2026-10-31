"""
ResearchX - Text Chunking Utility Module

Splits extracted academic paper text into overlapping chunks for downstream
vector embedding and semantic retrieval.

Token Approximation Methodology:
In the absence of a specialized heavyweight tokenizer library (e.g., tiktoken or tokenizers),
this module uses the standard academic and industry rule of thumb for English text:
    1 token ≈ 4 characters (or ~0.75 words)
    - Target chunk size: 800 tokens ≈ 3,200 characters
    - Target overlap: 150 tokens ≈ 600 characters

Splitting Strategy:
- Text from all valid pages is merged with character-offset tracking to map any
  chunk back to the exact page number(s) from which it originated.
- Chunks snap to natural semantic boundaries (paragraph breaks, sentence boundaries,
  or line breaks) within a search window to avoid truncating sentences or words.
- Each chunk preserves metadata: paper_id, page_numbers (list of ints), chunk_index,
  char_count, and estimated token_count_approx.
"""

from typing import Any, Dict, List

# Documented token approximation constants
APPROX_CHARS_PER_TOKEN = 4  # Standard heuristic: 1 token ~= 4 characters in English
DEFAULT_CHUNK_SIZE_TOKENS = 800
DEFAULT_CHUNK_OVERLAP_TOKENS = 150

CHUNK_SIZE_CHARS = DEFAULT_CHUNK_SIZE_TOKENS * APPROX_CHARS_PER_TOKEN  # ~3,200 chars
CHUNK_OVERLAP_CHARS = DEFAULT_CHUNK_OVERLAP_TOKENS * APPROX_CHARS_PER_TOKEN  # ~600 chars


def estimate_tokens(text: str) -> int:
    """
    Estimate token count for a text string using the 1 token ~= 4 chars heuristic.

    Args:
        text: Input string.

    Returns:
        Approximate token count (minimum 1 if text is non-empty, else 0).
    """
    if not text or not text.strip():
        return 0
    return max(1, round(len(text) / APPROX_CHARS_PER_TOKEN))


def _find_split_point(text: str, target: int, window_back: int = 300, window_fwd: int = 150) -> int:
    """
    Locate a natural semantic boundary (paragraph, sentence, or line) near the target offset.

    Args:
        text: The complete document text.
        target: Target character split position.
        window_back: Characters to look backward for a boundary.
        window_fwd: Characters to look forward for a boundary.

    Returns:
        Character index of the chosen boundary.
    """
    start = max(0, target - window_back)
    end = min(len(text), target + window_fwd)
    sub = text[start:end]

    # Priority 1: Paragraph break (\n\n)
    idx = sub.rfind("\n\n")
    if idx != -1:
        return start + idx + 2

    # Priority 2: Sentence boundaries (. , .\n, ? , ! )
    best_sent = -1
    for punct in [". ", ".\n", "? ", "! ", "!\n"]:
        pos = sub.rfind(punct)
        if pos > best_sent:
            best_sent = pos + len(punct)
    if best_sent != -1:
        return start + best_sent

    # Priority 3: Single newline (\n)
    idx = sub.rfind("\n")
    if idx != -1:
        return start + idx + 1

    # Priority 4: Word boundary (space)
    idx = sub.rfind(" ")
    if idx != -1:
        return start + idx + 1

    # Fallback: Hard cut at target
    return target


def _find_overlap_start(text: str, target_start: int, window: int = 100) -> int:
    """
    Snap the start of an overlapping chunk forward to the beginning of a word or sentence.

    Args:
        text: The complete document text.
        target_start: Desired starting character position.
        window: Window within which to look for a word boundary.

    Returns:
        Adjusted character start position.
    """
    end = min(len(text), target_start + window)
    sub = text[target_start:end]
    for sep in ["\n\n", "\n", " "]:
        idx = sub.find(sep)
        if idx != -1:
            return target_start + idx + len(sep)
    return target_start


def chunk_paper_pages(
    pages: List[Dict[str, Any]],
    paper_id: str,
    chunk_size_tokens: int = DEFAULT_CHUNK_SIZE_TOKENS,
    chunk_overlap_tokens: int = DEFAULT_CHUNK_OVERLAP_TOKENS,
) -> List[Dict[str, Any]]:
    """
    Split extracted paper pages into overlapping chunks preserving page metadata.

    Args:
        pages: List of page dictionaries, each containing 'page_number' (int) and 'text' (str).
        paper_id: Identifier or filename of the paper.
        chunk_size_tokens: Target chunk size in tokens (default: 800).
        chunk_overlap_tokens: Overlap between consecutive chunks in tokens (default: 150).

    Returns:
        List of chunk dictionaries with:
            - chunk_index: int (0-based)
            - paper_id: str
            - page_numbers: List[int] (all source pages contributing text to this chunk)
            - text: str (the chunk content)
            - token_count_approx: int (estimated tokens)
            - char_count: int (character count)
    """
    if not pages:
        return []

    target_chars = chunk_size_tokens * APPROX_CHARS_PER_TOKEN
    overlap_chars = chunk_overlap_tokens * APPROX_CHARS_PER_TOKEN

    # Build continuous text while tracking page character intervals
    page_spans = []  # Tuples: (page_number, start_char, end_char)
    combined_parts = []
    current_offset = 0

    for p in pages:
        txt = p.get("text", "")
        p_num = p.get("page_number", 1)
        if not txt or not txt.strip():
            continue

        if combined_parts:
            combined_parts.append("\n\n")
            current_offset += 2

        start_pos = current_offset
        combined_parts.append(txt)
        current_offset += len(txt)
        end_pos = current_offset
        page_spans.append((p_num, start_pos, end_pos))

    full_text = "".join(combined_parts)
    if not full_text.strip():
        return []

    total_len = len(full_text)

    # If the entire document is smaller than or equal to a single chunk target, return 1 chunk
    if total_len <= target_chars:
        all_pages = sorted(list({p_num for p_num, _, _ in page_spans}))
        cleaned_text = full_text.strip()
        return [
            {
                "chunk_index": 0,
                "paper_id": paper_id,
                "page_numbers": all_pages,
                "text": cleaned_text,
                "token_count_approx": estimate_tokens(cleaned_text),
                "char_count": len(cleaned_text),
            }
        ]

    chunks = []
    start_idx = 0

    while start_idx < total_len:
        raw_end = min(total_len, start_idx + target_chars)
        if raw_end >= total_len:
            end_idx = total_len
        else:
            end_idx = _find_split_point(full_text, raw_end)
            if end_idx <= start_idx:
                end_idx = raw_end

        chunk_text = full_text[start_idx:end_idx].strip()
        if chunk_text:
            # Identify which page spans intersect with [start_idx, end_idx]
            intersecting_pages = [
                p_num
                for (p_num, p_start, p_end) in page_spans
                if max(start_idx, p_start) < min(end_idx, p_end)
            ]
            if not intersecting_pages and page_spans:
                intersecting_pages = [page_spans[0][0]]

            chunks.append(
                {
                    "chunk_index": len(chunks),
                    "paper_id": paper_id,
                    "page_numbers": sorted(list(set(intersecting_pages))),
                    "text": chunk_text,
                    "token_count_approx": estimate_tokens(chunk_text),
                    "char_count": len(chunk_text),
                }
            )

        if end_idx >= total_len:
            break

        # Calculate next starting position with overlap
        next_raw = max(start_idx + 1, end_idx - overlap_chars)
        next_start = _find_overlap_start(full_text, next_raw)
        if next_start <= start_idx or next_start >= end_idx:
            next_start = start_idx + max(1, target_chars - overlap_chars)
        start_idx = next_start

    return chunks

