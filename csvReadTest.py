import csv
import os.path
import numpy as np
import cv2 as cv
from time import sleep

img = cv.imread('C:\\Users\\Kyle Bartido\\Documents\\FTP\\smallPoteka.jpg',1)
overlay = img.copy()
output = img.copy()
alpha = 0.05

#stations = ['00173455','00173456','00173457','00173458','00173459','00174722','00174723','00174724','00174725','00174726','00174727','00174728','00174729','00174730','00174731','00174732','00174733','00174734','00174735','00181271','00181272','00181274','00181283','00181284','00181285','00181286','00181287','00181288','00181289','00181290','00181291','00181292']
stations = {'00173456': {'location':'MMDA EFCOS', 'city':'Pasig City', 'xCoords':365,'yCoords':324},
            '00173457': {'location':'ASTI', 'city':'Quezon City', 'xCoords':339,'yCoords':239},
            '00173458': {'location':'Tapayan Pumping Station', 'city':'Rizal', 'xCoords':412,'yCoords':424},
            '00173459': {'location':'San Andres Pumping Station', 'city':'Manila', 'xCoords':226,'yCoords':350},
            '00174722': {'location':'De La Salle Araneta University', 'city':'Malabon','xCoords':211,'yCoords':198},
            '00174723': {'location':'MMDA Catmon', 'city':'Malabon', 'xCoords':139,'yCoords':199},
            '00174724': {'location':'Brgy. Elias Aldana', 'city':'Las Pinas', 'xCoords':181,'yCoords':538},
            '00174725': {'location':'Brgy. Punturin', 'city':'Valenzuela','xCoords':198,'yCoords':75},
            '00174726': {'location':'Las Pinas Science High School', 'city':'Las Pinas', 'xCoords':189,'yCoords':613},
            '00174727': {'location':'Brgy. Ugong', 'city':'Valenzuela', 'xCoords':229,'yCoords':116},
            '00174728': {'location':'MMDA Balut Pumping Station', 'city':'Manila', 'xCoords':162,'yCoords':269},
            '00174729': {'location':'CAAP', 'city':'Pasay','xCoords':223,'yCoords':471},
            '00174730': {'location':'DOST Compound', 'city':'Bicutan Taguig','xCoords':303,'yCoords':516},
            '00174731': {'location':'Brgy. Bagbaguin', 'city':'Valenzuela', 'xCoords':218,'yCoords':123},
            '00174732': {'location':'RED Training Center', 'city':'Pasig','xCoords':353,'yCoords':371},
            '00174733': {'location':'Dr. Filemon HS', 'city':'Las Pinas','xCoords':232,'yCoords':605},
            '00174734': {'location':'VCDRRMO Bldg', 'city':'Valenzuela', 'xCoords':161,'yCoords':158},
            '00174735': {'location':'PAGASA Science Garden', 'city':'Quezon City', 'xCoords':288,'yCoords':246},
            '00181271': {'location':'Quezon City High School', 'city':'Quezon City','xCoords':276,'yCoords':268},
            '00181272': {'location':'TUP Taguig', 'city':'Taguig','xCoords':276,'yCoords':482},
            '00181274': {'location':'E. Library, Technological College', 'city':'Pateros','xCoords':332,'yCoords':403},
            '00181283': {'location':'Bayanan Elementary School', 'city':'Muntinlupa','xCoords':304,'yCoords':651},
            '00181284': {'location':'C3 Bldg.', 'city':'Mandaluyong','xCoords':273,'yCoords':359},
            '00181285': {'location':'Xavier School', 'city':'San Juan','xCoords':283,'yCoords':315},
            '00181286': {'location':'Anabu 1-B', 'city':'Imus Cavite','xCoords':115,'yCoords':678},
            '00181287': {'location':'Unibersidad de Manila', 'city':'Manila', 'xCoords':185,'yCoords':334},
            '00181288': {'location':'Centennial Park', 'city':'Navotas', 'xCoords':129,'yCoords':234},
            '00181289': {'location':'MMDA Libertad PS', 'city':'Pasay', 'xCoords':196,'yCoords':418},
            '00181290': {'location':'RAVE Pasig City', 'city':'Pasig','xCoords':381,'yCoords':367},
            '00181291': {'location':'Greenheights Subdivision', 'city':'Paranaque','xCoords':247,'yCoords':545},
            '00181292': {'location':'Quezon City Science High School', 'city':'Quezon City', 'xCoords':266,'yCoords':219}}



events = {'000000':[]}

pathString ="C:\\Users\\Kyle Bartido\\Documents\\FTP\\P-Poteka Files\\Jan 4 0843AM"
daySelected = '20200117'
#print(os.path.join(pathString,stations[0],'Plate'))
def convertMonth(month):
    if(month=='01'):
        return 'January'
    elif(month=='02'):
        return 'February'
    elif(month=='03'):
        return 'March'
    elif(month=='04'):
        return 'April'
    elif(month=='05'):
        return 'May'
    elif(month=='06'):
        return 'June'
    elif(month=='07'):
        return 'July'                               
    elif(month=='08'):
        return 'August'
    elif(month=='09'):
        return 'September'
    elif(month=='10'):
        return 'October'
    elif(month=='11'):
        return 'November'        
    elif(month=='12'):
        return 'December'

def convertToHumanTime(strikeTime):
    year = strikeTime[1:5]
    month = convertMonth(strikeTime[5:7])
    day = strikeTime[7:9]
    hour = strikeTime[9:11]
    minute = strikeTime[11:13]
    second = strikeTime[13:15]
    finishedString = month+' '+day+' '+year+'  '+hour+':'+minute+':'+second
    return(finishedString)

