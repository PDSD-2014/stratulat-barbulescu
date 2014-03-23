import web

import sys, logging
import SimpleHTTPServer
import cgi

import urllib, json
import pprint

import configuration
from ReverseGeocode import get_geonames

import os

sys.path.append("./db")
import Database

urls = (
    '/',        'index',
    '/Victim',  'Victim',
    '/Criminal','Criminal',
    '/Test',     'Test',
    '/favicon.ico',     'icon'
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
        
class LocateGuy(object):
    
    def __init__(self):
        self.lat = 0
        self.lng = 0
    
    def plot_last_locations(self, who_table, count = 5):
        locations = []
        d = Database.Database()
        rows = d.execute_sql("select lat, lng from %s order by PostedTime desc limit %s;" % (str(who_table), str(count)))
        
        for row in rows:
            lat = row[0]
            lng = row[1]
            locations.append((lat, lng))

        return render.map_plot("text", locations)

class Victim(LocateGuy):
    def GET(self):
        return super(Victim, self).plot_last_locations("VictimLocation", 5)
        

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

class Criminal(LocateGuy):
    def GET(self):
        return super(Criminal, self).plot_last_locations("CriminalLocation", 5)

class Test:
    def GET(self):
        return render.map_plot("text", dummy_list=[ (45.3571195, 25.5397671), # Pensiunea Andre, Sinaia, Furnica
                                            (44.417126, 26.110211),  # Acasa
                                            (46.6023,  22.98421),    # Coordonatele accidentului din Apuseni
                                            (44.402913, 26.136045),  # Delta Vacaresti
                                            (45.185360, 29.655238),  # Sulina
                                            (44.057735, 28.596516),  # Techirghiol
                                            (45.331103, 22.822643)   # Parcul National Retezat
                                        ])
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
