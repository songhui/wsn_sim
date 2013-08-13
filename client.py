from filter import *

initialize()

sink = Sink("s")


f1 = Filter("f1", reportTo = sink)
f2 = Filter("f2", reportTo = f1)

se = SensorFilter("se", sensor = SensorSource(), reportTo = f2)

filters = [sink,f1,f2,se]

for f in filters:
    f.activateMe()
    
simulate(until = 100)

for f in filters:
    try:
        print "%s => %s" % (f.name, f.reportTo.name)
    except:
        pass