#Name: Bryan Huebner
#Date: 12 November 2014
#Description: Script developed for Twitter API data mining - collects "tweets" based on selected word and returns
#             details in the form of 'name of account holder'; 'user name'; 'actual tweet'; and 'coordinates'


import TwitterSearch
from TwitterSearch import *
import arcpy
from arcpy import env

tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
tso.set_keywords(['Seahawks'])  # let's define all words we would like to have a look for
tso.set_include_entities(False)  # and don't give us all those entity information
tso.set_geocode(47.2414, -122.4594, 250, False)  # set the range for twitter data locations

#object creation with secret token
ts = TwitterSearch(
    consumer_key = 'epawverCluWXSg54JB9xNQK6R',
    consumer_secret = 'KBZdE43sY3iLBuob45Qt9Q9P9NGokJdhJQ2y4rd6o1vfUBGpr1',
    access_token = '2841952236-HSeeNzs9Z9NxAnmXxx9Mt21FHPekJA4xDIjkHH5',
    access_token_secret = 'UHmRamF6KUQOLg78PAysfR5NATk035UyIaKeA9rj8BkcV')

env.workspace = "E:\GIS_501\Labs\Lab_7\Python_Scripts\Results"
arcpy.env.overwriteOutput = True
fc = "Tweety.shp"

chart1 = 4152  # GCS_North_American_1983_HARN = 4152 (factory code)
spat_ref = (chart1)  # spatial reference = GCS_North_American_1983_HARN

# create new feature class - define as a point and call the spatial reference
arcpy.CreateFeatureclass_management("E:\GIS_501\Labs\Lab_7\Python_Scripts\Results", "Tweety", "POINT", "", "", "", spat_ref)

# create fields in the attribute table
arcpy.AddField_management(fc, "TWEETED_BY", "TEXT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(fc, "POSTED", "TEXT", "", "", 100, "", "NULLABLE")
arcpy.AddField_management(fc, "USER_NAME", "TEXT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(fc, "LAT", "FLOAT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(fc, "LONG", "FLOAT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(fc, "DATE", "TEXT", "", "", 30, "", "NULLABLE")

# use insert cursor to create rows for each of the points
in_curs = arcpy.da.InsertCursor("E:\GIS_501\Labs\Lab_7\Python_Scripts\Results\Tweety.shp", ["SHAPE@XY"])

# iterate through selected tweets
for tweet in ts.search_tweets_iterable(tso):
    if tweet['place'] is not None:
        # use update cursor to poulate rows with tweet data
        up_curs = arcpy.da.UpdateCursor("E:\GIS_501\Labs\Lab_7\Python_Scripts\Results\Tweety.shp",  
                                      ["TWEETED_BY", "POSTED", "USER_NAME", "LAT", "LONG", "DATE"]) 
        cords = (tweet['coordinates'])
        list_cords = list(reduce(lambda x, y: x + y, cords.items()))
        xy = list_cords[3]
        var1 = []
        cord_loc = xy[1], xy[0]
        var1.append(cord_loc)
        in_curs.insertRow(var1)
        tweeted_by = (tweet['user']['name'])
        posted = (tweet['text'])
        user_name = (tweet['user']['screen_name'])
        lat = xy[1]
        lon = xy[0]
        loc = (tweet['created_at'])

        for row in up_curs:
            if row[0] == " ":
                row[0] = tweeted_by
                up_curs.updateRow(row)
            elif row[1] == " ":
                row[1] = posted
                up_curs.updateRow(row)
            elif row[2] == " ":
                row[2] = user_name
                up_curs.updateRow(row)
            elif row[3] == 0:
                row[3] = lat
                up_curs.updateRow(row)
            elif row[4] == 0:
                row[4] = lon
                up_curs.updateRow(row)
            elif row[5] == " ":
                row[5] = loc
                up_curs.updateRow(row)

print "Successful operation"
