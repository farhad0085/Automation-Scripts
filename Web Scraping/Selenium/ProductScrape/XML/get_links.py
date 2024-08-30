import xml.etree.ElementTree as ET

all_products_file = open("products_links.txt", "a+")

i = 1

links = set()

while i<9:

	file_name = "productsitemap"+str(i)+".xml"

	tree = ET.parse(file_name)
	root = tree.getroot()

	# In find/findall, prefix namespaced tags with the full namespace in braces
	for url in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
		loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
		links.add(loc)

	i += 1

for l in links:
	all_products_file.write(l+"\n")

print(len(links))