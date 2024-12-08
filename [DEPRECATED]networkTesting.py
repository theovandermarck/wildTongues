from localData import filePath, theirNumber
lastIndex = 0
texts = []
removeList = ['<u>', '</u>', '!', '?', '.', ',', ':', ';', '(', ')', '[', ']', '{', '}', '\n', '\t', '\r', '"']
replaceList = [['&quot;','"'],['&apos;',"'"],['&amp;','&'],['&lt;','<'],['&gt;','>']]
words = {}
cullThreshold = 25
with open(filePath, 'r+') as myFile:
    content = myFile.read()
    # print(content)
    while True:
        while True:
            if content.find('</span>\n</div>')<content.find('<span class="sender">Me'):
                print('r' + str(len(content)))
                content = content[:lastIndex]+content[content.find('</span>\n</div>')+14:]
            else:
                break
    
        # print(str(content.find('<span class="bubble">')) +" "+ str(content.find("</span>")))
        tbad = (content[content.find('<span class="sender">Me')+87:content.find('</span>\n</div>')])
        print(tbad)
        for a in replaceList:
            tbad = tbad.replace(a[0], a[1])
        for a in removeList:
            tbad = tbad.replace(a, '')
        texts.append(tbad)
        lastIndex = content.find('</span>\n</div>')+14
        content = content[lastIndex:]
        lastIndex = 0
        if content.find('<span class="sender">Me')==-1:
            break
# for i in range(len(texts)):
#     for a in removeList:
#         texts[i] = texts[i].replace(a, '')
#         print("e")
for text in texts:
    for word in text.split():
        if word.lower() in words:
            words[word.lower()] += 1
        else:
            words[word.lower()] = 1
tbdd = []
for a in words.keys():
    if words[a] < cullThreshold+1:
        tbdd.append(a)
for a in tbdd:
    del words[a]
sorted_dict = {key: value for key, 
               value in sorted(words.items(), 
                               key=lambda item: item[1])}
print(sorted_dict)

import networkx as nx
import matplotlib.pyplot as plt


# Define the cleanup lists
removeList = ['<u>', '</u>', '!', '?', '.', ',', ':', ';', '(', ')', '[', ']', '{', '}', '\n', '\t', '\r', '"']
replaceList = [['&quot;', '"'], ['&apos;', "'"], ['&amp;', '&'], ['&lt;', '<'], ['&gt;', '>']]

# Read the file and extract messages
texts = []
with open(filePath, 'r+') as myFile:
    content = myFile.read()
    while '<span class="bubble">' in content:
        start = content.find('<span class="bubble">') + 21
        end = content.find('</span>', start)
        if end == -1:
            break
        
        # Extract and clean the text
        text = content[start:end]
        for old, new in replaceList:
            text = text.replace(old, new)
        for char in removeList:
            text = text.replace(char, '')
        
        texts.append(text.strip())
        content = content[end + 7:]

# Calculate word frequencies and filter
word_frequencies = {}
for text in texts:
    words = text.lower().split()
    for word in words:
        word_frequencies[word] = word_frequencies.get(word, 0) + 1

# Remove words below the frequency threshold
filtered_words = {word: freq for word, freq in word_frequencies.items() if freq > cullThreshold}
tbddd=[]
for a in filtered_words.keys():
    if len(a) > 10:
        tbddd.append(a)
for a in tbddd:
    del filtered_words[a]

# Build the network graph
G = nx.Graph()
for text in texts:
    words = [word.lower() for word in text.split() if word.lower() in filtered_words]
    for i, word1 in enumerate(words):
        for word2 in words[i + 1:]:
            if G.has_edge(word1, word2):
                G[word1][word2]['weight'] += 1
            else:
                G.add_edge(word1, word2, weight=1)

# Set node sizes based on frequencies
node_sizes = [filtered_words[word] * 1 for word in G.nodes]

# Draw the graph
plt.figure(figsize=(15, 10))

# Adjust layout for better spacing
pos = nx.spring_layout(G, seed=42, k=0.4)

# Draw nodes without white circles
nx.draw_networkx_nodes(
    G, pos,
    node_size=node_sizes,
    node_color='skyblue',
    alpha=0.8,
    edgecolors='none'  # Removes the border
)

# Draw edges
nx.draw_networkx_edges(
    G, pos,
    alpha=0.6,
    width=0.1,
    edge_color='gray'
)

# Draw labels in red
nx.draw_networkx_labels(
    G, pos,
    font_size=10,
    font_color='red'
)

plt.title("Word Co-occurrence Network (Filtered)", fontsize=16)
plt.show()

