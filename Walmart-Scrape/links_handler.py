class LinkHelper():

    def readExactLink(self, ln):
        global link
        fp = open("product_links.txt")
        for i, line in enumerate(fp):
            if i == ln - 1:
                link = line.rstrip()
        fp.close()
        return link

    def linkNumber(self):
        return sum(1 for line in open('product_links.txt'))
