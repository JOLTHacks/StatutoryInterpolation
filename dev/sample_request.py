import requests, urllib2

r = requests.request(method='get', url='http://127.0.0.1:5000/getTitle',\
                 data='{"title": 10}')
print r, r.text
