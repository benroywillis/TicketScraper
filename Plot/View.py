import matplotlib.pyplot as plt
import ReadData as RD

def Plot(dataMap):
  # groups data by event, section; each section has time-sorted entries for time,day,price,size tuples
  groupData = {}
  for event in sorted(dataMap):
    if groupData.get(event) is None:
      groupData[event] = {}
    for day in sorted(dataMap[event]):
      for time in sorted(dataMap[event][day]):
        for entry in dataMap[event][day][time]:
          price    = entry[0]
          section  = entry[1]
          quantity = entry[2]
          if groupData[event].get(section) is None:
            groupData[event][section] = []
          groupData[event][section].append( (time, day, price, quantity) )

  # now plot by event and label by section
  for event in groupData:
    for section in groupData[event]:
      plt.title(event)
      xlabels = [ RD.reverseMapTime(x[0], x[1]) for x in groupData[event][section] ]
      plt.scatter( [x[0]/86400+x[1] for x in groupData[event][section]], [x[2] for x in groupData[event][section]],label=section )
      plt.xticks(ticks = [x[0]/86400+x[1] for x in groupData[event][section]], labels = xlabels, rotation=75)
      plt.legend(frameon=False, loc="lower center")
      plt.ylabel("$")
    plt.show()

dataMap = RD.RetrieveData()
Plot(dataMap)
