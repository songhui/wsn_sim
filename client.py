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
f3 = Filter("f3", reportTo = f2)
f3.getDataFrom.add(None)

sink.setNode(n1)
f1.setNode(n2)
f2.setNode(n2)
f3.setNode(n3)

ss = SensorSource(host = n3)
ss.activateMe()


nodes = [n1,n2,n3]
for n in nodes:
    n.activateMe()
    
simulate(until = 100)


 