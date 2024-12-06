from localData import filePath, theirNumber
lastIndex = 0
texts = []
removeList = ['<u>', '</u>', '!', '?', '.', ',', ':', ';', '(', ')', '[', ']', '{', '}', '\n', '\t', '\r', '"']
replaceList = [['&quot;','"'],['&apos;',"'"],['&amp;','&'],['&lt;','<'],['&gt;','>']]
words = {}
cullThreshold = 1
with open(filePath, 'r+') as myFile:
    content = myFile.read()
    while (content.find('<span class="sender">Me')!=-1):
        firstSender = content.find('<span class="sender">Me')
        nextMessage = content[firstSender:].find('<span class="bubble">')+firstSender+len('<span class="bubble">')
        nextEnd = content[nextMessage:].find("</span>")+nextMessage
        # print(nextMessage)
        # print(nextEnd)
        tbad = content[nextMessage:nextEnd]
        if tbad[0:3]!='<a':
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
texts = list(set(texts))
for i in range(len(texts)):
    for a in removeList:
        texts[i] = texts[i].replace(a, '')
        print("e")
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

# print(texts)
# for a in texts: print(a)