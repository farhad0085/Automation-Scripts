import requests

url = 'https://www.bigbasket.com/sitemap/productsitemap8.xml'
r = requests.get(url, allow_redirects=True)

open('productsitemap8.xml', 'wb').write(r.content)