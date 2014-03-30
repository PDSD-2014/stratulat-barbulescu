import sys

import configuration
import json
import urllib2

kelvin_default = 273.15

# No \n was used, as JSON marker for plotting on Gmap doesn't like this character

class Weather(object):
    
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
        
        url = 'http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s' % (str(self.lat), str(self.lng))

        self.jsondata = json.load(urllib2.urlopen(url))

            
    def get_description(self):
                
        retstr = ''
        jsondata = self.jsondata
        
        # Retrieve weather description
        retstr = retstr + str(jsondata["weather"][0]["main"]) + ", " + \
            str(jsondata["weather"][0]["description"]) + ", "
        
        self.description = retstr
            
        return retstr
    
    def get_temperatures(self):
        """
        Obtain minimum , maximum and current temperature values
        """

        retstr = ''
        
        # Open Weather gives us the values in Kelvin!
        # We, as Romanians, generally read it in Celsius
        temp_min = float(self.jsondata["main"]["temp_min"]) - kelvin_default
        temp_max = float(self.jsondata["main"]["temp_max"]) - kelvin_default
        temp_crt = float(self.jsondata["main"]["temp"]) - kelvin_default
        
        retstr = 'Current temp: %.2f C, Max: %.2f C, Min: %.2f C, ' % (temp_crt,
                                                                temp_max,
                                                                temp_min)
        return retstr
        
    def get_wind_humidity(self):
        
        wind_speed = float(self.jsondata["wind"]["speed"])
        humidity = float(self.jsondata["main"]["humidity"])
        
        retstr = 'Windspeed: %.3f m/s, Humidity: %.2f' % (wind_speed, humidity)
        
        return retstr

    def current_weather(self):
        """
        Return string containing multiple info about weather based on lat and lng
        """
        retstr = ''
        retstr = 'OpenWeatherMap API -- Retrieving weather data from: %s, ' % (str(self.jsondata["name"]))
        retstr = retstr + self.get_description() + self.get_temperatures() + self.get_wind_humidity()

        
        return retstr
        
        
if __name__ == '__main__':
    # A cruel test
    coords = [ (45.3571195, 25.5397671), # Pensiunea Andre, Sinaia, Furnica
                (44.417126, 26.110211),  # Acasa
                (46.6023,  22.98421),    # Coordonatele accidentului din Apuseni
                (44.402913, 26.136045),  # Delta Vacaresti
                (45.185360, 29.655238),  # Sulina
                (44.057735, 28.596516),  # Techirghiol
                (45.331103, 22.822643)   # Parcul National Retezat
            ]
    for (lat, lng) in coords:
        w = Weather(lat, lng)
        print w.current_weather()
