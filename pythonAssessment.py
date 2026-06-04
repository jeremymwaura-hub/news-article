from collections import Counter
from pathlib import Path
import re
import sys


def count_specific_word(text, search_word):
    """Count how many times search_word appears as a whole word (case-insensitive).

    Returns 0 if nothing is found or inputs are empty.
    """
    # simple checks
    if not text or not search_word:
        return 0
    # use word boundary so we don't count substrings
    pattern = r"\b" + re.escape(search_word) + r"\b"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    return len(matches)


def identify_most_common_word(text):
    """Return the most common word in the text, or None if text is empty."""
    if not text or not text.strip():
        return None
    # find words made of letters and apostrophes
    words = re.findall(r"[A-Za-z']+", text.lower())
    if not words:
        return None
    counter = Counter(words)
    most_common_word, _ = counter.most_common(1)[0]
    return most_common_word


def calculate_average_word_length(text):
    """Calculate average length of words ignoring punctuation.

    Return 0.0 for empty text.
    """
    if not text or not text.strip():
        return 0.0
    words = re.findall(r"[A-Za-z']+", text)
    if not words:
        return 0.0
    # remove apostrophes from length count
    total_len = 0
    for w in words:
        total_len += len(w.replace("'", ""))
    return total_len / len(words)


def count_paragraphs(text):
    """Count paragraphs separated by empty lines.

    If text is empty, return 1 (as per assignment requirement).
    """
    if text is None or text == "":
        return 1
    blocks = re.split(r"\n\s*\n+", text.strip())
    blocks = [b for b in blocks if b.strip()]
    return max(1, len(blocks))


def count_sentences(text):
    """Count sentences by splitting on . ! or ? followed by whitespace.

    If text is empty, return 1.
    """
    if text is None or text == "":
        return 1
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [p for p in parts if re.search(r'[A-Za-z0-9]', p)]
    return max(1, len(sentences))


def read_article_from_candidates():
    """Try to read a file from common names, else ask user or use sample."""
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
    print("No article file found in common locations.")
    user_path = input("Enter path to news article file (or press Enter to use sample): ").strip()
    if user_path:
        try:
            return Path(user_path).read_text(encoding="utf-8")
        except Exception as e:
            print("Couldn't read file:", e)
    sample = (
        "Breaking News: Local developer writes text-analysis script.\n\n"
        "This is a short sample article used when no file is provided.\n"
        "It includes multiple sentences. Does it count sentences correctly? Yes!"
    )
    return sample


def main():
    # read article text
    article_text = read_article_from_candidates()

    print("\n--- Article Analysis Summary ---\n")
    most_common = identify_most_common_word(article_text)
    avg_len = calculate_average_word_length(article_text)
    para_count = count_paragraphs(article_text)
    sent_count = count_sentences(article_text)

    print("Most common word:", most_common)
    print("Average word length:", f"{avg_len:.2f}")
    print("Paragraphs:", para_count)
    print("Sentences:", sent_count)

    # show top words (simple for loop)
    words = re.findall(r"[A-Za-z']+", article_text.lower())
    freq = Counter(words)
    print("\nTop words:")
    for i, (w, c) in enumerate(freq.most_common(10), start=1):
        print(i, w, "-", c)

    # simple interactive menu using while and if/else
    while True:
        print("\nOptions: [1] Count specific word  [2] Re-analyze  [3] Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            word = input("Enter word to count: ").strip()
            count = count_specific_word(article_text, word)
            if count:
                print("The word '", word, "' appears", count, "times.")
            else:
                print("The word '", word, "' was not found.")
        elif choice == "2":
            most_common = identify_most_common_word(article_text)
            print("Most common word:", most_common)
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
