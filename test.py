file = open('data.txt', 'r')

secondfile = open("data2.txt", 'a+')

links = set()

for line in file.readlines():
    fslash = line.find("/", line.find("/", line.find("/", line.find("/")+1)+1)+1)
    purelink = line[0:fslash].split("?")[0]
    if len(purelink) <= 55:
        links.add(purelink)

for link in links:
    secondfile.write(link+"\n")

print(len(links))