"""
This module deals with file 'locations.list' and creates an html file.
"""
import certifi

import ssl

import geopy.geocoders

from geopy.geocoders import Nominatim

ctx = ssl.create_default_context(cafile=certifi.where()) 
geopy.geocoders.options.default_ssl_context = ctx

geolocator = Nominatim(user_agent="hello", scheme='http')
import re
import csv

def read_file(path: str) -> list:
    """
    Function reads file 'locations.list' and returns it as a list of lists.
    >>> read_file("locations.list")[:3]
    [['"#1 Single" (2006)', '', '', '', '', 'Los Angeles, California, USA'],\
    ['"#1 Single" (2006)', '', '', '', '', 'New York City, New York, USA'],\
    ['"#15SecondScare" (2015) {It\'s Me Jessica (#1.5)}', 'Coventry, West Midlands, England, UK']]
    """
    with open(path, encoding="utf8", errors='ignore') as file:
        
        data = [(line.strip()).split('\t') for line in file]

    return data
# print(read_file('locations.list')[:3])


def get_needed_info(data: list) -> list:
    """
    Function returns the title, year and location of the movies.
    >>> get_needed_info(read_file('locations.list')[:3])
    [['"#1 Single" ', 2006, 'Los Angeles, California, USA'],\
    ['"#1 Single" ', 2006, 'New York City, New York, USA'],\
    ['"#15SecondScare" ', 2015, 'Coventry, West Midlands, England, UK']]
    """
    info = []
    for line in data:
        location = line[-1]
        # if '(' in location or ')' in location:
        #     location = line[-2]
        location = location.replace('\n', '')

        if 'Federal District' not in location and 'Highway' not in location:
            name = line[0]
            if '(' in name or ')' in name:
                index = name.find('(')
                film = name[:index]
            date = re.search(r'\(([^)]+)\)', name).group(1)

            try:
                date = int(date)

            except ValueError:
                continue
            film_line = [film, date, location]

            if film_line in info:
                continue
            else:
                info.append(film_line)

    return info
# print(get_needed_info(read_file('locations2222.list')))

import geopy.distance
from geopy.exc import GeocoderUnavailable
from geopy.exc import GeocoderTimedOut

def create_csv(info):
    '''
    Function creates a csv files with (film, year, location, latitude, longitude).
    '''
    with open('location.csv', 'w') as file:
        writer = csv.writer(file, delimiter='|', quotechar=' ', quoting=csv.QUOTE_ALL, lineterminator='\n')
        for film_line in info:
            try:
                location = geolocator.geocode(film_line[2])
                writer.writerow([film_line[0], film_line[1], film_line[2], location.latitude, location.longitude])
            except AttributeError:
                continue
            except GeocoderTimedOut:
                continue
            except GeocoderUnavailable:
                pass
# create_csv(get_needed_info(read_file('newlocations.list')))
from math import radians, cos, sin, atan, sqrt, asin

def calculate_haversine_distance(latitude1, longitude1, latitude2, longitude2):
    """
    Returns the distance between two locations on Earth with given longitudes and 
    latitudes.
    >>> calculate_haversine_distance(53.32055555555556, -1.7297222222222221, 53.31861111111111, -1.6997222222222223)
    2.0043678382716137
    """
    longitude1, latitude1, longitude2, latitude2 = map(radians, [longitude1, latitude1, longitude2, latitude2])
    distancelon = longitude2 - longitude1
    distancelat = latitude2 - latitude1
    first_value = (cos(latitude1) * cos(latitude2) * sin(distancelon/2)**2)
    second_value = sin(distancelat/2)
    final_value = 2*asin(sqrt(second_value**2 + first_value))
    distance = final_value * 6371
    return distance
# print(calculate_haversine_distance(53.32055555555556, -1.7297222222222221, 53.31861111111111, -1.6997222222222223))

