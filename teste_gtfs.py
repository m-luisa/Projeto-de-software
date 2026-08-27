import requests
url = "http://realtime4.mobilibus.com/web/4ch6j/trip-updates?accesskey=982a57efd77a9462bf1665696fb25984"
r = requests.get(url, timeout=10)
print(r.status_code)      # espera 200
print(len(r.content))     # espera um número maior que zero