def retrieveStationsToDraw(events):
    listOfStations=[]
    for event in events:
        currentStation = event['stationID']
        if currentStation not in listOfStations:
            listOfStations.append(currentStation)
    return listOfStations




def rowToEventData(row):
    data = {'stationID':row[0],'datetime':row[3],'startTime':row[6],'endTime':row[7],'peakAtStart':row[8],'peakAtEnd':row[9],'gpsStatus':row[10]}
    return data

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

def draw_events(event,x,y,flags,param):
    
    if event == cv.EVENT_LBUTTONDBLCLK:
        for hr in range(24):
            stringHr=str(hr)
            if(hr<10): stringHr = '0'+stringHr
            for minute in range(60):
                stringMin=str(minute)
                if(minute<10): stringMin = '0'+stringMin
                for sec in range(60):
                    stringSec = str(sec)
                    if(sec<10): stringSec = '0'+stringSec
                    currentDateTime=stringHr+stringMin+stringSec
                    entireDateTime='\''+daySelected+currentDateTime+'\''         
                    if currentDateTime not in events:
                        None
                    else:
                        #print('at '+convertToHumanTime(entireDateTime)+ ' there were '+ str(len(events[currentDateTime])) +' events')
                        stationsToDraw=retrieveStationsToDraw(events[currentDateTime])
                        #print(str(retrieveStationsToDraw(events[currentDateTime])))
                        for station in stationsToDraw:
                            print(station)
                            currentDict = stations.get(station)
                            if 'eventCount' not in currentDict:
                                currentDict['eventCount']=1
                            else:
                                currentDict['eventCount']+=1
                            stationX=currentDict['xCoords']
                            stationY=currentDict['yCoords']
                            currentEventCount=currentDict['eventCount']
                            print('Station has had '+ str(currentEventCount)+' number of events')
                            #stationX=stations.get(station)['xCoords']
                            #stationY=stations.get(station)['yCoords']
                            if currentEventCount*2 < 255:
                                cv.circle(overlay,(stationX,stationY),35,(0,165,currentEventCount*2),-1)
                            else: cv.circle(overlay,(stationX,stationY),35,(0,165,255),-1)
                            cv.putText(overlay, str(currentDict['eventCount']),(stationX-5, stationY+3), cv.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2)
                            cv.putText(overlay, str(currentDict['location']),(stationX-10, stationY+16), cv.FONT_HERSHEY_SIMPLEX, .3, (255, 255, 255), 1)
                            cv.waitKey(50)


                            
                    
                    cv.addWeighted(overlay, alpha, output, 1 - alpha,0, output)
                    #cv.putText(output, convertToHumanTime(entireDateTime),(10, 30), cv.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 255), 3)
                    #cv.imshow('Output',output)
                cv.putText(output, convertToHumanTime(entireDateTime),(10, 30), cv.FONT_HERSHEY_SIMPLEX, .7, (255, 255, 255), 2)
                cv.imshow('Output',output)
                cv.waitKey(10)
                        
                       
                        #print('sample of events list: ' + str(events[currentDateTime]))
        #print('x: '+str(x)+ '   y: '+str(y))





for station in stations:
    directory=os.path.join(pathString,station,'Plate')
    print(directory)
    print(stations.get(station)['city'])
    for root,dirs,files in os.walk(directory):
        for file in files:
           if file.endswith(".csv"):
                if daySelected in file:
                    fileDir = os.path.join(directory,file)
                    with open(fileDir, 'r') as csvfile:
                        csv_reader = csv.reader(csvfile, delimiter=',')
                        line_count = 0
                        cityStrike = stations.get(station)['city']
                        for row in csv_reader:
                            #print('Lightning Strike Happened at '+convertToHumanTime(repr(row[3]))+ ' near ' + station['city'] + ' at '+ station['location'])
                            #print(rowToEventData(row))
                            currentEvent = rowToEventData(row)
                            currentTime = currentEvent['datetime'][8:14]
                            #print('time is:' +currentTime)
                            arr = []
                            arr.append(currentEvent)
                            if currentTime not in events:
                                events[currentTime] = arr
                            else: 
                                events[currentTime].append(currentEvent)

                        #pretty(events)

                           #print('Row0: ' +row[0]+' Row1: '+row[1]+' Row2: '+row[2]+' Row3: '+row[3]+' Row4: '+row[4]+ ' Row5: '+row[5]+ ' Row6: '+row[6]+ ' Row7: '+row[7]+ ' Row8: '+row[8]+ ' Row9: '+row[9]+ ' Row10: '+row[10]+ ' Row11: '+row[11])



for hr in range(24):
    stringHr=str(hr)
    if(hr<10): stringHr = '0'+stringHr
    for minute in range(61):
        stringMin=str(minute)
        if(minute<10): stringMin = '0'+stringMin
        for sec in range(61):
            stringSec = str(sec)
            if(sec<10): stringSec = '0'+stringSec
            currentDateTime=stringHr+stringMin+stringSec
            entireDateTime='\''+daySelected+currentDateTime+'\''         
            if currentDateTime not in events:
                None
            else:
                #print('at '+convertToHumanTime(entireDateTime)+ ' there were '+ str(len(events[currentDateTime])) +' events')
                print(str(retrieveStationsToDraw(events[currentDateTime])))
                #print('sample of events list: ' + str(events[currentDateTime]))
                print(' ')

cv.namedWindow('image')
cv.setMouseCallback('image',draw_events)

while(1):
    cv.imshow('image',img)
    if cv.waitKey(20) & 0xFF == 27:
        break
cv.destroyAllWindows()