def films_distance_and_nearest(year, latitude, longitude):
    """
    Returns list of lists with films, that were released in a year that
    was given by user and distance to these films from the user's location.
    >>> films_distance_and_nearest(2017, 49.83826, 24.02324)[:2]
    [[' "#Hashtag  Travel  UK"   ', ' England,  UK ', 1778.2784041544705, \
    ' 52.5310214 ', ' -1.2649062 '], [' "#Hashtag  Travel"   ', \
    ' Poughkeepsie,  New  York,  USA ', 7091.835097405759, ' 41.7065539 ', ' -73.9283672 ']]
    """
    this_year_films = []
    with open ('location.csv', 'r') as csv_file :
        csv_reader = csv.reader(csv_file, delimiter='|')
        for film_line in csv_reader:
            try:
                film_year = int(film_line[1])
                if film_year == int(year) :
                    distance_to_user = calculate_haversine_distance(float(film_line[3]), float(film_line[4]), latitude, longitude)
                    this_year_films.append([film_line[0], film_line[2], distance_to_user, film_line[3], film_line[4]])
            except IndexError:
                pass
        this_year_films.sort(key=lambda film_line: film_line[2])
        num_nearest = len(this_year_films)
        if num_nearest > 10:
            this_year_films = this_year_films[0:10]     
    return this_year_films
# print(films_distance_and_nearest(2020, 49.83826, 24.02324))

import folium

def create_map(user_latitude, user_longitude, this_year_films, year):
    """
    Function creates a map with 10(or less) film locations, user's location and a location in Zhytomyr city.
    """
    user_location = []
    user_location.append(user_latitude)
    user_location.append(user_longitude)
    fig = folium.FeatureGroup(name = 'Films Map')
    mapp = folium.Map(tiles='Stamen Terrain', location=user_location, zoom_start=17)
    fig2 = folium.FeatureGroup(name = 'Your location')
    mapp.add_child(folium.Marker(location=user_location,popup="You are here",color="#800000",fill=True,fill_color="#3186cc",icon=folium.Icon()))
    mapp.add_child(fig2)

    for film_line in this_year_films:
        if film_line[2] < 1500:
            fig.add_child(folium.CircleMarker(location=[film_line[3], film_line[4]],radius=10,color='#00FF00',fill=True,fill_color="#00FF00", popup=film_line[0],icon=folium.Icon()))


        elif 1500 < film_line[2] < 2500 :
            fig.add_child(folium.CircleMarker(location=[film_line[3], film_line[4]],radius=10,color='yellow',fill=True,fill_color="yellow",popup=film_line[0],icon=folium.Icon()))

        else:
            fig.add_child(folium.CircleMarker(location=[film_line[3], film_line[4]],radius=10,color='red',fill=True,fill_color="red",popup=film_line[0],icon=folium.Icon()))

    mapp.add_child(fig)
    fig3 = folium.FeatureGroup(name = 'Special Place in Zhytomyr')
    zhytomyr_loc = [50.58832765, 27.6136538943799]
    mapp.add_child(folium.Marker(location=zhytomyr_loc,popup= ('<a href=\"https://www.youtube.com/watch?v=rWk_ZF-o8IU">Welcome to Житомир</a>')))

    mapp.add_child(fig3)
    mapp.add_child(folium.LayerControl())
    mapp.save('{}_map_films.html'.format(year))
    return '{}_map_films.html'.format(year)

if __name__ == "__main__":
    year = input("Please enter a year you would like to have a map for: ")
    coords = input("Please enter your location (format: lat, long): ").split(", ")
    latitude = float(coords[0])
    longitude = float(coords[1])
    # info = get_needed_info(read_file('newlocations.list'))
    # create_csv(get_needed_info(read_file('newlocations.list')))
    print("Generating film coordinates...")
    this_year_films = films_distance_and_nearest(year, latitude, longitude)
    print("Map is generating...")
    create_map(latitude, longitude, films_distance_and_nearest(year, latitude, longitude), year)
    print("Finished. Please have look at the map {}_map_films.html".format(year))