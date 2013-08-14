from filter import *

initialize()

n1 = Node("n1")
n2 = Node("n2")
n3 = Node("n3")

n1.addNeighbour(n2)  
n2.addNeighbour(n3)

sink = Sink("s")
f1 = Filter("f1", reportTo = sink)
f2 = Filter("f2", reportTo = f1)
se = SensorFilter("se", sensor = SensorSource(), reportTo = f2)

sink.setNode(n1)
f1.setNode(n2)
f2.setNode(n2)
se.setNode(n3)

filters = [sink,f1,f2,se]
for f in filters:
    f.activateMe()
    
simulate(until = 100)

for f in filters:
    try:
        print "%s => %s" % (f.name, f.reportTo.name)
    except:
        pass