import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
import os, glob
from matplotlib import cm
import numpy as np
import matplotlib

from localData import swearList
removeList = ['<u>', '</u>', '!', '?', '.', ',', ':', ';', '(', ')', '[', ']', '{', '}', '\n', '\t', '\r', '"']
replaceList = [['&quot;', '"'], ['&apos;', "'"], ['&amp;', '&'], ['&lt;', '<'], ['&gt;', '>']]

def run_analysis(filePath):
    exclamations = 0
    totalMessages = 0
    totalWordLength = 0
    wordsCounted = 0
    swears = 0
    capitalization = 0
    gTen = 0
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
            if not tbad.startswith('<a'): 
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
        if len(words)>10:
            gTen+=1
        if text.lower() != text:
            capitalization += 1
        for word in words:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1
            totalWordLength += len(word)
            wordsCounted += 1

    sorted_dict = {}
    for key in sorted(word_frequencies, key=word_frequencies.get):
        sorted_dict[key] = word_frequencies[key]
    newFileName = f"savedData/{filename.replace('toBeRead/','')}.txt"
    with open(newFileName, 'w') as file:
        file.write('')
        for key in sorted_dict:
            file.write(f'{key}: {sorted_dict[key]}\n')

    cullThreshold = wordsCounted * 0.001
    filtered_words = {word: freq for word, freq in word_frequencies.items() if freq > cullThreshold}

    print('\n' +filePath)
    print (f'{round(exclamations/totalMessages*100,2)}% of messages had at least one exclamation mark in them')
    print (f'The average word length was {round(totalWordLength/wordsCounted,2)} characters')
    print(f'{round(swears/totalMessages*100,2)}% of messages contained swear words or swear adjacent words')
    print(f'{round(capitalization/totalMessages*100,2)}% of messages contained capitalization')
    print(f'{round(gTen/totalMessages*100,2)}% of messages contained more than 10 words')



    G = nx.Graph()
    for text in texts:
        words = [word.lower() for word in text.split() if word.lower() in filtered_words]
        for i, word1 in enumerate(words):
            for word2 in words[i + 1:]:
                if word1 != word2:
                    if G.has_edge(word1, word2):
                        G[word1][word2]['weight'] += 1
                    else:
                        G.add_edge(word1, word2, weight=1)

    
    # threshold = 2
    # edges_to_remove = [(u, v) for u, v, weight in G.edges(data='weight') if weight < threshold]
    # G.remove_edges_from(edges_to_remove)

    node_sizes = [max(filtered_words[word] * 5, 50) for word in G.nodes]

    pos = nx.spring_layout(G, seed=42, k=0.3)

    frequencies = [filtered_words[word] for word in G.nodes]
    if frequencies:
        normalized_frequencies = np.array(frequencies) / max(frequencies)
        color_map = cm.viridis(normalized_frequencies)
    else:
        color_map = []
    plt.figure(figsize=(15, 8))
    nx.draw_networkx_nodes(
        G, pos,
        node_size=node_sizes,
        node_color=color_map,
        alpha=0.8
    )

    edge_widths = [G[u][v]['weight'] * 0.01 for u, v in G.edges]
    nx.draw_networkx_edges(
        G, pos,
        width=edge_widths,
        edge_color='gray'
    )

    nx.draw_networkx_labels(
        G, pos,
        font_size=5,
        font_color='red'
    )

    plt.title(filename, fontsize=16)
    plt.savefig(f"savedImages/{filename[9:]}.png", dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    plt.clf()



# for f in filePaths:
    # run_analysis(f)

for filename in glob.glob('toBeRead/*.html'):
    run_analysis(filename)
# G = nx.Graph()
# for text in texts:
#     words = [word.lower() for word in text.split() if word.lower() in filtered_words]
#     for i, word1 in enumerate(words):
#         for word2 in words[i + 1:]:
#             if G.has_edge(word1, word2):
#                 G[word1][word2]['weight'] += 1
#             else:
#                 G.add_edge(word1, word2, weight=1)

# node_sizes = [filtered_words[word] * 1 for word in G.nodes]

# plt.figure(figsize=(15, 10))

# pos = nx.spring_layout(G, seed=42, k=0.4)

# nx.draw_networkx_nodes(
#     G, pos,
#     node_size=node_sizes,
#     node_color='skyblue',
#     alpha=0.8,
#     edgecolors='none'  # Removes the border
# )

# nx.draw_networkx_edges(
#     G, pos,
#     alpha=0.6,
#     width=0.1,
#     edge_color='gray'
# )

# nx.draw_networkx_labels(
#     G, pos,
#     font_size=10,
#     font_color='red'
# )

# plt.title("Word Co-occurrence Network (Filtered)", fontsize=16)
# plt.show()

