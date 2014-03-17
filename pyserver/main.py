import web
import sys, logging
import SimpleHTTPServer
import cgi

import urllib, json
import pprint

import configuration
from reverse_geocode_demo import get_geonames

urls = (
    '/',        'index',
    '/Victim',  'Victim',
    '/Criminal','Criminal'
)

render = web.template.render('templates/', base='layout')
render_plain = web.template.render('templates/')

class index:
    def GET(self):
        f = open("lipsum.txt", "r")
        return render.index(str(f.read()))

    def POST(self):
        i = web.input(name=None)
        return render.index(i.name)

class Victim:
    def GET(self):
        return render_plain.victim("x", "y", "z", "t")

    def POST(self):
        i = web.input(lat=45, lng=42)
        #Process some reverse geocoding        
        google_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=true" % (str(i.lat), str(i.lng))
        googleResponse = urllib.urlopen(google_url)
        jsonResp = json.loads(googleResponse.read())
        fmt_addr = str(jsonResp['results'][0]['formatted_address']) + '\n'
        retstr = '';
        types = configuration.filter_types
        for geoname in get_geonames(i.lat, i.lng, types):
            common_types = set(geoname['types']).intersection(set(types))
            retstr =  retstr + '{} {}'.format(geoname['long_name'], ', ') + '  '
 
        return render.victim(fmt_addr, retstr, str(i.lat), str(i.lng))

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
