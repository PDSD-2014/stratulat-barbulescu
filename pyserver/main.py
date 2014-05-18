import web

import sys, logging
import SimpleHTTPServer
import cgi

import datetime
import pytz

import urllib, json
import pprint

import configuration
from ReverseGeocode import get_geonames

import os
import time
import markdown

sys.path.append("./db")
import Database

sys.path.append(".")
import Weather

import PDSDlogging
log = PDSDlogging.PDSDlogging('MAIN_Logger', 'logs/PDSD_Main.log', logging.DEBUG)
#sys.stdout = log.logger
#sys.stderr = log.logger
log = log.logger

urls = (
    '/',        'index',
    '/Victim',  'Victim',
    '/Criminal','Criminal',
    '/Test',     'Test',
    '/GetAndroidData',     'GetAndroidData',
    '/Distances',       'Distances'
)

render = web.template.render('templates/', base='layout')
render_plain = web.template.render('templates/')

criminal_count = 0

import utils
 
class index:
    def GET(self):
        web.header('Content-Type','text/html; charset=utf-8') 

        try:
            f = open(configuration.README_FILE_PATH, "r")
        except IOError:
            log.info("Could not find file %s" % str(configuration.README_FILE_PATH))
            return web.notfound()
            
        content = f.read()
        f.close()
        
        try:
            f = open("templates/readme.html", "w")
        except:
            log.info("Could not open templates/readme.html for writing")
            return render.index("templates/readme.html", 
                                "Could not open templates/readme.html for writing")
        
        md = markdown.Markdown(output_format='html4')
        content = md.convert(content)
        f.write("$def with (nothing)\n\n$var title: Project Documentation \n $var footer: Showing %s\n\n" % str(configuration.README_FILE_PATH))
        f.write(str(content))  
        f.close()
        time.sleep(0.1)
        return render.readme("x")

    def POST(self):
        i = web.input(name=None)
        return render.index(i.name, "Nothing to show up now")
        
class LocateGuy(object):
    
    def __init__(self):
        self.lat = 0
        self.lng = 0
    
    #whom is only VictimLocation or CriminalLocation    
    def add_to_db(self, lat, lng, whom):
        try:
            db = Database.Database()
        except:
            return render.index("Connection to Database failed! Consider starting MySQL server!")
        
        crt_date = datetime.datetime.now(pytz.timezone("Europe/Bucharest"))
        fmt = '%Y-%m-%d %H:%M:%S'
        d_string = crt_date.strftime(fmt)
        
        types = ['route',
                'sublocality', 
                'administrative_area_level_1', 
                'administrative_area_level_2', 
                'country']
        to_db = dict()
        filter_types = ['route',
                'sublocality', 
                'administrative_area_level_1', 
                'administrative_area_level_2', 
                'country']
        for geoname in get_geonames(lat, lng, types):
            common_types = set(geoname['types']).intersection(set(filter_types))
            tmp_key = str(list(common_types)[0])
            to_db[tmp_key] = u'{}'.format(geoname['long_name'])
        if 'administrative_area_level_1' in to_db.keys():
            to_db['sublocality'] = to_db.pop('administrative_area_level_1')
        result = db.execute_sql("INSERT INTO %s (lat,lng,PostedTime,route, \
        sublocality, city, country) values (%s,%s,'%s','%s','%s','%s','%s');" % (whom, str(lat), str(lng),
                                                        d_string,
                                                        to_db['route'],
                                                        to_db['sublocality'],
                                                        to_db['administrative_area_level_2'],
                                                        to_db['country']
                                                       )
                               )
        print result
            
    def plot_last_locations(self, who_table, count = 5):
        locations = []
        try:
            d = Database.Database()
        except:
            return render.index("Connection to Database failed! Consider starting MySQL server!")
            
        sql_query = "select lat, lng from %s order by PostedTime desc limit %s;" % (str(who_table), str(count))
        
        rows = d.execute_sql(sql_query)
        
        if len(rows) == 0:
            return render.index("No records in Database for this query: %s " % sql_query)
        
        for row in rows:
            lat = row[0]
            lng = row[1]
            w = Weather.Weather(lat, lng)
            tag = str(w.current_weather())
            locations.append((tag, lat, lng))

        return render.map_plot("Showing last %s locations from table %s" % (str(count),str(who_table))
                               , locations)
    
    def get_last_locations(self, who_table, count = 5):
        '''
        I am aware that this is duplicated code and it should not be done, 
        but I have no more time for refactoring. Please, excuse me!
        '''
        locations = []
        try:
            d = Database.Database()
        except:
            return render.index("Connection to Database failed! Consider starting MySQL server!")
            
        sql_query = "select lat, lng from %s order by PostedTime desc limit %s;" % (str(who_table), str(count))
        
        rows = d.execute_sql(sql_query)
        
        if len(rows) == 0:
            return render.index("No records in Database for this query: %s " % sql_query)
        
        for row in rows:
            lat = row[0]
            lng = row[1]
            locations.append((lat, lng))
            
        return locations
        

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

