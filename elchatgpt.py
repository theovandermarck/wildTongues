import os
from collections import Counter

def load_word_counts(file_path):
    """Load word counts from a file and return as a dictionary."""
    word_counts = {}
    with open(file_path, 'r') as file:
        for line in file:
            word, count = line.strip().split(': ')
            word_counts[word] = int(count)
    return word_counts

def get_top_words(word_counts, top_n=200):
    """Retrieve the top N most frequent words from a word count dictionary."""
    return set([word for word, _ in Counter(word_counts).most_common(top_n)])

def compare_top_words(file_paths, top_n=200):
    """Compare the top N words across multiple files and find unique words."""
    all_top_words = []
    all_word_counts = [load_word_counts(file) for file in file_paths]

    for word_counts in all_word_counts:
        all_top_words.append(get_top_words(word_counts, top_n))

    unique_words = []
    for i, top_words in enumerate(all_top_words):
        other_words = set.union(*(all_top_words[:i] + all_top_words[i+1:]))
        unique_words.append(top_words - other_words)

    return unique_words

def display_unique_words(file_paths, unique_words):
    """Display unique words for each file."""
    for file, words in zip(file_paths, unique_words):
        print(f"Unique words in {file}:")
        print(', '.join(sorted(words)))
        print(len(words))
        print()


# Example usage:
if __name__ == "__main__":
    # Replace with the paths to your files
    file_paths = ["savedData/Minceraft.html.txt", "savedData/Mormon sleeper cell.html.txt", "savedData/mother.html.txt", "savedData/saskia.html.txt", "savedData/theo.html.txt"]

    unique_words = compare_top_words(file_paths, top_n=200)
    display_unique_words(file_paths, unique_words)


