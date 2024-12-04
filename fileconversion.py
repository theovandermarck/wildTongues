filePath = '+14156375366.txt'
theirNumber = "+14156375366"
with open(filePath, 'r+') as myFile:
    content = myFile.read()
    print(content[content.find(theirNumber):content.find('\n\n')])