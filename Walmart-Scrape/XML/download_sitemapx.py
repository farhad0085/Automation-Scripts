import requests
from links_handler import LinkHelper

l = LinkHelper()
total_products = l.linkNumber()

i = 1

while i <= total_products:

	url = l.readExactLink(i)
	r = requests.get(url, allow_redirects=True)

	open(f'sitemap{i}.xml', 'wb').write(r.content)
	print(f"{i} sitemaps downloaded!")
	i += 1