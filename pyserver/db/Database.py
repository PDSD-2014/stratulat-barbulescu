# A generic class to interact from python code with our database

import sys
sys.path.append("..")

import configuration as cfg
import MySQLdb as sql
import string 

import PDSDlogging
log = PDSDlogging.PDSDlogging()
log = log.logger

import unicodedata
import datetime
import pytz

class Database(object):
    
    def __init__(self, db = cfg.DB_NAME,
                        host = cfg.DB_SRV,
                        usr = cfg.DB_USR,
                        passwd = cfg.DB_PASSWD):
        self.database = db
        self.host = host
        self.user = usr
        self.password = passwd
        self.connected = False
        
        try:
            self.con = sql.connect(host = host, user = usr, passwd = passwd, db = db)
            self.cursor = self.con.cursor()
        except:
            log.exception("Connection to database failed. Host server wrong, or database server stopped")
            raise Exception("DB Connection failed")
        
        self.connected = True
        log.info("Connection succesful to database")
    
    def execute_sql(self, query):
        
        if(self.connected == False):
            log.warning("SQL query not executed: Not connected to database")
            return []
        
        #Paranoic: normalize query, to have characters mysql varchar accepts
        unicode_query = u''
        unicode_query = unicode_query + query
        query = unicodedata.normalize('NFKD', unicode_query).encode('ascii', 'ignore')        
        
        log.debug("SQL query was : %s" % query)

        try:
            val = self.cursor.execute(query)
            log.debug("SQL query executed was: %s" % str(self.cursor._last_executed))
        except sql.Error, e:
            self.con.rollback()
            log.exception("MySQL Query Error: ")
            
        try:
            fetch = self.cursor.fetchall()
        except:
            fetch = []
        
        self.cursor.connection.commit()
        
        return fetch
    
    def make_dict(table_name, table_rows):
        #not tested!!!
        table_cols = self.execute_sql("SHOW COLUMNS FROM %s;" % table_name)
        ret = []
        
        for row in table_rows:
            if row:
                d = {}
                for i, hdr in enumerate(table_cols):
                    d[hdr[0]] = row[i]
                ret.append(d)
        
        return ret
        
    def close(self):
        if(self.connected == True):
            self.cursor.close()
            self.con.close()
    
    def __del__(self):
        self.close()

if __name__ == "__main__":
    # For testing purposes:
    import json
    import urllib2

    filter_types = None
        

    def get_geonames(lat, lng, types = ['route',
                                        'sublocality', 
                                        'administrative_area_level_1', 
                                        'administrative_area_level_2', 
                                        'country']):
        url = 'http://maps.googleapis.com/maps/api/geocode/json' + \
                '?latlng={},{}&sensor=false'.format(lat, lng)
        jsondata = json.load(urllib2.urlopen(url))
        address_comps = jsondata['results'][0]['address_components']
            
        flag = 'no'
        for x in address_comps:
            if 'sublocality' in x['types']:
                flag = 'yes'
                break

        if flag == 'yes':
            types.remove('administrative_area_level_1')
        else:
            types.remove('sublocality')
        
        global filter_types
        filter_types = types
        filter_method = lambda x: len(set(x['types']).intersection(types))
        return filter(filter_method, address_comps)

        
    
    #Do some testing with PDSD database
    db = Database()
    
    rows = db.execute_sql("SELECT * FROM CriminalLocation;")
    print rows
    
    coords = [ (45.3571195, 25.5397671), # Pensiunea Andre, Sinaia, Furnica
                (44.417126, 26.110211),  # Acasa
                (46.6023,  22.98421),    # Coordonatele accidentului din Apuseni
                (44.402913, 26.136045),  # Delta Vacaresti
                (45.185360, 29.655238),  # Sulina
                (44.057735, 28.596516),  # Techirghiol
                (45.331103, 22.822643)   # Parcul National Retezat
            ]
    
    retstr = u''
    for (lat, lng) in coords: 
        types = ['route',
                'sublocality', 
                'administrative_area_level_1', 
                'administrative_area_level_2', 
                'country']
        to_db = dict()
        for geoname in get_geonames(lat, lng, types):
            common_types = set(geoname['types']).intersection(set(filter_types))
            tmp_key = str(list(common_types)[0])
            to_db[tmp_key] = u'{}'.format(geoname['long_name'])
        
        if 'administrative_area_level_1' in to_db.keys():
            to_db['sublocality'] = to_db.pop('administrative_area_level_1')
        
        #print to_db
        crt_date = datetime.datetime.now(pytz.timezone("Europe/Bucharest"))
        fmt = '%Y-%m-%d %H:%M:%S'
        d_string = crt_date.strftime(fmt)
        result = db.execute_sql("INSERT INTO VictimLocation (lat,lng,PostedTime,route, \
        sublocality, city, country) values (%s,%s,'%s','%s','%s','%s','%s');" % (str(lat), str(lng),
                                                        d_string,
                                                        to_db['route'],
                                                        to_db['sublocality'],
                                                        to_db['administrative_area_level_2'],
                                                        to_db['country']
                                                       )
                               )

    rows = db.execute_sql("SELECT * FROM VictimLocation;")
    print rows
