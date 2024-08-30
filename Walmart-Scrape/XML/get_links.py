import xml.etree.ElementTree as ET

all_products_file = open("product_links.txt", "a+")




for i in range(1010):
	links = set()
	file_name = "sitemap" + str(i+1) + ".xml"

	tree = ET.parse(file_name)
	root = tree.getroot()

	# In find/findall, prefix namespaced tags with the full namespace in braces
	for url in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
		loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
		links.add(loc)

	for l in links:
		all_products_file.write(l+"\n")

	print(str(len(links))+' links added - ' + str(i+1))