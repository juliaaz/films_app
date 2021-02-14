|Films app|
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
This program generates a map with locations of films which were released in the year given by user and 10(or less) films which are near the user's place.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|Functions:|
Module includes 7 different functions:
1. read_file.
|Function reads file from path ('locations.list'). Return list of lists.|
2. get_needed_info.
|Function returns the title, year and location of the movies. (list of lists)|
3. create_csv.
|Function creates a csv file 'locations.csv' with (film, year, location, latitude, longitude) of every movie from the list of lists created be the previous function.|
4. calculate_haversine_distance.
|Returns the distance between two locations on Earth with given longitudes and latitudes. In this function the haversinus formula is used.|
5. films_distance_and_nearest.
|Returns list of lists with films, that were released in a year that was given by user and distance to these films from the user's location. The previous function(calculate_haversine_distance) is used in this one|
6. create_map.
|Function creates a map with 10(or less) film locations, user's location and a location in Zhytomyr city.|
The last one is a main one and creates an html file  with different markers of locations. The others are for working with given data.
---------------------------------------------------------------------------------------------------------------------------------------
|Example of usage|:
--------------------------------------------------------------------------
Warning!!!
Program with newlocations.list works more than 2-3 minutes, so if you want to get a map quickly I recoomend using location.csv. Just uncomment lines 180-181.
The user indicates for the films for which year he wants to build a map and his location as latitude and longitude (e.g. 49.83826,24.02324), and as a result receives an HTML file.
User receives a message 'Please enter a year you would like to have a map for:' in order to input a year he/she would like to get movies of. (in example year input is 1978)
Then user receives a new message 'Please enter your location (format: lat, long):' after which he/she has to input his/her location's latitude and longitude. (in example user input is 49.83826,24.02324)
After this, user receives a message:
--------------------------------------------------------------------------
    "Map is generating...
    Please wait...
    Finished. Please have look at the map (input_year)_movies_map.html"
--------------------------------------------------------------------------
Here is an example off input in a Terminal:
![Photo](images/example_input.png?raw=true "An example of user's input and the terminals output")
---------------------------------------------------------------------------------------------------------------------------------------
|Result|

The result is a map with three layers: the films' locations, user's locations and a locations of a special place in Zhytomyr. You can add and remove layers on the map using the layer control.

Note: if user clicks on a marker of Zhytomyr's special place, you can click on an active url with text 'Welcome to Житомир' which sends user to the Youtube video which is called 'Гімн Житомира. Культурна версія'.
Here is an example:
![Photo](images/screenshot_of_zhytomyr.png?raw=true "Here is a special place in Zhytomyr oblast and a marker with an active url with text 'Welcome to Житомир'")

Note2.0: Movie location markers have three different colors: green, yellow, red. The color depends on the insistence of the location from the user. :
1. If the location is at a distance of up to 1500 km, the marker is green.
2. if the distance is from 1500 to 2500 km, the marker becomes yellow. 
3. Accordingly, if the distance from the user more than 2500 km, the marker becomes red.
After clicking on a location marker, user receives a name of the movie that was filmed in that place.

Here is an example:
![text](images/screenshot_of_map.png?raw=true "You can see movie location markers with three different colors, user's location (created be input) and a location in Zhytomyr")