class GetAndroidData():
    
    def GET(self):
        raise Exception("Not Implemented")
    
    def POST(self):
        i = web.input(lat=45, lng=42, the_type="CriminalLocation")
        locg = LocateGuy()
        
        try:
            db = Database.Database()
        except:
            return render.index("Connection to Database failed! Consider starting MySQL server!")
            
        rows = db.execute_sql("SELECT lat,lng FROM %s ORDER BY id DESC LIMIT 1" % str(i.the_type))
        #print rows
        #db.close()
        eps = 0.001
        
        global criminal_count
        if(rows != ()):
            for x in rows:
                xlat = float(format(x[0], '4f'))
                xlng = float(format(x[1], '4f'))
                wlat = float(format(float(i.lat), '4f'))
                wlng = float(format(float(i.lng), '4f'))
                print xlat, xlng, wlat, wlng
                if(abs(xlat - wlat) < eps and abs(xlng - wlng) < eps):
                    return 'Nothing to do, you are in the same place'
                else:
                    locg.add_to_db(i.lat, i.lng, i.the_type)
                    
                    criminal_count = criminal_count + 1
                    
                    if(criminal_count > (sys.maxint - 2) ):
                        criminal_count = 0
                    log.debug( "Done sending to database this data from a POST request in GetAndroidData(): %s, %s, %s" % (str(i.lat),
                                str(i.lng),
                                str(i.the_type)) )
        else:
            locg.add_to_db(i.lat, i.lng, i.the_type)
            
            criminal_count = criminal_count + 1
            
            if(criminal_count > (sys.maxint - 2) ):
                criminal_count = 0
            log.debug( "Done sending to database this data from a POST request in GetAndroidData(): %s, %s, %s" % (str(i.lat),
                        str(i.lng),
                        str(i.the_type)) )
            
        
        return "Done sending to database your data: %s, %s, %s. Counter = %s\n\n" % (str(i.lat),
                            str(i.lng),
                            str(i.the_type), str(criminal_count))
                            

class Criminal(LocateGuy):
    def GET(self):
        return super(Criminal, self).plot_last_locations("CriminalLocation", 5)

class Test:
    def GET(self):
        return render.map_plot("text", dummy_list=[ ("Pensiunea Andre, Sinaia, Furnica", 45.3571195, 25.5397671), 
                                            ("Mihai's home", 44.4171, 26.1102),  # Acasa
                                            ("home2", 44.4171, 26.1105),  # Acasa2
                                            ("Coordonatele accidentului din Apuseni", 46.6023,  22.98421),     
                                            ("Delta Vacaresti", 44.402913, 26.136045), 
                                            ("Sulina", 45.185360, 29.655238),  
                                            ("Techirghiol", 44.057735, 28.596516),  
                                            ("Parcul National Retezat", 45.331103, 22.822643)   
                                        ])
class Distances:
    def GET(self):
        c = Criminal()
        v = Victim()
        
        how_many = 3
        
        c_locs = c.get_last_locations("CriminalLocation", how_many)
        v_locs = v.get_last_locations("VictimLocation", how_many)
        
        distances = []
        for cl, vl in zip(c_locs, v_locs):
            #Compute distances
            lat1 = cl[0]
            lng1 = cl[1]
            lat2 = vl[0]
            lng2 = vl[1]
            d = utils.compute_distance(lat1, lng1, lat2, lng2)
            distances.append(d)
        
        #print distances
        return render.distances(distances, how_many)

if __name__ == "__main__":
    
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
