import requests
import BeautifulSoup4



product_code = 2802056
url = f'https://www.ceneo.pl/{product_code}#tab=reviews'
response = requests.get(url)