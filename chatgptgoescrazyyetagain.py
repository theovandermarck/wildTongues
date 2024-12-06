import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations

# Parameters and settings
from localData import filePath, theirNumber
removeList = ['<u>', '</u>', '!', '?', '.', ',', ':', ';', '(', ')', '[', ']', '{', '}', '\n', '\t', '\r', '"']
replaceList = [['&quot;', '"'], ['&apos;', "'"], ['&amp;', '&'], ['&lt;', '<'], ['&gt;', '>']]
cullThreshold = 25  # Words appearing less than this will be removed

# Read and process the text file
def parse_text(file_path):
    texts = []
    with open(file_path, 'r', encoding='utf-8') as myFile:
        content = myFile.read()
        while '<span class="sender">Me' in content:
            firstSender = content.find('<span class="sender">Me')
            nextMessage = content[firstSender:].find('<span class="bubble">') + firstSender + len('<span class="bubble">')
            nextEnd = content[nextMessage:].find("</span>") + nextMessage
            tbad = content[nextMessage:nextEnd]
            if not tbad.startswith('<a'):  # Exclude links
                for a in replaceList:
                    tbad = tbad.replace(a[0], a[1])
                for a in removeList:
                    tbad = tbad.replace(a, '')
                texts.append(tbad)
            lastIndex = content.find('</span>\n</div>') + 14
            content = content[lastIndex:]
    return list(set(texts))

# Build the word co-occurrence network
def build_cooccurrence_graph(texts, cull_threshold):
    word_freq = defaultdict(int)
    cooccurrences = defaultdict(int)
    
    # Count word frequencies
    for text in texts:
        words = text.lower().split()
        for word in words:
            word_freq[word] += 1
        # Track co-occurrences
        for pair in combinations(set(words), 2):
            cooccurrences[frozenset(pair)] += 1

    # Filter words below the threshold
    filtered_words = {word for word, count in word_freq.items() if count > cull_threshold}
    filtered_cooccurrences = {
        pair: count for pair, count in cooccurrences.items()
        if all(word in filtered_words for word in pair)
    }

    # Create graph
    G = nx.Graph()
    for pair, weight in filtered_cooccurrences.items():
        word1, word2 = tuple(pair)
        G.add_edge(word1, word2, weight=weight)
    return G

# Visualize the graph
def visualize_graph(G):
    pos = nx.spring_layout(G)  # Layout for visualization
    weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw(
        G, pos, with_labels=True, node_size=500, node_color="skyblue",
        edge_color=weights, width=1, edge_cmap=plt.cm.Blues
    )
    plt.show()

# Main program
if __name__ == "__main__":
    texts = parse_text(filePath)
    G = build_cooccurrence_graph(texts, cullThreshold)
    visualize_graph(G)
