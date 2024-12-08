import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations

# Parameters and settings
from localData import filePaths
removeList = ['<u>', '</u>', '!', '?', '.', ',', ':', ';', '(', ')', '[', ']', '{', '}', '\n', '\t', '\r', '"']
replaceList = [['&quot;', '"'], ['&apos;', "'"], ['&amp;', '&'], ['&lt;', '<'], ['&gt;', '>']]
cullThreshold = 25  # Words appearing less than this will be removed

# Read and process the text file
def run_analysis(filePath):
    exclamations = 0
    totalMessages = 0
    totalWordLength = 0
    wordsCounted = 0
    texts = []
    with open(filePath, 'r', encoding='utf-8') as myFile:
        content = myFile.read()
        while '<span class="sender">Me' in content:
            firstSender = content.find('<span class="sender">Me')
            nextMessage = content[firstSender:].find('<span class="bubble">') + firstSender + len('<span class="bubble">')
            nextEnd = content[nextMessage:].find("</span>") + nextMessage
            tbad = content[nextMessage:nextEnd]
            if '!' in tbad:
                exclamations += 1
            if not tbad.startswith('<a'):  # Exclude links
                for a in replaceList:
                    tbad = tbad.replace(a[0], a[1])
                for a in removeList:
                    tbad = tbad.replace(a, '')
                texts.append(tbad)
            lastIndex = content.find('</span>\n</div>') + 14
            content = content[lastIndex:]
            totalMessages += 1
    texts = list(set(texts))
    word_frequencies = {}
    for text in texts:
        words = text.lower().split()
        for word in words:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1
            totalWordLength += len(word)
            wordsCounted += 1

    # Remove words below the frequency threshold
    filtered_words = {word: freq for word, freq in word_frequencies.items() if freq > cullThreshold}
    print('\n' +filePath)
    print (f'{exclamations/totalMessages*100}% of messages had at least one exclamation mark in them')
    print (f'The average word length was {totalWordLength/wordsCounted} characters')

for f in filePaths:
    run_analysis(f)
# Build the word co-occurrence network
# G = nx.Graph()
# for text in texts:
#     words = [word.lower() for word in text.split() if word.lower() in filtered_words]
#     for i, word1 in enumerate(words):
#         for word2 in words[i + 1:]:
#             if G.has_edge(word1, word2):
#                 G[word1][word2]['weight'] += 1
#             else:
#                 G.add_edge(word1, word2, weight=1)

# # Set node sizes based on frequencies
# node_sizes = [filtered_words[word] * 1 for word in G.nodes]

# # Draw the graph
# plt.figure(figsize=(15, 10))

# # Adjust layout for better spacing
# pos = nx.spring_layout(G, seed=42, k=0.4)

# # Draw nodes without white circles
# nx.draw_networkx_nodes(
#     G, pos,
#     node_size=node_sizes,
#     node_color='skyblue',
#     alpha=0.8,
#     edgecolors='none'  # Removes the border
# )

# # Draw edges
# nx.draw_networkx_edges(
#     G, pos,
#     alpha=0.6,
#     width=0.1,
#     edge_color='gray'
# )

# # Draw labels in red
# nx.draw_networkx_labels(
#     G, pos,
#     font_size=10,
#     font_color='red'
# )

# plt.title("Word Co-occurrence Network (Filtered)", fontsize=16)
# plt.show()

