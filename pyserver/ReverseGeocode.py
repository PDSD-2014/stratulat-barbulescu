import json
import urllib2

fmt_addr = None

def get_geonames(lat, lng, types):
    url = 'http://maps.googleapis.com/maps/api/geocode/json' + \
            '?latlng={},{}&sensor=false'.format(lat, lng)
    #print url
    jsondata = json.load(urllib2.urlopen(url))
    global fmt_addr
    fmt_addr = str(jsondata['results'][0]['formatted_address'])
    address_comps = jsondata['results'][0]['address_components']
    filter_method = lambda x: len(set(x['types']).intersection(types))
    return filter(filter_method, address_comps)


if __name__ == '__main__':

    types = ['sublocality', 'locality', 'administrative_area_level_1', 'country', 'administrative_area_level_2' ]

    # Pensiunea Andre, Sinaia, Furnica
    lat, lng = 45.3571195, 25.5397671

    #MY home
    #lat, lng = 44.417126, 26.110211

    #Coordonatele accidentului din Apuseni
    #lat, lng = 46.6023,  22.98421

    # Display all geographical names along with their types
    for geoname in get_geonames(lat, lng, types):
        common_types = set(geoname['types']).intersection(set(types))
        print '{} ({})'.format(geoname['long_name'], ', '.join(common_types))
