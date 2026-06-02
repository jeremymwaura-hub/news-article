#!/usr/bin/env python3
# """pythonAssessment.py

# Text analysis utilities for news article content.

# Implements:
# - count_specific_word(text, word)
# - identify_most_common_word(text)
# - calculate_average_word_length(text)
# - count_paragraphs(text)
# - count_sentences(text)

# Also provides an interactive menu demonstrating usage.
# """

from collections import Counter
from pathlib import Path
import re
import sys


def count_specific_word(text: str, search_word: str) -> int:
    """Count whole-word, case-insensitive occurrences of search_word in text.

    Returns 0 if no matches or if either argument is empty.
    """
    if not text or not search_word:
        return 0
    pattern = r"\b" + re.escape(search_word) + r"\b"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    return len(matches)


def identify_most_common_word(text: str) -> str | None:
    """Return the most common word (lowercased) or None for empty input.

    Words are sequences of letters and apostrophes. Punctuation is ignored.
    """
    if not text or not text.strip():
        return None
    words = re.findall(r"[A-Za-z']+", text.lower())
    if not words:
        return None
    counter = Counter(words)
    most_common_word, _ = counter.most_common(1)[0]
    return most_common_word


def calculate_average_word_length(text: str) -> float:
    """Calculate average word length, excluding punctuation.

    Returns 0.0 for empty input.
    """
    if not text or not text.strip():
        return 0.0
    words = re.findall(r"[A-Za-z']+", text)
    if not words:
        return 0.0
    total_len = sum(len(w.replace("'", '')) for w in words)
    return total_len / len(words)


def count_paragraphs(text: str) -> int:
    """Count paragraphs defined by one or more empty lines between blocks.

    Edge case: empty string should return 1.
    """
    if text is None or text == "":
        return 1
    # Split on two or more newlines (with optional whitespace)
    blocks = re.split(r"\n\s*\n+", text.strip())
    # Filter out any empty blocks
    blocks = [b for b in blocks if b.strip()]
    return max(1, len(blocks))


def count_sentences(text: str) -> int:
    """Count sentences based on terminal punctuation (., !, ?).

    Edge case: empty string should return 1.
    """
    if text is None or text == "":
        return 1
    # Split on sentence enders followed by whitespace (keep abbreviations simple)
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    # Filter out very short fragments
    sentences = [p for p in parts if re.search(r'[A-Za-z0-9]', p)]
    return max(1, len(sentences))


def read_article_from_candidates() -> str:
    """Try common file locations for a provided article, else ask user.

    Returns the article text as a string. If no file found, returns an empty string.
    """
    candidates = [
        Path("news_article.txt"),
        Path("article.txt"),
        Path("news-article/article.txt"),
        Path(__file__).with_name("article.txt"),
    ]
    for p in candidates:
        try:
            if p.exists():
                return p.read_text(encoding="utf-8")
        except Exception:
            continue
    # No candidate found — try asking user for path (non-interactive tests can skip)
    print("No article file found in common locations.")
    user_path = input("Enter path to news article file (or press Enter to use sample): ").strip()
    if user_path:
        try:
            return Path(user_path).read_text(encoding="utf-8")
        except Exception as e:
            print(f"Couldn't read file: {e}")
    # Return sample placeholder text
    sample = (
        "Breaking News: Local developer writes text-analysis script.\n\n"
        "This is a short sample article used when no file is provided.\n"
        "It includes multiple sentences. Does it count sentences correctly? Yes!"
    )
    return sample


def main():
    article_text = read_article_from_candidates()

    # Demonstrate the functions with example outputs
    print("\n--- Article Analysis Summary ---\n")
    most_common = identify_most_common_word(article_text)
    avg_len = calculate_average_word_length(article_text)
    para_count = count_paragraphs(article_text)
    sent_count = count_sentences(article_text)

    print(f"Most common word: {most_common}")
    print(f"Average word length: {avg_len:.2f}")
    print(f"Paragraphs: {para_count}")
    print(f"Sentences: {sent_count}")

    # Show top 10 words using a for loop
    words = re.findall(r"[A-Za-z']+", article_text.lower())
    freq = Counter(words)
    print("\nTop words:")
    for i, (w, c) in enumerate(freq.most_common(10), start=1):
        print(f"{i}. {w} — {c}")

    # Interactive menu demonstrating while loop and conditional logic
    while True:
        print("\nOptions: [1] Count specific word  [2] Re-analyze  [3] Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            word = input("Enter word to count: ").strip()
            count = count_specific_word(article_text, word)
            if count:
                print(f"The word '{word}' appears {count} times.")
            else:
                print(f"The word '{word}' was not found.")
        elif choice == "2":
            # Recompute and show a short summary
            most_common = identify_most_common_word(article_text)
            print(f"Most common word: {most_common}")
        elif choice == "3" or choice.lower() in ("q", "quit", "exit"):
            print("Exiting analysis.")
            break
        else:
            print("Invalid option — please choose 1, 2, or 3.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")
        sys.exit(0)
