# i modified the codes from the references below with my personal HERE API Key 
# by inserting local time in Rome/Italy,
# setting location (latitudes, longitudes) of a chosen frame in Lanciano/Italy and
# scheduling the task using Windows Task Scheduler with another 2 alternatives for scheduling in Python,
# as well as elaborated comments to make the script clearer

# references:
# https://towardsdatascience.com/visualizing-real-time-traffic-patterns-using-here-traffic-api-5f61528d563
# https://data.mendeley.com/datasets/g64s8h9k57/3

# set your target folder path for saving results
basePath="target_folder_path"

# set your personal HERE API Key
apiKey="your_HERE_API_key"

# matplotlib is used for visualization
from matplotlib import pyplot as plt
# numpy is used when working with arrays
import numpy as np
# matplotlib.cm is used to make colormaps
import matplotlib.cm as cm

# Requests is an HTTP library
import requests
# dill is used for serialization of objects
import dill
# sys module provides access to system-specific parameters and functions
import sys
# OS module provides functions for interacting with the operating system
import os

# BeautifulSoup is used for pulling data out of HTML and XML files
from bs4 import BeautifulSoup
# time module is used for representing time
from time import gmtime, strftime
# xml.etree.ElementTree is used to parse XML data
from xml.etree.ElementTree import XML, fromstring, tostring

# datetime helps working with date and time
from datetime import datetime
# pytz helps working with timezones
from pytz import timezone

# the desired format is DD-MM-YY_HHMM
frmt = "%d-%m-%Y_%H%M"
# set variable to local time in Rome/Italy
time_in_italy = datetime.now(timezone('Europe/Rome'))
# rearrange local time in Italy in previously set format
timestamp = time_in_italy.strftime(frmt)
print(timestamp)

# for this case, Lanciano in Abruzzo Region is going to be examined
city_name = 'lanciano'
# set folder name according to city name
folderPath = os.path.join(basePath, city_name)
# if the path doesn't exist
if not os.path.exists(folderPath):
    # create the directory
    os.mkdir(folderPath)
print("We are working is folder " + str(folderPath))

# XML file name and extension should be set as well as the right mode
# to write file which is 'w'
xml_file = open(folderPath+'/'+city_name+'_'+timestamp+'.xml', "w")

# request data from HERE API service with given parameters
# API Key is accessible after a login in HERE Developer and
# latitudes and longitudes of chosen left-top and right-bottom points of the frame should be inserted
page = requests.get('https://traffic.ls.hereapi.com/traffic/6.1/flow.xml?bbox='+'42.271921'+'%2C'+'14.337169'+'%3B'+'42.167677'+'%2C'+'14.449779'+'&apiKey='+apiKey+'&responseattributes=sh,fc')

# use lxml parser in BeautifulSoup
soup = BeautifulSoup(page.text, "lxml")
# find all roads
roads = soup.find_all('fi')
# write roads to xml file
xml_file.write(str(roads))
# close the file
xml_file.close()

loc_list_hv=[]
lats=[]
longs=[]
sus=[]
ffs=[]
c=0
for road in roads:
    #for j in range(0,len(shps)):
    myxml = fromstring(str(road))
    fc=5
    for child in myxml:
        # de: location names
        if('de' in child.attrib):
            de = str(child.attrib['de'])
        # fc: for the functional class information
        if('fc' in child.attrib):
            fc = int(child.attrib['fc'])
        # cn: confidence, an indication how HERE determined the speed.
        if('cn' in child.attrib):
            cn = float(child.attrib['cn'])
        # su: speed of actual drivers in km/hour
        if('su' in child.attrib):
            su = float(child.attrib['su'])
        # ff: free flow speed / average speed if there's no congestion or another negative factor like bad weather
        if('ff' in child.attrib):
            ff = float(child.attrib['ff'])
    # if it is any type of road over 0.2 confidence
    if((fc<=5) and (cn>=0.2)):
        # gather all shapefiles
        shps = road.find_all("shp")
        # iterate for every shapefile
        for j in range(0, len(shps)):
            # rearrange the latitude - langitude data for latlong
            latlong = shps[j].text.replace(',',' ').split()
            # print(de)
            # print(fc)
            # print(su)
            # print(ff)
            # print(latlong)
            la=[]
            lo=[]
            su1=[]
            ff1=[]

            # the rest is necessary in case of plotting, if skipped you'd still have xml data
            for i in range(0, int(len(latlong)/2)):
                loc_list_hv.append([float(latlong[2*i]), float(latlong[2*i+1]), float(su), float(ff)])
                # print(loc_list_hv)
                la.append(float(latlong[2*i]))
                lo.append(float(latlong[2*i+1]))
                # append each speed to su1 list
                su1.append(float(su))
                # append each free flow speed to ff1 list
                ff1.append(float(ff))
            lats.append(la)
            longs.append(lo)
            # append the mean value of speeds in su1 list to sus
            sus.append(np.mean(su1))
            # append the mean value of free flow speeds in ff1 list to ffs
            ffs.append(np.mean(ff1))

# create a figure object
fig = plt.figure()
# use a dark background
plt.style.use(['dark_background'])
# plot grid is not preferred
plt.grid(False)
for i in range(0, len(lats)):
    if(sus[i]/ffs[i] < 0.25):
        plt.plot(longs[i], lats[i], c='brown',linewidth=0.5)
    elif(sus[i]/ffs[i] < 0.5):
        plt.plot(longs[i], lats[i], c='red',linewidth=0.5)
    elif(sus[i]/ffs[i] < 0.75):
        plt.plot(longs[i], lats[i], c='yellow',linewidth=0.5)
    else:
        plt.plot(longs[i], lats[i], c='green',linewidth=0.5)

# axis is not wanted in the output
plt.axis('off')
# save the output with desired extension, set resolution, set 'transparent=False' to have a black background, set bounding box in inches to 'tight'
plt.savefig(folderPath+'/'+city_name+'_'+timestamp+'.png', dpi=200, transparent=False, bbox_inches='tight')