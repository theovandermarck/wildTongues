import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
import os, glob

# Parameters and settings
from localData import filePaths, swearList
removeList = ['<u>', '</u>', '!', '?', '.', ',', ':', ';', '(', ')', '[', ']', '{', '}', '\n', '\t', '\r', '"']
replaceList = [['&quot;', '"'], ['&apos;', "'"], ['&amp;', '&'], ['&lt;', '<'], ['&gt;', '>']]
cullThreshold = 25  # Words appearing less than this will be removed

# Read and process the text file
def run_analysis(filePath):
    exclamations = 0
    totalMessages = 0
    totalWordLength = 0
    wordsCounted = 0
    swears = 0
    capitalization = 0
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
            for swear in swearList:
                if swear in tbad:
                    swears += 1
                    break
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
        if text.lower() != text:
            capitalization += 1
        for word in words:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1
            totalWordLength += len(word)
            wordsCounted += 1

    # Remove words below the frequency threshold
    filtered_words = {word: freq for word, freq in word_frequencies.items() if freq > cullThreshold}
    print('\n' +filePath)
    print (f'{round(exclamations/totalMessages*100,2)}% of messages had at least one exclamation mark in them')
    print (f'The average word length was {round(totalWordLength/wordsCounted,2)} characters')
    print(f'{round(swears/totalMessages*100,2)}% of messages contained swear words or swear adjacent words')
    print(f'{round(capitalization/totalMessages*100,2)}% of messages contained capitalization')

# for f in filePaths:
    # run_analysis(f)

for filename in glob.glob('toBeRead/*.html'):
    run_analysis(filename)
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

