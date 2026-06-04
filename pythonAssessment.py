from collections import Counter
import re


def most_common_word(text):
    words = re.findall(r"[A-Za-z']+", text.lower())

    if not words:
        return "No words found"

    counter = Counter(words)
    return counter.most_common(1)[0]


def average_word_length(text):
    words = re.findall(r"[A-Za-z']+", text)

    if not words:
        return 0

    total = 0

    for word in words:
        total += len(word)

    return total / len(words)


def count_paragraphs(text):
    paragraphs = text.strip().split("\n\n")
    return len(paragraphs)


def count_sentences(text):
    sentences = re.findall(r"[.!?]", text)
    return len(sentences)


def count_word(text, search_word):
    words = re.findall(r"[A-Za-z']+", text.lower())
    return words.count(search_word.lower())


# Read article file
with open("article.txt", "r", encoding="utf-8") as file:
    article = file.read()

# Analysis
print("\n--- ARTICLE ANALYSIS ---")

print("Most common word:", most_common_word(article))
print("Average word length:", round(average_word_length(article), 2))
print("Paragraphs:", count_paragraphs(article))
print("Sentences:", count_sentences(article))

# Top 10 words
words = re.findall(r"[A-Za-z']+", article.lower())
counter = Counter(words)

print("\nTop 10 Words:")
for word, count in counter.most_common(10):
    print(word, "-", count)

# Menu
while True:
    print("\n1. Count a specific word")
    print("2. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        word = input("Enter a word: ")
        print("Occurrences:", count_word(article, word))

    elif choice == "2":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")