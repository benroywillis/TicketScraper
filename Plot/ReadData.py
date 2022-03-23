import os
import re

def reverseMapTime(date, time):
  """
  Maps integer date and time to a string
  Date should be an integer of the number of days past 00/00/0000
  time should be the integer second in the day
  """
  year = int( date/365 )
  date = date - year*365
  date = date - int(year/4) # leap years
  month = "Jan"
  while( date > 28 ):
    # we iteratively go through months until we don't have enough days left to get to the next month
    if month == "Jan":
      month = "Feb"
      date = date - 31
    elif month == "Feb":
      month = "Mar"
      date = date - 28
    elif month == "Mar":
      month = "Apr"
      date = date - 31
    elif month == "Apr":
      month = "May"
      date = date - 30
    elif month == "May":
      month = "Jun"
      date = date - 31
    elif month == "Jun":
      month = "Jul"
      date = date - 30
    elif month == "Jul":
      month = "Aug"
      date = date - 31
    elif month == "Aug":
      month = "Sep"
      date = date - 31
    elif month == "Sep":
      month = "Oct"
      date = date - 30
    elif month == "Oct":
      month = "Nov"
      date = date - 31
    elif month == "Nov":
      month = "Dec"
      date = date - 30
    else:
      print("Ran out of months to subtract!")
  day = date

  # parse time
  hour = int(time / 3600)
  time = time - hour*3600
  minute = int( time / 60 )
  time = time - minute*60
  second = time
  return str(day)+"-"+str(month)+"-"+str(year)+"_"+str(hour)+":"+str(minute)+":"+str(second)

def getMonthDays(month):
  """
  Counts the number of days that have occured before the input <month> occurs
  month input should be an integer
  """
  if month == 1:
    return 0
  elif month == 2:
    return 31
  elif month == 3:
    return 59
  elif month == 4:
    return 90
  elif month == 5:
    return 120
  elif month == 6:
    return 151
  elif month == 7:
    return 181
  elif month == 8:
    return 212
  elif month == 9:
    return 243
  elif month == 10:
    return 273
  elif month == 11:
    return 304
  elif month == 12:
    return 334
  else:
    print("Month not recognized!")
    return 0

def getEventName(name):
  """
  @brief Returns the name of an event from a filename that includes data information
  The filename format should be as follows
  <EventName>_<Date>_<Time>.csv
  Where each category has some rules
  All categories: no newline characters or commas
  <EventName>: Only letters and numbers
  <Date>: dd-mm-yyyy
  <Time>: hh:mm:ss
  """
  return name.split("_")[0]

def getDate(name):
  """
  @brief Returns the date of an event from a filename that includes data information
  The date is returned as an integer of the number of days from 00-00-0000 to the input date
  The filename format should be as follows
  <EventName>_<Date>_<Time>.csv
  Where each category has some rules
  All categories: no newline characters or commas
  <EventName>: Only letters and numbers
  <Date>: dd-mm-yyyy
  <Time>: hh:mm:ss
  """
  dateString = name.split("_")[1]
  dayString  = dateString.split("-")[0]
  monthString  = dateString.split("-")[1]
  yearString  = dateString.split("-")[2]
  # years + leapdays + month days + days
  return int(yearString) * 365 + int( int(yearString) / 4 ) + getMonthDays( int(monthString) ) + int(dayString)

def getTime(name):
  """
  Returns the number of seconds from 00:00:00 as described in the input filename <name>
  The filename format should be as follows
  <EventName>_<Date>_<Time>.csv
  Where each category has some rules
  All categories: no newline characters or commas
  <EventName>: Only letters and numbers
  <Date>: dd-mm-yyyy
  <Time>: hh:mm:ss
  """
  timeString = name.split("_")[2].split(".")[0]
  hourString = timeString.split(":")[0]
  minuteString = timeString.split(":")[1]
  secondString = timeString.split(":")[2]
  return int(hourString) * 3600 + int(minuteString) * 60 + int(secondString)

def parseData(name):
  """
  Reads the input csv file described by name
  name should be a complete path to the file
  The file should be in format
  Price,section,ticket_num
  Price: $<float>
  section: <string>
  ticket_num: <x - y tickets> or <x tickets> and an "instant download" can follow these
  """
  data = []
  with open(name, "r") as f:
    columns = f.readline()
    for line in f:
      price = float( line.split(",")[0].strip("$") )
      section = line.split(",")[1]
      ticketString = line.split(",")[2]
      # with the ticketString, we are just looking for %d+\sticket, as in <4 ticket> in "row ANYTIME ENTRY 1 - 4 tickets"
      ticketQuantity = re.findall("\d+\sticket", ticketString)
      if len(ticketQuantity):
        # just take the first one
        tickets = int( ticketQuantity[0].split(" ")[0] )
      else:
        print("Multiple expressions found in ticket number string!: "+ str(ticketQuantity) + " from string: " + ticketString)
        tickets = 0
      data.append( [price, section, tickets] )
  return data

def RetrieveData():
  """ 
  maps an event to a map of dates, each data has a map of times, each time has a 2d list of price data
  """
  # open as many data files as we can
  files = []
  for file in os.scandir("../Data/"):
    if file.name.endswith(".csv"):
      files.append(file)

  inputData = {}
  for f in files:
    EN = getEventName(f.name)
    if inputData.get( EN ) is None:
      inputData[EN] = {}
    if inputData[EN].get(getDate(f.name)) is None:
      inputData[EN][getDate(f.name)] = {}
    inputData[EN][getDate(f.name)][getTime(f.name)] = parseData(f.path)
  return inputData

