import math
import configuration
import json
import urllib2

def compute_distance(lat1, lng1, lat2, lng2, unit="km"):
    """
    This function computes distance based on latitude and longitude
    between 2 points on Earth

    Returned result is given in unit. By default is in kilometers

    Code snipped is taken from John D. Cook. All credits go to him!
    Source:  http://www.johndcook.com/python_longitude_latitude.html
    """
    
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = lng1*degrees_to_radians
    theta2 = lng2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    
    if unit == 'km':
        d = arc * 6373.00
    elif unit == 'miles':
        d = arc * 3960.00

    return d


def compute_route_distance(lat1, lng1, lat2, lng2, lang='en-US', units='metric'):
    """
    Compute the distance between two points
     using Google Maps API Distance Matrix
    based on latitude and longitude

    Full documentation of the url json dump is here:
    https://developers.google.com/maps/documentation/distancematrix/
    """
    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins=%s,%s&destinations=%s,%s&language=%s&units=%s&sensor=false" % (str(lat1), str(lng1), str(lat2), str(lng2), str(lang), str(units))
    #print url
    jsondata = json.load(urllib2.urlopen(url))
    orig = jsondata["origin_addresses"][0]
    dest = jsondata["destination_addresses"][0]

    dispstr = u' and  '.join((orig, dest)).encode('utf-8').strip()

    print 'You have requested distance between %s \n' % (str(dispstr))

    dist = jsondata["rows"][0]["elements"][0]["distance"]["text"]
    duration = jsondata["rows"][0]["elements"][0]["duration"]["text"]

    print "Distance is %s and it takes %s" % (str(dist), str(duration))




