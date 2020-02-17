import requests
s = requests.Session()
r = s.post('http://127.0.0.1:8080/',data={ "model":"iPhone 6",
                                           "brand":"Apple",
                                           "os":"iOS",
                                           "osVersion":"11.4"})

print (r.text)