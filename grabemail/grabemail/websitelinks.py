class linkHelpMan():
    def getFirstLink(self):
        firslink = list()
        websitefile = open('websites.txt', 'r')
        firstline = websitefile.readline().rstrip()
        firslink.append(firstline)
        websitefile.close()
        return firslink

    def readExactLink(self, ln):
        global link
        fp = open("websites.txt")
        for i, line in enumerate(fp):
            if i == ln - 1:
                link = line.rstrip()
        fp.close()
        return link

    def linkNumber(self):
        return sum(1 for line in open('websites.txt'))
